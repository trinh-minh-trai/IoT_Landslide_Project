class lcd:
    def __init__(self):
        # Khởi tạo màn hình LCD với hai dòng
        self.lcd_lines = ["", ""]

    def lcd_clear(self):
        # Xóa màn hình LCD
        self.lcd_lines = ["", ""]
        print("LCD Cleared")

    def lcd_display_string(self, string, line, pos=0):
        # Hiển thị chuỗi lên dòng 1 hoặc 2
        if line == 1:
            self.lcd_lines[0] = string
        elif line == 2:
            self.lcd_lines[1] = string

        # Mô phỏng việc hiển thị nội dung lên màn hình
        self.display()

    def display(self):
        # Hiển thị nội dung giả lập của màn hình LCD trong terminal
        print(f"LCD Line 1: {self.lcd_lines[0]}")
        print(f"LCD Line 2: {self.lcd_lines[1]}")
