import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("360x550")
window.resizable(False, False)

buttons = []
current_player = "X"
player_symbol = "X"
computer_symbol = "O"
score_x = 0
score_o = 0
game_over = False


def update_status():
    status_label.config(text=f"Ход игрока: {current_player}")
    score_label.config(text=f"Счёт  X: {score_x}   O: {score_o}")


def reset_board():
    global current_player, game_over
    for i in range(3):
        for j in range(3):
            buttons[i][j]["text"] = ""
            buttons[i][j]["state"] = "normal"
            buttons[i][j]["bg"] = "white"

    current_player = player_symbol
    game_over = False
    update_status()


def full_reset():
    global score_x, score_o
    score_x = 0
    score_o = 0
    reset_board()


def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return [(i, 0), (i, 1), (i, 2)]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return [(0, i), (1, i), (2, i)]

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return [(0, 0), (1, 1), (2, 2)]

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return [(0, 2), (1, 1), (2, 0)]

    return None


def check_draw():
    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                return False
    return True


def disable_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j]["state"] = "disabled"


def on_click(row, col):
    global current_player, score_x, score_o, game_over

    if game_over:
        return

    if buttons[row][col]["text"] != "":
        return

    buttons[row][col]["text"] = current_player

    winner_cells = check_winner()
    if winner_cells:
        game_over = True
        for r, c in winner_cells:
            buttons[r][c]["bg"] = "lightgreen"

        if current_player == "X":
            score_x += 1
        else:
            score_o += 1

        update_status()
        disable_board()

        if score_x == 3 or score_o == 3:
            messagebox.showinfo("Матч окончен", f"Игрок {current_player} победил в матче до 3 побед!")
            full_reset()
            return
        else:
            messagebox.showinfo("Игра окончена", f"Игрок {current_player} победил!")
            return

    if check_draw():
        game_over = True
        update_status()
        messagebox.showinfo("Игра окончена", "Ничья!")
        return

    current_player = "O" if current_player == "X" else "X"
    update_status()


def set_symbol(symbol):
    global player_symbol, computer_symbol, current_player
    player_symbol = symbol
    computer_symbol = "O" if symbol == "X" else "X"
    current_player = player_symbol
    reset_board()


title_label = tk.Label(window, text="Крестики-нолики", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

status_label = tk.Label(window, text="", font=("Arial", 12))
status_label.pack()

score_label = tk.Label(window, text="", font=("Arial", 12, "bold"))
score_label.pack(pady=5)

choice_frame = tk.Frame(window)
choice_frame.pack(pady=10)

tk.Label(choice_frame, text="Выбери символ:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
tk.Button(choice_frame, text="X", width=5, command=lambda: set_symbol("X")).grid(row=0, column=1, padx=5)
tk.Button(choice_frame, text="O", width=5, command=lambda: set_symbol("O")).grid(row=0, column=2, padx=5)

board_frame = tk.Frame(window)
board_frame.pack(pady=10)

for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(
            board_frame,
            text="",
            font=("Arial", 20, "bold"),
            width=5,
            height=2,
            bg="white",
            command=lambda r=i, c=j: on_click(r, c)
        )
        btn.grid(row=i, column=j, padx=3, pady=3)
        row.append(btn)
    buttons.append(row)

control_frame = tk.Frame(window)
control_frame.pack(pady=15)

tk.Button(control_frame, text="Сброс поля", width=12, command=reset_board).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="Сброс всего", width=12, command=full_reset).grid(row=0, column=1, padx=5)

update_status()
window.mainloop()