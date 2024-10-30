import time
import threading
import paho.mqtt.client as mqtt
import json
from EmulatorGUI import GPIO  # Sử dụng GPIO giả lập từ EmulatorGUI.py
from DHT22 import DHT22  # Cảm biến DHT22
from Moisture import Moisture  # Cảm biến độ ẩm đất
from MPU6050 import MPU6050  # Gia tốc kế và con quay hồi chuyển
from Ultrasonic import Ultrasonic  # Cảm biến siêu âm
from Vibration import Vibration  # Cảm biến rung

# MQTT Config
BROKER_ADDRESS = "broker.hivemq.com"
TOPIC = "landslide/sensor_data"
NODE_ID = "Node_3"

client = mqtt.Client(client_id=NODE_ID, protocol=mqtt.MQTTv311)

try:
    client.connect(BROKER_ADDRESS)
    print(f"{NODE_ID} connected to MQTT broker successfully.")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

# Cấu hình các chân GPIO
DHT_PIN = 4              # Chân tín hiệu DHT22
MOISTURE_PIN = 17        # Chân tín hiệu cảm biến độ ẩm
MPU6050_SDA = 2          # Chân SDA của MPU6050
MPU6050_SCL = 3          # Chân SCL của MPU6050
ULTRASONIC_TRIG_PIN = 23 # Chân Trig của cảm biến siêu âm
ULTRASONIC_ECHO_PIN = 24 # Chân Echo của cảm biến siêu âm
VIBRATION_PIN = 27       # Chân tín hiệu cảm biến rung

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)

dht22 = DHT22(DHT_PIN)
moisture_sensor = Moisture(MOISTURE_PIN)
mpu = MPU6050()
ultrasonic_sensor = Ultrasonic(trig_pin=ULTRASONIC_TRIG_PIN, echo_pin=ULTRASONIC_ECHO_PIN)
vibration_sensor = Vibration(pin=VIBRATION_PIN)

running = True  # Đặt trạng thái mô phỏng là chạy

# Khởi tạo khóa để đảm bảo đồng bộ giữa các luồng
sensor_lock = threading.Lock()

def read_sensors():
    # Đọc dữ liệu từ các cảm biến
    with sensor_lock:
        temperature, humidity = dht22.read_data()
        soil_moisture = moisture_sensor.read_moisture()
        accel_gyro = mpu.get_accel_gyro()
        distance = ultrasonic_sensor.get_distance()
        vibration_status = vibration_sensor.detect_vibration()
    
    return temperature, humidity, soil_moisture, accel_gyro, distance, vibration_status

# Hàm gửi dữ liệu lên MQTT broker
last_publish_time = 0
PUBLISH_INTERVAL = 3  # Giây

def send_data():
    global last_publish_time
    while running:
        current_time = time.time()
        if current_time - last_publish_time >= PUBLISH_INTERVAL:
            temperature, humidity, soil_moisture, accel_gyro, distance, vibration = read_sensors()
            data = {
                'node_id': NODE_ID,
                'temperature': temperature,
                'humidity': humidity,
                'soil_moisture': soil_moisture,
                'accel_gyro': accel_gyro,
                'distance': distance,
                'vibration': vibration
            }
            result = client.publish(TOPIC, json.dumps(data))
            if result.rc == 0:
                print(f"{NODE_ID} successfully published data to topic {TOPIC}.")
            else:
                print(f"{NODE_ID} failed to publish data. Result code: {result.rc}")
            last_publish_time = current_time

# Khởi động luồng đọc và gửi dữ liệu cảm biến
sensor_thread = threading.Thread(target=send_data, daemon=True)
sensor_thread.start()

# Giữ chương trình chạy
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
    print("Stopping sensor simulation...")
