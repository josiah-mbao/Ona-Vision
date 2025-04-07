import unittest
import socket
from main import start_server, process_frame
from client import display_frame

class TestIntegration(unittest.TestCase):
    def test_server_client_integration(self):
        # Start server and process a frame
        server_socket = start_server()
        frame = process_frame('tests/sample_frame.jpg')
        
        # Simulate sending the frame from the server to the client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send(frame)
        
        # Ensure the client receives and displays the frame correctly
        received_frame = client_socket.recv(1024)
        self.assertEqual(received_frame, frame)
