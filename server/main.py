import socket
import pickle
import struct
import time
import cv2
import psutil
import threading
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

# Start Prometheus metrics server
start_http_server(8000)

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8001))
server_socket.listen(5)
print("Waiting for clients...")

def handle_client(client_socket):
    print(f"Client connected from {client_socket.getpeername()}")

    # Initialize webcam per client (optional: move outside to share across threads)
    cap = cv2.VideoCapture("crowd_demo.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()

        # YOLO inference
        results = model(frame)

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0].item()
                class_id = int(box.cls[0])
                class_name = result.names[class_id]

                detections.append(([x1, y1, x2, y2], confidence, class_name))

        # Object tracking
        tracked_objects = tracker.update_tracks(detections, frame=frame)

        for track in tracked_objects:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            label = f"{track.get_det_class()} (ID: {track_id})"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Prometheus metrics
        fps_metric.set(1.0 / (time.time() - start_time))
        detection_count_metric.set(len(tracked_objects))

        # Send frame
        data = pickle.dumps(frame)
        msg_size = struct.pack("Q", len(data))
        try:
            client_socket.sendall(msg_size + data)
        except BrokenPipeError:
            print("Client disconnected.")
            break

    cap.release()
    client_socket.close()

# Accept loop
while True:
    client_socket, _ = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.daemon = True
    client_thread.start()
