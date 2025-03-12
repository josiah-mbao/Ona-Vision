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

    # Draw bounding boxes on detected objects
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            label = result.names[int(box.cls[0])]  # Object label
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

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

