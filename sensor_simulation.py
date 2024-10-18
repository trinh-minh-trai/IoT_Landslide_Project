import time
import threading
from EmulatorGUI import GPIO  # Sử dụng GPIO giả lập từ EmulatorGUI.py
from LCD1602 import LCD1616  # Sử dụng lớp LCD1616
from DHT22 import DHT22  # Cảm biến DHT22
from Moisture import Moisture  # Cảm biến độ ẩm đất
from MPU6050 import MPU6050  # Gia tốc kế và con quay hồi chuyển
from Ultrasonic import Ultrasonic  # Cảm biến siêu âm
from Vibration import Vibration  # Cảm biến rung
import requests  # Thư viện để gửi dữ liệu qua HTTP

# Cấu hình các chân GPIO
DHT_PIN = 4              # Chân tín hiệu DHT22
MOISTURE_PIN = 17        # Chân tín hiệu cảm biến độ ẩm
MPU6050_SDA = 2          # Chân SDA của MPU6050
MPU6050_SCL = 3          # Chân SCL của MPU6050
ULTRASONIC_TRIG_PIN = 23 # Chân Trig của cảm biến siêu âm
ULTRASONIC_ECHO_PIN = 24 # Chân Echo của cảm biến siêu âm
VIBRATION_PIN = 27       # Chân tín hiệu cảm biến rung
BUZZER_PIN = 18          # Chân buzzer
UP_BUTTON_PIN = 22       # Chân nút UP
DOWN_BUTTON_PIN = 21     # Chân nút DOWN

# Giới hạn nhiệt độ ban đầu
temp_limit = 30

# API Key và URL của ThingSpeak
THINGSPEAK_API_KEY = 'TU6SKU8JHLQ3NQGR'  # Thay thế bằng API Key của bạn
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Khởi tạo màn hình LCD
lcd = LCD1616()

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Khởi tạo các cảm biến
dht22 = DHT22(DHT_PIN)
moisture_sensor = Moisture(MOISTURE_PIN)
mpu = MPU6050()
ultrasonic_sensor = Ultrasonic(trig_pin=ULTRASONIC_TRIG_PIN, echo_pin=ULTRASONIC_ECHO_PIN)
vibration_sensor = Vibration(pin=VIBRATION_PIN)

running = False  # Trạng thái mô phỏng
lcd_update_interval = 1  # Giây
data_send_interval = 15  # Giây
last_lcd_update_time = time.time()
last_data_send_time = time.time()

def read_sensors():
    # Đọc dữ liệu từ các cảm biến
    temperature, humidity = dht22.read_data()
    soil_moisture = moisture_sensor.read_moisture()
    accel_gyro = mpu.get_accel_gyro()
    distance = ultrasonic_sensor.get_distance()
    vibration_status = vibration_sensor.detect_vibration()

    # In dữ liệu cảm biến ra màn hình
    print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
    print(f"Soil Moisture: {soil_moisture}%")
    print(f"Acceleration/Gyro: {accel_gyro}")
    print(f"Distance: {distance} cm")
    print(f"Vibration Detected: {vibration_status}")

    return temperature, humidity, soil_moisture, accel_gyro, distance, vibration_status

def update_lcd():
    global last_lcd_update_time
    while True:
        if running and (time.time() - last_lcd_update_time >= lcd_update_interval):
            temperature, humidity, soil_moisture, accel_gyro, distance, vibration_status = read_sensors()  # Đọc cảm biến để lấy tất cả dữ liệu
            
            lcd.clear()  # Xóa màn hình
            
            # Hiển thị thông tin trên LCD
            lcd.write_string(f"Temp: {temperature:.1f}C")  # Hiển thị nhiệt độ
            lcd.set_cursor(1, 0)  # Chuyển đến dòng thứ hai
            lcd.write_string(f"Humi: {humidity:.1f}%")  # Hiển thị độ ẩm
            lcd.set_cursor(2, 0)  # Chuyển đến dòng thứ ba
            lcd.write_string(f"Soil: {soil_moisture:.1f}%")  # Hiển thị độ ẩm đất
            lcd.set_cursor(3, 0)  # Chuyển đến dòng thứ tư
            lcd.write_string(f"Dist: {distance:.1f}cm")  # Hiển thị khoảng cách
            lcd.set_cursor(4, 0)  # Chuyển đến dòng thứ năm
            lcd.write_string(f"Vib: {vibration_status}")  # Hiển thị trạng thái rung
            
            # Hiển thị dữ liệu Acceleration
            lcd.set_cursor(5, 0)  # Chuyển đến dòng thứ sáu
            lcd.write_string(f"Accel X: {accel_gyro['accel_x']:.1f}")  # Hiển thị gia tốc X
            lcd.set_cursor(6, 0)  # Chuyển đến dòng thứ bảy
            lcd.write_string(f"Accel Y: {accel_gyro['accel_y']:.1f}")  # Hiển thị gia tốc Y
            lcd.set_cursor(7, 0)  # Chuyển đến dòng thứ tám
            lcd.write_string(f"Accel Z: {accel_gyro['accel_z']:.1f}")  # Hiển thị gia tốc Z
            
            # Hiển thị dữ liệu Gyro
            lcd.set_cursor(8, 0)  # Chuyển đến dòng thứ chín
            lcd.write_string(f"Gyro X: {accel_gyro['gyro_x']:.1f}")  # Hiển thị con quay hồi chuyển X
            lcd.set_cursor(9, 0)  # Chuyển đến dòng thứ mười
            lcd.write_string(f"Gyro Y: {accel_gyro['gyro_y']:.1f}")  # Hiển thị con quay hồi chuyển Y
            lcd.set_cursor(10, 0)  # Chuyển đến dòng thứ mười một
            lcd.write_string(f"Gyro Z: {accel_gyro['gyro_z']:.1f}")  # Hiển thị con quay hồi chuyển Z
            
            last_lcd_update_time = time.time()  # Cập nhật thời gian lần cuối
        time.sleep(0.1)  # Giảm tải CPU một chút

