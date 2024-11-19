from tkinter import *

root = Tk()  # Tạo cửa sổ chínhr
root.geometry("820x700")  # Thiết lập kích thước cửa sổ
root.title("2 player mode")  # Tên của cửa sổ 

# Tạo khung chung để chứa frame3, frame1 và frame4
frame_container = Frame(root)
frame_container.pack(pady=10, fill="x")  # Cho frame_container trải rộng theo chiều ngang

# Tạo khung chứa nút thoát ở bên trái
frame3 = Frame(frame_container)
frame3.pack(side=LEFT, padx=(50, 10))  # Căn trái với một khoảng cách nhất định

button_out = Button(frame3, text="Exit", font=("Arial", 20), bg="orange", width=8, command=root.quit)
button_out.pack()

# Tạo khung chứa tiêu đề ở giữa
frame1 = Frame(frame_container)
frame1.pack(side=LEFT, expand=True)  # Đặt frame1 ở giữa và cho phép mở rộng

titleLabel = Label(frame1, text="Chơi Vui Vẻ", font=("Arial", 26), bg="orange", width=16)
titleLabel.pack()

game_over = False  # Biến để kiểm tra trạng thái của trò chơi

# Khởi tạo bàn cờ 18*18
board_size = 18
board = {i: " " for i in range(1, board_size**2 + 1)}

# Hàm kiểm tra điều kiện thắng khi có 5 ô liên tiếp
def checkForWin(player):
    # Kiểm tra hàng ngang
    for i in range(board_size):
        for j in range(board_size - 4):  # Chỉ cần kiểm tra đến ô thứ 6 của mỗi hàng
            # Kiểm tra chính xác 5 ô liên tiếp có ký hiệu giống nhau
            if all(board[i * board_size + j + k + 1] == player for k in range(5)):
                # Đảm bảo không có ký hiệu tiếp tục ngay trước hoặc sau dãy 5 ô
                if (j == 0 or board[i * board_size + j] != player) and \
                   (j + 5 == board_size or board[i * board_size + j + 5 + 1] != player):
                    return True

    # Kiểm tra hàng dọc
    for i in range(board_size - 4):  # Chỉ cần kiểm tra đến hàng thứ 6
        for j in range(board_size):
            # Kiểm tra chính xác 5 ô liên tiếp có ký hiệu giống nhau
            if all(board[(i + k) * board_size + j + 1] == player for k in range(5)):
                if (i == 0 or board[(i - 1) * board_size + j + 1] != player) and \
                   (i + 5 == board_size or board[(i + 5) * board_size + j + 1] != player):
                    return True

    # Kiểm tra đường chéo từ trái sang phải
    for i in range(board_size - 4):
        for j in range(board_size - 4):
            # Kiểm tra chính xác 5 ô liên tiếp có ký hiệu giống nhau
            if all(board[(i + k) * board_size + j + k + 1] == player for k in range(5)):
                if (i == 0 or j == 0 or board[(i - 1) * board_size + j - 1 + 1] != player) and \
                   (i + 5 == board_size or j + 5 == board_size or board[(i + 5) * board_size + j + 5 + 1] != player):
                    return True

    # Kiểm tra đường chéo từ phải sang trái
    for i in range(board_size - 4):
        for j in range(4, board_size):
            # Kiểm tra chính xác 5 ô liên tiếp có ký hiệu giống nhau
            if all(board[(i + k) * board_size + j - k + 1] == player for k in range(5)):
                if (i == 0 or j == board_size - 1 or board[(i - 1) * board_size + j + 1] != player) and \
                   (i + 5 == board_size or j - 5 == -1 or board[(i + 5) * board_size + j - 5 + 1] != player):
                    return True

    return False
#hàm kiểm tra hòa
def checkForDraw():
    return all(value != " " for value in board.values())

#hàm restart game
def restartGame():
    global game_over, turn
    game_over = False
    turn = "x"
    titleLabel.config(text="Chơi Vui Vẻ")  # Đặt lại tiêu đề mặc định
    
    # Xóa nội dung của từng ô và đặt lại trạng thái bàn cờ
    for button in buttons:
        button["text"] = " "
    
    for i in board.keys():
        board[i] = " "
# Biến lưu lượt chơi
turn = "x"

# Hàm xử lý khi nhấp vào ô
def play(event, index):
    global turn, game_over  # Phải có câu lệnh này mới có thể click chuột trái hiện x và o
    if game_over:
        return  # Nếu game_over là True, không cho phép thêm "X" hoặc "O"
    
    button = event.widget

    # Tránh đánh dấu lại các ô đã có X và O
    if button["text"] == " ":
        if turn == "x":
            button["text"] = "X"
            button["fg"] = "red"  # Làm cho X có màu đỏ khi là turn x
            board[index] = turn   #CẦN XEM LẠI
             # Kiểm tra điều kiện thắng sau mỗi lần đánh
            if checkForWin(turn):
                 winLabel = Label(titleLabel, text=f"{turn} đã chiến thắng!", font=("Arial", 26), fg="green", bg="yellow")
                 winLabel.pack()  #hien thi
                 game_over = True # Đặt game_over thành True khi có người thắng
                 return
            turn = "O" # Chuyển sang lượt O
        else:
            button["text"] = "O"
            button["fg"] = "blue"  # Làm cho O có màu xanh khi là turn o
            board[index] = turn
             # Kiểm tra điều kiện thắng sau mỗi lần đánh
            if checkForWin(turn):
                winLabel = Label(titleLabel, text=f"{turn} đã chiến thắng!", font=("Arial", 26), fg="green", bg="yellow")
                winLabel.pack() #hien thi
                game_over = True  # Đặt game_over thành True khi có người thắng
                return
            turn = "x"  # Chuyển lượt sang X

# Kiểm tra trò chơi hòa sau khi hoàn tất lượt đi
        if checkForDraw():
            drawLabel = Label(titleLabel, text="Game Draw", font=("Arial", 26), fg="green", bg="yellow")
            drawLabel.pack()


# Tạo khung chứa các ô
frame2 = Frame(root, bg="white")
frame2.pack()
buttons = []

# Tạo các ô và gán sự kiện nhấp chuột cho từng ô
for i in range(board_size):
    for j in range(board_size):
        index = i * board_size + j + 1  # Tính chỉ số duy nhất cho từng ô
        button = Button(frame2, text=" ", width=3, height=1, font=("Arial", 16), bg="white", relief=RAISED, borderwidth=1)
        button.grid(row=i, column=j)
        button.bind("<Button-1>", lambda event, idx=index: play(event, idx))  # Truyền chỉ số ô vào hàm play
        buttons.append(button)


# Tạo khung chứa nút Restart ở bên phải
frame4 = Frame(frame_container)
frame4.pack(side=LEFT, padx=(10, 50))  # Đặt khoảng cách với frame1
# Nút Restart được liên kết với hàm restartGame
button_restart = Button(frame4, text="Restart", font=("Arial", 20), bg="orange", width=8, command = restartGame)
button_restart.pack()


root.mainloop()  # Bắt đầu vòng lặp chính của ứng dụng





