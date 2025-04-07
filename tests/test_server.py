import unittest
from main import start_server, process_frame

class TestServer(unittest.TestCase):
    def test_server_start(self):
        # Example of testing the server startup
        server_socket = start_server()
        self.assertIsNotNone(server_socket)

    def test_frame_processing(self):
        frame = process_frame('tests/sample_frame.jpg')
        self.assertIsNotNone(frame)
