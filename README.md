Dự án này phát triển một hệ thống cảnh báo sớm sạt lở đất sử dụng các cảm biến IoT và máy học để dự đoán nguy cơ xảy ra sạt lở. Hệ thống được triển khai trên Raspberry Pi 4, 
thu thập dữ liệu từ nhiều loại cảm biến khác nhau để theo dõi các yếu tố môi trường và địa chất, sau đó gửi dữ liệu lên nền tảng ThingSpeak để phân tích và đưa ra các cảnh báo.

Các cảm biến được sử dụng:
DHT22: Đo nhiệt độ và độ ẩm không khí.
Cảm biến độ ẩm đất: Đo mức độ ẩm trong đất.
MPU6050: Cảm biến gia tốc và con quay hồi chuyển để theo dõi sự thay đổi góc nghiêng và rung động của mặt đất.
Cảm biến siêu âm: Đo khoảng cách để theo dõi sự thay đổi địa hình.
Cảm biến rung SW-420: Phát hiện các rung động mạnh có thể dẫn đến sạt lở.
