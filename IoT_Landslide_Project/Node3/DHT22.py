import random

class DHT22:
    def __init__(self, pin):
        self.pin = pin

    def read_data(self):
        # Giả lập nhiệt độ từ 15°C đến 40°C và độ ẩm từ 20% đến 90%
        temperature = random.uniform(15, 40)
        humidity = random.uniform(20, 90)
        return round(temperature, 2), round(humidity, 2)
