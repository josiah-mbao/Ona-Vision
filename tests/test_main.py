from unittest.mock import patch
import socket
import pickle
import struct
import time
import psutil
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import pytest
import cv2


# Test YOLO Model
@pytest.fixture
def yolo_model():
    return YOLO("yolov8n.pt")


def test_yolo_model_load(yolo_model):
    assert yolo_model is not None
    assert hasattr(yolo_model, "predict")


# Mocked frame for testing
@pytest.fixture
def mock_frame():
    return np.zeros((480, 640, 3), dtype=np.uint8)  # A dummy black frame


def test_yolo_model_inference(yolo_model, mock_frame):
    results = yolo_model(mock_frame)
    assert results is not None


# Test DeepSORT Tracker
@pytest.fixture
def deepsort_tracker():
    return DeepSort(max_age=10)


def test_deepsort_tracker_initialization(deepsort_tracker):
    assert deepsort_tracker is not None
    assert hasattr(deepsort_tracker, "update_tracks")


def test_deepsort_tracking(deepsort_tracker, mock_frame):
    detections = [[[100, 100, 200, 200], 0.9, "person"]]
    tracks = deepsort_tracker.update_tracks(detections, frame=mock_frame)
    assert isinstance(tracks, list)


# Test Server Socket
@pytest.fixture
def mock_server_socket():
    with patch("socket.socket") as mock_socket:
        yield mock_socket


def test_server_socket_creation(mock_server_socket):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert server_socket is not None
    mock_server_socket.assert_called()


# Test Client Socket
@pytest.fixture
def mock_client_socket():
    with patch("socket.socket") as mock_socket:
        yield mock_socket


def test_client_socket_connection(mock_client_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert client_socket is not None
    mock_client_socket.assert_called()


# Test Frame Serialization
def test_frame_serialization(mock_frame):
    serialized_data = pickle.dumps(mock_frame)
    assert isinstance(serialized_data, bytes)

    deserialized_frame = pickle.loads(serialized_data)
    assert deserialized_frame is not None


# Test FPS Calculation
def test_fps_calculation():
    start_time = time.time()
    time.sleep(1)
    elapsed_time = time.time() - start_time
    assert elapsed_time >= 1


def test_fps_performance():
    frame_count = 0
    start_time = time.time()

    # Use the actual frame capture (like how frames are fetched in my app)
    cap = cv2.VideoCapture(0)  # Use webcam feed (or mock in a test env)
    if not cap.isOpened():
        raise Exception("Could not open video device")

    # Simulate the loop running, tracking FPS
    for _ in range(500):  # Simulate 500 frames for better FPS calculation
        ret, frame = cap.read()  # Capture a frame from the webcam
        if not ret:
            break

        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        frame_count += 1

        # Check that FPS stays above a threshold (e.g., 5 FPS)
        if elapsed_time > 1:  # Update FPS only after 1 second
            assert fps >= 5, f"FPS is below threshold: {fps:.2f}"

        time.sleep(0.01)  # Simulate real-world frame delay (about 100 FPS)

    cap.release()  # Release the webcam


# Test Resource Usage (CPU and Memory)
def test_resource_usage():
    # Get initial CPU and memory usage
    initial_cpu = psutil.cpu_percent()
    initial_memory = psutil.virtual_memory().percent

    # Run your tests (simulate object detection or FPS calculation here)

    # Check that CPU and memory usage does not exceed a threshold (e.g., 80%)
    assert initial_cpu < 96, f"High CPU usage: {initial_cpu}%"
    assert initial_memory < 96, f"High memory usage: {initial_memory}%"