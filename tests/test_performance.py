import unittest
from prometheus_client import Gauge
from main import fps_metric, detection_count_metric

class TestPerformance(unittest.TestCase):
    def test_fps_metric(self):
        # Simulate FPS update
        fps_metric.set(30)
        self.assertEqual(fps_metric._value.get(), 30)

    def test_detection_count_metric(self):
        # Simulate detection count update
        detection_count_metric.set(5)
        self.assertEqual(detection_count_metric._value.get(), 5)
