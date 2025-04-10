"""
This script captures video from a webcam,
performs object detection using YOLOv8, tracks detected objects using DeepSORT,
and sends the processed video frames to a client over a socket connection.
It also exposes Prometheus metrics for frames per second (FPS)
and the number of detected objects.
"""
import socket
import pickle
import struct
import time
import cv2
import psutil
from collections import defaultdict
from ultralytics import YOLO
from prometheus_client import start_http_server, Gauge
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize DeepSORT tracker
tracker = DeepSort(max_age=10)

# Initialize Prometheus metrics
fps_metric = Gauge("fps", "Frames per second")
detection_count_metric = Gauge("detected_objects", "Number of objects detected per frame")

# Start Prometheus server
start_http_server(8000)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8001))
server_socket.listen(5)
print("Waiting for a client to connect...")
client_socket, addr = server_socket.accept()
print(f"Client connected from {addr}")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()

    # Run YOLO inference
    results = model(frame)

    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            detections.append(([x1, y1, x2, y2], confidence, class_name))

    # Track objects
    tracked_objects = tracker.update_tracks(detections, frame=frame)

    # Draw bounding boxes and labels
    for track in tracked_objects:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()
        x1, y1, x2, y2 = map(int, ltrb)
        LABEL = f"{track.get_det_class()} (ID: {track_id})"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, LABEL, (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Update metrics
    fps_metric.set(1.0 / (time.time() - start_time))
    detection_count_metric.set(len(tracked_objects))

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
