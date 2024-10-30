import random

class Vibration:
    def __init__(self, pin):
        self.pin = pin

    def detect_vibration(self):
        # Giả lập trạng thái rung (True/False)
        vibration_detected = random.choice([True, False])
        return vibration_detected
