import random

class Ultrasonic:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

    def get_distance(self):
        # Giả lập khoảng cách từ 10 cm đến 200 cm
        distance = random.uniform(10, 200)
        return round(distance, 2)
