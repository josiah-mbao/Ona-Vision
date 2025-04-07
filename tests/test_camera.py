import unittest
from unittest.mock import patch
import cv2

class TestCamera(unittest.TestCase):
    @patch('cv2.VideoCapture')  # Mock the camera feed
    def test_capture_frame(self, MockCamera):
        mock_camera = MockCamera.return_value
        mock_camera.read.return_value = (True, 'frame_data')
        
        frame = capture_frame()  # Replace with the actual method you use to capture frames
        self.assertEqual(frame, 'frame_data')