def check_buttons():
    global temp_limit
    # Kiểm tra các nút nhấn để thay đổi giới hạn nhiệt độ
    if GPIO.input(UP_BUTTON_PIN) == GPIO.LOW:
        temp_limit += 1
        time.sleep(0.2)  # Tránh hiện tượng debounce
    if GPIO.input(DOWN_BUTTON_PIN) == GPIO.LOW:
        temp_limit -= 1
        time.sleep(0.2)

def toggle_running():
    global running
    while True:
        if GPIO.input(UP_BUTTON_PIN) == GPIO.LOW:  # Sử dụng UP_BUTTON_PIN để bật/tắt mô phỏng
            running = not running  # Chuyển đổi trạng thái chạy
            time.sleep(0.2)  # Tránh hiện tượng debounce

def activate_alarm():
    # Kích hoạt báo động nếu vượt quá giới hạn nhiệt độ
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    lcd.clear()
    lcd.write_string("ALERT: Over Temp!")
    time.sleep(5)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def send_data_to_thingspeak(temperature, humidity, soil_moisture, accel_gyro, distance, vibration):
    # Tạo payload với các trường Field của ThingSpeak
    data = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': temperature,
        'field2': humidity,
        'field3': soil_moisture,
        'field4': accel_gyro['accel_x'],  # Ví dụ chỉ gửi accel_x
        'field5': distance,
        'field6': 1 if vibration else 0  # Vibration (True/False)
    }

    # Gửi yêu cầu HTTP POST lên ThingSpeak
    response = requests.post(THINGSPEAK_URL, params=data)

    # Kiểm tra phản hồi từ ThingSpeak
    if response.status_code == 200:
        print('Dữ liệu đã được đẩy lên ThingSpeak thành công!')
    else:
        print('Lỗi khi đẩy dữ liệu lên ThingSpeak:', response.status_code)

def loop():
    global last_data_send_time
    alarm_active = False

    while True:
        # Kiểm tra nút nhấn GPIO 21 để thoát chương trình
        if GPIO.input(DOWN_BUTTON_PIN) == GPIO.LOW:  # Sử dụng DOWN_BUTTON_PIN để đóng chương trình
            print("Đóng chương trình...")
            GPIO.cleanup()  # Dọn dẹp GPIO
            break

        if running:
            # Đọc dữ liệu cảm biến
            temperature, humidity, soil_moisture, accel_gyro, distance, vibration = read_sensors()
            
            # Gửi dữ liệu lên ThingSpeak
            if time.time() - last_data_send_time >= data_send_interval:
                send_data_to_thingspeak(temperature, humidity, soil_moisture, accel_gyro, distance, vibration)
                last_data_send_time = time.time()
                
            # Kích hoạt báo động nếu vượt quá giới hạn nhiệt độ
            if temperature > temp_limit and not alarm_active:
                activate_alarm()
                alarm_active = True
            elif temperature <= temp_limit and alarm_active:
                alarm_active = False  # Đặt lại trạng thái báo động

            check_buttons()  # Kiểm tra nút nhấn
            
        time.sleep(0.1)

# Khởi động các luồng
threading.Thread(target=update_lcd, daemon=True).start()
threading.Thread(target=toggle_running, daemon=True).start()
loop()
