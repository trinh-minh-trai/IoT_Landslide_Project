import random

class MPU6050:
    def __init__(self):
        pass

    def get_accel_gyro(self):
        # Giả lập dữ liệu gia tốc và con quay hồi chuyển bằng random
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
