"""
Real-time object detection using YOLOv8 and OpenCV.

This script initializes a webcam, runs YOLOv8 object detection, and streams
the processed frames to a client over a socket connection.
"""

import socket
import pickle
import struct
import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Ensure this model is downloaded

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for laptop webcam, 1+ for external cameras

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8000))  # Listen on all interfaces, port 8000
server_socket.listen(5)
print("Waiting for a client to connect...")

client_socket, addr = server_socket.accept()
print(f"Client connected from {addr}")

# Define text properties
FONT_SCALE = 1  # Increase size
FONT_THICKNESS = 2  # Make bolder
TEXT_COLOR = (255, 255, 255)  # White text
OUTLINE_COLOR = (0, 0, 0)  # Black outline

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frame is captured

    # Store original dimensions
    h, w, _ = frame.shape  # Original frame size

    # Resize frame for YOLO processing
    small_frame = cv2.resize(frame, (640, 480))
    sh, sw = small_frame.shape[:2]  # YOLO input size

    # Run object detection on the resized frame
    results = model(small_frame)

    # Draw bounding boxes and labels on detected objects
    for result in results:
        for box in result.boxes:
            # Scale bounding box coordinates back to original frame size
            x1, y1, x2, y2 = map(int, [
                box.xyxy[0][0] * (w / sw),  # Scale X
                box.xyxy[0][1] * (h / sh),  # Scale Y
                box.xyxy[0][2] * (w / sw),  # Scale X
                box.xyxy[0][3] * (h / sh)   # Scale Y
            ])

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Get label text
            label = result.names[int(box.cls[0])]

            # Get text size for positioning
            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)

            # Add background rectangle for contrast
            cv2.rectangle(frame,
                          (x1, y1 - text_height - 10),
                          (x1 + text_width, y1),
                          OUTLINE_COLOR,
                          -1)

            # Put text with black outline for readability
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        FONT_SCALE, OUTLINE_COLOR, FONT_THICKNESS + 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)

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
