import unittest
from yolov8_model import YOLOv8
import cv2

class TestYOLOv8(unittest.TestCase):
    def setUp(self):
        self.image = cv2.imread('tests/sample_frame.jpg')  # Sample image for detection

    def test_object_detection(self):
        model = YOLOv8()
        detections = model.detect(self.image)
        self.assertGreater(len(detections), 0)  # Ensure that detection occurs
