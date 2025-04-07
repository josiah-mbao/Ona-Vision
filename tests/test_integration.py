import unittest
from unittest.mock import MagicMock
from main import start_server
from client import receive_frame

class TestIntegration(unittest.TestCase):
    def test_server_client_integration(self):
        # Mock server and client
        server_socket = MagicMock()
        client_socket = MagicMock()

        # Simulate sending a frame from the server to the client
        mock_frame = b"frame_data"
        client_socket.sendall(mock_frame)

        # Simulate receiving the frame in the client
        received_frame = receive_frame(mock_frame)
        
        self.assertEqual(received_frame, mock_frame)  # Ensure the frame was received correctly
        server_socket.sendall.assert_called_with(mock_frame)
