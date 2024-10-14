
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import I2C_LCD_driver  # Thư viện để điều khiển LCD I2C

# Cấu hình các chân GPIO
DHT_PIN = 4  # Chân GPIO kết nối với cảm biến DHT11/DHT22
BUZZER_PIN = 18  # Chân GPIO kết nối với còi CHIP
UP_BUTTON_PIN = 23  # Nút nhấn tăng giới hạn nhiệt độ
DOWN_BUTTON_PIN = 24  # Nút nhấn giảm giới hạn nhiệt độ
DHT_SENSOR = Adafruit_DHT.DHT11  # Chọn loại cảm biến (DHT11 hoặc DHT22)

# Thiết lập nhiệt độ giới hạn mặc định
temp_limit = 30  # Giới hạn nhiệt độ ban đầu

# Trạng thái báo động
alarm_active = False

# Khởi tạo LCD
lcd = I2C_LCD_driver.lcd()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Cấu hình các chân GPIO
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_temp_and_humidity():
    """
    Đọc giá trị nhiệt độ và độ ẩm từ cảm biến DHT.
    """
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def update_lcd(temperature, humidity, temp_limit):
    """
    Hiển thị nhiệt độ, độ ẩm và giới hạn nhiệt độ trên màn hình LCD.
    """
    lcd.lcd_clear()
    lcd.lcd_display_string(f"Temp: {temperature:.1f}C", 1)
    lcd.lcd_display_string(f"Humidity: {humidity:.1f}%", 2)
    lcd.lcd_display_string(f"Limit: {temp_limit}C", 2, 12)  # Hiển thị nhiệt độ giới hạn ở góc phải

def check_buttons():
    """
    Kiểm tra trạng thái của các nút nhấn (Up, Down) để điều chỉnh giới hạn nhiệt độ.
    """
    global temp_limit
    if GPIO.input(UP_BUTTON_PIN) == GPIO.LOW:  # Nút Up nhấn
        temp_limit += 1
        time.sleep(0.2)  # Tránh hiện tượng debounce
    if GPIO.input(DOWN_BUTTON_PIN) == GPIO.LOW:  # Nút Down nhấn
        temp_limit -= 1
        time.sleep(0.2)

def activate_alarm():
    """
    Kích hoạt báo động khi nhiệt độ vượt quá giới hạn.
    """
    global alarm_active
    alarm_active = True
    lcd.lcd_clear()
    lcd.lcd_display_string("ALERT: Over Temp!", 1)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(5)  # Cảnh báo trong 5 giây
    deactivate_alarm()

def deactivate_alarm():
    """
    Kết thúc báo động.
    """
    global alarm_active
    alarm_active = False
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    lcd.lcd_clear()

def loop():
    global alarm_active

    try:
        while True:
            # Đọc nhiệt độ và độ ẩm
            temperature, humidity = read_temp_and_humidity()

            # Hiển thị thông tin lên LCD
            update_lcd(temperature, humidity, temp_limit)

            # Kiểm tra nút nhấn để điều chỉnh giới hạn nhiệt độ
            check_buttons()

            # Kiểm tra nếu nhiệt độ vượt quá giới hạn
            if temperature > temp_limit and not alarm_active:
                activate_alarm()

            # Kiểm tra nếu có nút nhấn trong khi báo động để tắt báo động
            if alarm_active and (GPIO.input(UP_BUTTON_PIN) == GPIO.LOW or GPIO.input(DOWN_BUTTON_PIN) == GPIO.LOW):
                deactivate_alarm()

            time.sleep(1)  # Chu kỳ cập nhật mỗi giây
    except KeyboardInterrupt:
        pass

def destroy():
    """
    Đặt lại trạng thái các chân GPIO khi thoát chương trình.
    """
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    loop()
    destroy()
