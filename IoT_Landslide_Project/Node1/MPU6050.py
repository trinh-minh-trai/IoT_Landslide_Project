# from smbus2 import SMBus
import random

class MPU6050:
    # def __init__(self, sda_pin, scl_pin):
    #     self.sda_pin = sda_pin
    #     self.scl_pin = scl_pin
    #     self.bus = SMBus(1)  # Bus I2C thường là 1 trên Raspberry Pi
    #     self.address = 0x68  # Địa chỉ I2C mặc định của MPU6050
    def __init__(self):
        pass
    
    def get_accel_gyro(self):
        # Giả lập việc đọc dữ liệu từ MPU6050 qua bus I2C
        # (ở đây bạn có thể sử dụng mô phỏng của bạn để lấy dữ liệu ngẫu nhiên)
        accel_x = random.uniform(-10, 10)
        accel_y = random.uniform(-10, 10)
        accel_z = random.uniform(-10, 10)
        gyro_x = random.uniform(-180, 180)
        gyro_y = random.uniform(-180, 180)
        gyro_z = random.uniform(-180, 180)
        
        return {
            "accel_x": round(accel_x, 2), 
            "accel_y": round(accel_y, 2), 
            "accel_z": round(accel_z, 2),
            "gyro_x": round(gyro_x, 2), 
            "gyro_y": round(gyro_y, 2), 
            "gyro_z": round(gyro_z, 2)
        }