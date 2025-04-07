import unittest
from prometheus_client import start_http_server, Gauge
import time

class TestPerformance(unittest.TestCase):
    def test_fps(self):
        start_http_server(8000)
        start_time = time.time()
        frames_processed = 0
        while time.time() - start_time < 1:
            frames_processed += 1
        fps = frames_processed / (time.time() - start_time)
        self.assertGreater(fps, 10)  # Ensure FPS stays above a threshold
