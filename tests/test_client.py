import unittest
import socket
from client import receive_frame

class TestClient(unittest.TestCase):
    def test_client_receive_frame(self):
        mock_frame = b'frame_data'
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send(mock_frame)

        received_frame = receive_frame(client_socket)  # Your client function for receiving frames
        self.assertEqual(received_frame, mock_frame)
