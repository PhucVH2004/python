import sys
import os
import pygame as pg
from UI import Button
import subprocess

# Khởi tạo Pygame và font
pg.init()
pg.font.init()  # Đảm bảo font được khởi tạo

# Cấu hình đầu ra để in Unicode trên Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Thiết lập độ phân giải và các thông số giao diện
RESOLUTION = WIDTH, HEIGHT = 1280, 720
surface = pg.display.set_mode(RESOLUTION)
pg.display.set_caption("Game caro")

BGCOLOR = "#1B1F66"

# Khởi tạo các nút giao diện
buttons = [
    Button(surface, (WIDTH // 2, 200), "Chơi với máy"),  # Nút "Play with BOT"
    Button(surface, (WIDTH // 2, 350), "2 player mode"),
    Button(surface, (WIDTH // 2, 500), "play online"),
]

def update():
    for button in buttons:
        button.update()

def draw():
    surface.fill(BGCOLOR)  # Màu nền của giao diện chính
    for button in buttons:
        button.draw()  # Vẽ các nút

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if e.type == pg.MOUSEBUTTONDOWN:
            # Kiểm tra nếu nhấn nút "Play with BOT"
            if buttons[0].is_clicked(e.pos):  # `buttons[0]` là nút "Play with BOT"
                # Xác định đường dẫn đến file AI.py
                script_path = os.path.join(os.path.dirname(__file__), '..', 'main','play_with_BOT','AI.py')
                # Kiểm tra nếu file tồn tại trước khi thực thi
                if os.path.isfile(script_path):
                    # Chạy file AI.py
                    subprocess.run([sys.executable, script_path])
                else:
                    print(f"File AI.py không tồn tại tại: {script_path}")
            if buttons[1].is_clicked(e.pos):  # `buttons[0]` là nút "Play with BOT"
                # Xác định đường dẫn đến file AI.py
                script_path = os.path.join(os.path.dirname(__file__), '..', 'main','2_player_mode','2p.py')
                # Kiểm tra nếu file tồn tại trước khi thực thi
                if os.path.isfile(script_path):
                    # Chạy file AI.py
                    subprocess.run([sys.executable, script_path])
                else:
                    print(f"File AI.py không tồn tại tại: {script_path}")
       


    update()  # Cập nhật các thành phần giao diện
    draw()  # Vẽ lại giao diện

    pg.display.flip()  # Cập nhật màn hình
