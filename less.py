from EmulatorGUI import GPIO  # Thay thế bằng `import RPi.GPIO as GPIO` nếu chạy trên Raspberry Pi
import time
import traceback

# Danh sách các chân GPIO kết nối với 8 LED
LED_PINS = [5, 6, 13, 19, 26, 21, 20, 16]  # Các chân GPIO cho 8 LED
BUTTON_PIN = 18  # Chân GPIO cho nút nhấn Start/Stop
delay = 0.2  # Thời gian delay giữa các bước dịch chuyển LED

running = False  # Trạng thái chạy/dừng của hiệu ứng
button_pressed = False  # Biến kiểm tra trạng thái nút nhấn

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Cấu hình chân GPIO cho các LED
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # Cấu hình chân GPIO cho nút nhấn
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def update_leds(state):
    """
    Cập nhật trạng thái của dãy LED dựa trên giá trị của `state`.
    `state` là một số nguyên 8 bit đại diện cho trạng thái của 8 LED.
    """
    for i in range(8):
        GPIO.output(LED_PINS[i], GPIO.HIGH if state & (1 << i) else GPIO.LOW)

def led_effect():
    """
    Hiệu ứng LED: dịch chuyển 2 bit từ trung tâm ra hai bên, sau đó quay lại.
    """
    pattern = [0b00011000, 0b00100100, 0b01000010, 0b10000001, 0b00000000,
               0b10000001, 0b01000010, 0b00100100, 0b00011000]
    
    for state in pattern:
        update_leds(state)
        time.sleep(delay)

def loop():
    global running
    global button_pressed

    try:
        while True:
            # Kiểm tra trạng thái của nút nhấn
            if GPIO.input(BUTTON_PIN) == GPIO.LOW and not button_pressed:
                button_pressed = True  # Ghi nhận lần nhấn nút
                running = not running  # Chuyển trạng thái start/stop
                if running:
                    print("LED effect started")
                else:
                    print("LED effect stopped")
                    update_leds(0)  # Tắt LED khi dừng
            elif GPIO.input(BUTTON_PIN) == GPIO.HIGH and button_pressed:
                button_pressed = False  # Đặt lại trạng thái nút nhấn

            # Nếu hiệu ứng đang chạy, thực hiện hiệu ứng LED
            if running:
                led_effect()

            time.sleep(0.1)  # Chờ trong thời gian ngắn giữa các lần kiểm tra
    except KeyboardInterrupt:
        pass

def destroy():
    """
    Đặt lại các chân GPIO khi thoát chương trình.
    """
    update_leds(0)  # Tắt toàn bộ LED
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    loop()
    destroy()
