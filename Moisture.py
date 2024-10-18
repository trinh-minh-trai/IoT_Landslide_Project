import random

class Moisture:
    def __init__(self, pin):
        self.pin = pin

    def read_moisture(self):
        # Giả lập độ ẩm từ 0% đến 100%
        moisture_level = random.uniform(0, 100)
        return round(moisture_level, 2)
