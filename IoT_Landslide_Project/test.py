# Node Trung Tâm (Chương Trình Trung Tâm)
import time
import threading
import paho.mqtt.client as mqtt
import requests
import json
import warnings
import subprocess

# Bỏ qua cảnh báo DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# MQTT Config
BROKER_ADDRESS = "broker.hivemq.com"
TOPIC = "landslide/sensor_data"
START_TOPIC = "landslide/start_signal"

# ThingSpeak Config for each node
THINGSPEAK_URL = 'https://api.thingspeak.com/update'
nodes = [
    {"folder": "C:/Users/Trinh Minh Trai/Desktop/gpio/IoT_Landslide_Project/Node1", "command": "python sensor_simulation.py", "api_key": "5QFP900X4EGKUB5S"},
    {"folder": "C:/Users/Trinh Minh Trai/Desktop/gpio/IoT_Landslide_Project/Node2", "command": "python sensor_simulation.py", "api_key": "N6ZRCD2241H13MQO"},
    {"folder": "C:/Users/Trinh Minh Trai/Desktop/gpio/IoT_Landslide_Project/Node3", "command": "python sensor_simulation.py", "api_key": "28ANW3VH3BEXK0MW"}
]

# Khởi tạo MQTT client cho nút trung tâm
client = mqtt.Client(client_id="central_node", protocol=mqtt.MQTTv311)

# Biến để lưu trữ dữ liệu cảm biến từ các node
sensor_data = {}

try:
    client.connect(BROKER_ADDRESS)
    print("Connected to MQTT broker successfully.")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

# Hàm xử lý khi nhận được tin nhắn từ các node
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        print(f"Message received on topic {message.topic}: {payload}")
        node_id = payload['node_id']
        sensor_data[node_id] = payload
        print(f"Successfully received data from {node_id}. Data: {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Cài đặt hàm callback cho sự kiện nhận tin nhắn
client.on_message = on_message
result = client.subscribe(TOPIC)
if result[0] == 0:
    print(f"Successfully subscribed to topic: {TOPIC}")
else:
    print(f"Failed to subscribe to topic: {TOPIC}")

# Hàm gửi dữ liệu tổng hợp lên ThingSpeak
def send_data_to_thingspeak():
    while True:
        if sensor_data:
            for node in nodes:
                print(f"Preparing to send data from node {node['folder'].split('/')[-1]} to ThingSpeak...")
                node_id = node["folder"].split('/')[-1]  # Sử dụng tên thư mục làm node ID
                if node_id in sensor_data:
                    data = sensor_data[node_id]
                    payload = {
                        'api_key': node['api_key'],
                        'field1': data.get('temperature', 0),
                        'field2': data.get('humidity', 0),
                        'field3': data.get('soil_moisture', 0),
                        'field4': data['accel_gyro'].get('accel_x', 0),
                        'field5': data.get('distance', 0),
                        'field6': 1 if data.get('vibration', False) else 0
                    }
                    try:
                        response = requests.post(THINGSPEAK_URL, params=payload)
                        if response.status_code == 200:
                            print(f"Data from {node_id} successfully sent to ThingSpeak!")
                        else:
                            print(f"Failed to send data from {node_id} to ThingSpeak: {response.status_code}")
                    except Exception as e:
                        print(f"Error sending data to ThingSpeak from {node_id}: {e}")
        else:
            print("No data available to send to ThingSpeak yet. Waiting for sensor data...")
            for node in nodes:
                node_id = node["folder"].split('/')[-1]
                if node_id not in sensor_data:
                    print(f"No data received from {node_id} yet.")
        time.sleep(15)  # Giảm thời gian chờ xuống còn 5 giây để cập nhật dữ liệu thường xuyên hơn

# Hàm khởi động các node
started_nodes = set()  # Tập hợp để theo dõi các node đã được khởi động
def start_nodes():
    for node in nodes:
        node_folder = node["folder"]
        if node_folder not in started_nodes:
            try:
                # Chuyển đến thư mục của node và khởi chạy file mô phỏng
                command = node["command"].split()
                subprocess.Popen(command, cwd=node_folder)
                print(f"Started node in folder {node_folder}")
                started_nodes.add(node_folder)  # Đánh dấu node đã được khởi động
            except Exception as e:
                print(f"Failed to start node in folder {node_folder}: {e}")

# Gửi tín hiệu khởi động đến tất cả các node
def send_start_signal():
    result = client.publish(START_TOPIC, json.dumps({"command": "start"}))
    if result.rc == 0:
        print("Start signal sent to all nodes successfully.")
    else:
        print(f"Failed to send start signal. Result code: {result.rc}")

# Khởi động các luồng
# Khởi động các node
start_nodes()

# Gửi tín hiệu khởi động
send_start_signal()

# Khởi động các luồng
threading.Thread(target=send_data_to_thingspeak, daemon=False).start()

# Khởi động các luồng


# Khởi động các node
start_nodes()

# Gửi tín hiệu khởi động
send_start_signal()

# Chờ một khoảng thời gian để các node bắt đầu gửi dữ liệu
time.sleep(15)  # Tăng thời gian để các node con có đủ thời gian khởi động

# Bắt đầu vòng lặp để nhận tin nhắn từ MQTT broker
print("Waiting for sensor data from nodes...")
client.loop_forever()
