import cv2
import socket
import pickle
import struct
import time
import psutil
from collections import defaultdict
from ultralytics import YOLO
from prometheus_client import start_http_server, Gauge

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize Prometheus metrics
fps_metric = Gauge("fps", "Frames per second")
inference_time_metric = Gauge("inference_time_ms", "Inference time in milliseconds")
detection_count_metric = Gauge("detected_objects", "Number of objects detected per frame")
cpu_usage_metric = Gauge("cpu_usage", "CPU usage percentage")
memory_usage_metric = Gauge("memory_usage", "Memory usage percentage")
confidence_metric = Gauge("avg_detection_confidence", "Average detection confidence per frame")
class_count_metric = Gauge("object_count", "Number of objects detected per class", ["class_name"])

# Start Prometheus metrics server
start_http_server(8000)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8001))  # Change port to 8001 to avoid conflicts
server_socket.listen(5)
print("Waiting for a client to connect...")
client_socket, addr = server_socket.accept()
print(f"Client connected from {addr}")

# Define text properties
FONT_SCALE = 1  # Increase size
FONT_THICKNESS = 2  # Make bolder
TEXT_COLOR = (255, 255, 255)  # White text
OUTLINE_COLOR = (0, 0, 0)  # Black outline

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    start_time = time.time()
    
    # Run YOLO inference
    results = model(frame)
    
    # End time for FPS calculation
    end_time = time.time()
    fps = 1.0 / (end_time - start_time)
    inference_time = (end_time - start_time) * 1000  # Convert to ms
    num_detections = len(results[0].boxes)
    
    # Update Prometheus metrics
    fps_metric.set(fps)
    inference_time_metric.set(inference_time)
    detection_count_metric.set(num_detections)
    cpu_usage_metric.set(psutil.cpu_percent())
    memory_usage_metric.set(psutil.virtual_memory().percent)
    
    # Calculate confidence scores
    confidences = [box.conf[0].item() for result in results for box in result.boxes]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    confidence_metric.set(avg_confidence)
    
    # Track per-class counts
    class_counts = defaultdict(int)
    for result in results:
        for box in result.boxes:
            class_counts[result.names[int(box.cls[0])]] += 1
    
    for class_name, count in class_counts.items():
        class_count_metric.labels(class_name=class_name).set(count)
    
    # Draw bounding boxes and labels
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[int(box.cls[0])]
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Get text size
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)
            
            # Add background rectangle for contrast
            cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), OUTLINE_COLOR, -1)
            
            # Put text with black outline for readability
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, OUTLINE_COLOR, FONT_THICKNESS + 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)
    
    # Serialize frame
    data = pickle.dumps(frame)
    msg_size = struct.pack("Q", len(data))
    
    try:
        client_socket.sendall(msg_size + data)
    except BrokenPipeError:
        print("Client disconnected.")
        break

cap.release()
client_socket.close()
server_socket.close()

