# Phạm Ngọc Hưng
# Thư viện mô phỏng LCD 16x16 giao tiếp I2C
# Cần cài đặt pygame để chạy được
# pip install pygame
import pygame

class LCD1616:
    def __init__(self, width=400, height=250, address=0x27):
        # Khởi tạo Pygame
        pygame.init()
        self.width = width
        self.height = height
        self.address = address
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LCD1616")
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 20)
        self.lines = [""] * 16  # 16 dòng
        self.backlight = True
        self.cursor_visible = False
        self.cursor_position = (0, 0)

        self.clear()

    def clear(self):
        self.lines = [""] * 16  # Đặt lại tất cả các dòng thành rỗng
        self.display()

    def write_string(self, text):
        # Ghi chuỗi vào dòng tiếp theo nếu còn chỗ
        for i in range(16):
            if len(self.lines[i]) == 0:
                self.lines[i] = text[:16]  # Chỉ ghi tối đa 16 ký tự vào mỗi dòng
                break
        self.display()

    def write_char(self, char):
        row, col = self.cursor_position
        if col < 16:
            self.lines[row] = self.lines[row][:col] + char + self.lines[row][col + 1:]
            self.cursor_position = (row, col + 1)
            self.display()

    def set_cursor(self, row, col):
        if row < 16 and col < 16:
            self.cursor_position = (row, col)

    def cursor_on(self):
        self.cursor_visible = True
        self.display()

    def cursor_off(self):
        self.cursor_visible = False
        self.display()

    def backlight_on(self):
        self.backlight = True
        self.display()

    def backlight_off(self):
        self.backlight = False
        self.display()

    def home(self):
        self.cursor_position = (0, 0)
        self.display()

    def display(self):
        self.screen.fill((0, 0, 0))  # Màu nền đen
        for i in range(16):
            text = self.lines[i]
            rendered_text = self.font.render(text, True, (0, 255, 0) if self.backlight else (50, 50, 50))
            # Đặt vị trí hiển thị cho từng dòng
            self.screen.blit(rendered_text, (10, i * 15))  # Mỗi dòng cách nhau 15 pixel

        if self.cursor_visible:
            cursor_x = 10 + self.cursor_position[1] * 15
            cursor_y = self.cursor_position[0] * 15
            pygame.draw.line(self.screen, (255, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 15), 2)

        pygame.display.flip()

    def close(self):
        pygame.quit()

# Ví dụ sử dụng lớp LCD1616
if __name__ == "__main__":
    lcd = LCD1616()

    try:
        # Ví dụ ghi chuỗi vào màn hình
        lcd.write_string("Hello, World!")
        lcd.set_cursor(1, 0)
        lcd.write_string("LCD 16x16 Test")
        
        # Đợi 5 giây để xem kết quả
        pygame.time.delay(5000)
    finally:
        lcd.close()