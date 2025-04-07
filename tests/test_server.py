import unittest
import socket
from unittest.mock import patch, MagicMock
from main import start_server, process_frame, model, tracker

class TestServer(unittest.TestCase):
    @patch("main.socket.socket")
    def test_server_start(self, MockSocket):
        # Simulate a server start
        mock_socket = MagicMock()
        MockSocket.return_value = mock_socket
        server_socket = start_server()
        self.assertIsNotNone(server_socket)
        MockSocket.return_value.bind.assert_called_with(('0.0.0.0', 8001))
    
    @patch("main.model")
    @patch("main.tracker.update_tracks")
    def test_process_frame(self, mock_tracker, mock_model):
        # Mock frame processing
        frame = MagicMock()  # Simulate a frame object
        mock_model.return_value = []  # No detections for simplicity
        mock_tracker.return_value = []  # No objects tracked

        detections = process_frame(frame)

        self.assertEqual(detections, [])
        mock_model.assert_called_with(frame)  # Ensure model was called
        mock_tracker.update_tracks.assert_called_with([], frame)
