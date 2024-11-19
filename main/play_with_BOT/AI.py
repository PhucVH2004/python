from tkinter import *

root = Tk()
root.geometry("820x700")
root.title("Player vs Advanced AI")

board_size = 18
board = {i: " " for i in range(1, board_size**2 + 1)}
turn = "X"
game_over = False

# Kiểm tra chiến thắng
def checkForWin(player):
    for i in range(board_size):
        for j in range(board_size - 4):
            if all(board[i * board_size + j + k + 1] == player for k in range(5)):
                return True
    for i in range(board_size - 4):
        for j in range(board_size):
            if all(board[(i + k) * board_size + j + 1] == player for k in range(5)):
                return True
    for i in range(board_size - 4):
        for j in range(board_size - 4):
            if all(board[(i + k) * board_size + j + k + 1] == player for k in range(5)):
                return True
    for i in range(board_size - 4):
        for j in range(4, board_size):
            if all(board[(i + k) * board_size + j - k + 1] == player for k in range(5)):
                return True
    return False

# Kiểm tra hòa
def checkForDraw():
    return all(value != " " for value in board.values())

# Khởi động lại trò chơi
def restartGame():
    global game_over, turn
    game_over = False
    turn = "X"
    titleLabel.config(text="Chơi Vui Vẻ")
    for button in buttons:
        button["text"] = " "
    for i in board.keys():
        board[i] = " "

# Hàm kiểm tra điểm nước đi dựa trên chuỗi
def evaluate_move(index, player):
    score = 0
    row, col = (index - 1) // board_size, (index - 1) % board_size

    # Các hướng kiểm tra chuỗi
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal up-right
    ]

    for d in directions:
        count = 1
        
        # Kiểm tra chuỗi quân cùng hướng
        for i in range(1, 5):
            r, c = row + i * d[0], col + i * d[1]
            if r >= board_size or c >= board_size or c < 0 or board.get(r * board_size + c + 1) != player:
                break
            count += 1
        
        # Kiểm tra chuỗi ngược hướng
        for i in range(1, 5):
            r, c = row - i * d[0], col - i * d[1]
            if r < 0 or c < 0 or c >= board_size or board.get(r * board_size + c + 1) != player:
                break
            count += 1
        
        # Tính điểm cho chuỗi với quân "mở" hai đầu
        if count == 5:
            score += 100000  # Điểm cao nhất nếu có chuỗi thắng
        elif count == 4:
            score += 1000
        elif count == 3:
            score += 100
        elif count == 2:
            score += 10
        elif count == 1:
            score += 1
            
    return score

# AI lựa chọn nước đi
def ai_move():
    best_move, best_score = None, -float('inf')

    for move in board.keys():
        if board[move] == " ":
            # Đánh giá điểm phòng thủ và tấn công
            board[move] = "O"
            attack_score = evaluate_move(move, "O")
            board[move] = "X"
            defense_score = evaluate_move(move, "X")
            board[move] = " "
            
            # Tính điểm tổng và tìm nước đi tốt nhất
            score = max(attack_score, defense_score)
            if score > best_score:
                best_score, best_move = score, move

    return best_move

# Thực hiện nước đi
def makeMove(index, player):
    global game_over
    if board[index] == " " and not game_over:
        board[index] = player
        buttons[index - 1]["text"] = player
        buttons[index - 1]["fg"] = "red" if player == "X" else "blue"
        
        if checkForWin(player):
            titleLabel.config(text=f"{player} đã chiến thắng!", fg="green", bg="yellow")
            game_over = True
        elif checkForDraw():
            titleLabel.config(text="Game Draw", fg="green", bg="yellow")
            game_over = True

# Khi người chơi nhấp vào ô
def play(event, index):
    global turn, game_over
    if game_over:
        return
    button = event.widget
    if button["text"] == " ":
        makeMove(index, "X")  # Người chơi đi
        turn = "O"
        
        if not game_over:
            ai_move_index = ai_move()
            if ai_move_index:
                makeMove(ai_move_index, "O")
                turn = "X"

# Giao diện chính
frame_container = Frame(root)
frame_container.pack(pady=10, fill="x")

frame3 = Frame(frame_container)
frame3.pack(side=LEFT, padx=(50, 10))
button_out = Button(frame3, text="Exit", font=("Arial", 20), bg="orange", width=8, command=root.quit)
button_out.pack()

frame1 = Frame(frame_container)
frame1.pack(side=LEFT, expand=True)
titleLabel = Label(frame1, text="Chơi Vui Vẻ", font=("Arial", 26), bg="orange", width=16)
titleLabel.pack()

frame4 = Frame(frame_container)
frame4.pack(side=LEFT, padx=(10, 50))
button_restart = Button(frame4, text="Restart", font=("Arial", 20), bg="orange", width=8, command=restartGame)
button_restart.pack()

frame2 = Frame(root, bg="white")
frame2.pack()
buttons = []

for i in range(board_size):
    for j in range(board_size):
        index = i * board_size + j + 1
        button = Button(frame2, text=" ", width=3, height=1, font=("Arial", 16), bg="white", relief=RAISED, borderwidth=1)
        button.grid(row=i, column=j)
        button.bind("<Button-1>", lambda event, idx=index: play(event, idx))
        buttons.append(button)

root.mainloop()
