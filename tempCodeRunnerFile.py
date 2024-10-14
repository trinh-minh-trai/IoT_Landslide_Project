import threading
import random
from EmulatorGUI import GPIO
import time

DHT_PIN = 4
BUTTON_START_PIN = 24
BUTTON_STOP_PIN = 23
LED_PIN = 16  
SENSOR_70_PIN = 27  
SENSOR_50_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SENSOR_70_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_50_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


count_70 = 0
count_50 = 0
running = False


last_update_time = time.monotonic()
last_led_blink_time = time.monotonic()
led_state = False


def read_dht22():
    temperature = random.uniform(20, 30)  
    humidity = random.uniform(40, 60)  
    return humidity, temperature

def display_info(temp, humidity):
    print(f"Temperature: {temp:.1f}°C, Humidity: {humidity:.1f}%")
    print(f"70g Count: {count_70}, 50g Count: {count_50}")

def blink_led():
    global led_state
    while True:
        if running:
            current_time = time.monotonic()
            if current_time - last_led_blink_time >= 0.5:
                led_state = not led_state
                GPIO.output(LED_PIN, led_state)
                last_led_blink_time = current_time

try:

    threading.Thread(target=blink_led, daemon=True).start()

    while True:
        current_time = time.monotonic()

 
        if current_time - last_update_time >= 3:
            humidity, temperature = read_dht22()
            display_info(temperature, humidity)
            last_update_time = current_time


        if GPIO.input(BUTTON_START_PIN) == GPIO.LOW:
            running = True
            print("System Started.")


        if GPIO.input(BUTTON_STOP_PIN) == GPIO.LOW:
            running = False
            print("System Stopped.")

   
        if running:
            if GPIO.input(SENSOR_70_PIN) == GPIO.LOW:
                count_70 += 1
                print("70g Product Detected.")
                while GPIO.input(SENSOR_70_PIN) == GPIO.LOW:
                    pass
           
            if GPIO.input(SENSOR_50_PIN) == GPIO.LOW:
                count_50 += 1
                print("50g Product Detected.")
                while GPIO.input(SENSOR_50_PIN) == GPIO.LOW:
                    pass

except KeyboardInterrupt:
    print("Program stopped.")
finally:
    GPIO.cleanup()