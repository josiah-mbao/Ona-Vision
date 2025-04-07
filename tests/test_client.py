import unittest
from unittest.mock import patch, MagicMock
import socket
from client import receive_frame, display_frame

class TestClient(unittest.TestCase):
    @patch("client.socket.socket")
    def test_client_connection(self, MockSocket):
        # Simulate a successful connection to the server
        mock_socket = MagicMock()
        MockSocket.return_value = mock_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8001))
        
        self.assertIsNotNone(client_socket)

    @patch("client.pickle.loads")
    @patch("client.cv2.imshow")
    def test_receive_and_display_frame(self, mock_imshow, mock_pickle):
        # Simulate receiving a frame and displaying it
        mock_frame = MagicMock()  # Simulate a frame object
        mock_pickle.return_value = mock_frame
        
        frame_data = b"frame_data"
        received_frame = receive_frame(frame_data)

        self.assertEqual(received_frame, mock_frame)  # Ensure the frame was correctly received
        mock_imshow.assert_called_with("Ona Vision - Live Object Detection", mock_frame)

