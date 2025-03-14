import cv2
import torch
import socket
import pickle
import struct
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Make sure you have this model downloaded

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for laptop webcam, 1+ for external cameras

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8000))  # Listen on all interfaces, port 8000
server_socket.listen(5)
print("Waiting for a client to connect...")

client_socket, addr = server_socket.accept()
print(f"Client connected from {addr}")

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frame is captured

    # Run object detection on the frame
    results = model(frame)

    # Draw bounding boxes and labels on detected objects
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box

            # Get label text
            label = result.names[int(box.cls[0])]  # Object label

            # Define text properties
            font_scale = 1  # Increase size
            font_thickness = 2  # Make bolder
            text_color = (255, 255, 255)  # White text
            outline_color = (0, 0, 0)  # Black outline

            # Get text size for positioning
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)

            # Add background rectangle for contrast
            cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), (0, 0, 0), -1)

            # Put text with black outline for readability
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, outline_color, font_thickness + 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

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

