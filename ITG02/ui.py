"""Графический интерфейс на Tkinter: меню, игровая доска, победа и поражение."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from game_logic import (
    LETTERS,
    PRIZES,
    GameState,
    format_money,
    load_questions,
)

BG = "#071433"
PANEL = "#0c1f4d"
GOLD = "#e6c35c"
WHITE = "#f4f1e8"
MUTED = "#9aa7c7"
CORRECT = "#1f8a4c"
WRONG = "#b33939"
BTN = "#163a8a"
BTN_HOVER = "#1f4cb3"
DISABLED = "#3a4566"


class MillionaireApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Кто хочет стать миллионером")
        self.root.geometry("980x640")
        self.root.minsize(900, 580)
        self.root.configure(bg=BG)
        self.state: GameState | None = None
        self.answer_buttons: list[tk.Button] = []
        self.ladder_labels: list[tk.Label] = []
        self._build()
        self.show_menu()

    def _build(self) -> None:
        self.menu_frame = tk.Frame(self.root, bg=BG)
        self.game_frame = tk.Frame(self.root, bg=BG)
        self.result_frame = tk.Frame(self.root, bg=BG)
        self._build_menu()
        self._build_game()
        self._build_result()

    def _hide_all(self) -> None:
        for frame in (self.menu_frame, self.game_frame, self.result_frame):
            frame.pack_forget()

    def show_menu(self) -> None:
        self._hide_all()
        self.menu_frame.pack(fill="both", expand=True)

    def _build_menu(self) -> None:
        box = tk.Frame(self.menu_frame, bg=BG)
        box.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            box,
            text="КТО ХОЧЕТ СТАТЬ\nМИЛЛИОНЕРОМ",
            font=("Segoe UI", 28, "bold"),
            fg=GOLD,
            bg=BG,
            justify="center",
        ).pack(pady=(0, 12))
        tk.Label(
            box,
            text="15 вопросов · 3 подсказки · несгораемые суммы",
            font=("Segoe UI", 12),
            fg=MUTED,
            bg=BG,
        ).pack(pady=(0, 28))
        self._menu_button(box, "Играть", self.start_game).pack(pady=8)
        self._menu_button(box, "Выход", self.root.destroy).pack(pady=8)

    def _menu_button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 16, "bold"),
            fg=BG,
            bg=GOLD,
            activebackground="#f0d67a",
            activeforeground=BG,
            relief="flat",
            width=18,
            cursor="hand2",
        )
        return btn

    def _build_game(self) -> None:
        top = tk.Frame(self.game_frame, bg=BG)
        top.pack(fill="x", padx=16, pady=10)
        self.hint_fifty = self._hint_button(top, "50:50", self.on_fifty)
        self.hint_friend = self._hint_button(top, "Звонок другу", self.on_friend)
        self.hint_audience = self._hint_button(top, "Помощь зала", self.on_audience)
        self.hint_fifty.pack(side="left", padx=6)
        self.hint_friend.pack(side="left", padx=6)
        self.hint_audience.pack(side="left", padx=6)

        body = tk.Frame(self.game_frame, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=4)

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        self.question_label = tk.Label(
            left,
            text="",
            wraplength=620,
            justify="center",
            font=("Segoe UI", 18, "bold"),
            fg=WHITE,
            bg=PANEL,
            padx=20,
            pady=24,
        )
        self.question_label.pack(fill="x", pady=(8, 20))

        grid = tk.Frame(left, bg=BG)
        grid.pack(fill="x")
        self.answer_buttons = []
        for i in range(4):
            row, col = divmod(i, 2)
            btn = tk.Button(
                grid,
                text="",
                font=("Segoe UI", 13),
                fg=WHITE,
                bg=BTN,
                activebackground=BTN_HOVER,
                activeforeground=WHITE,
                relief="flat",
                anchor="w",
                padx=14,
                pady=12,
                wraplength=280,
                justify="left",
                command=lambda idx=i: self.on_answer(idx),
            )
            btn.grid(row=row, column=col, sticky="ew", padx=6, pady=6)
            self.answer_buttons.append(btn)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        self.status_label = tk.Label(
            left,
            text="",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=BG,
        )
        self.status_label.pack(pady=12)

        ladder = tk.Frame(body, bg=PANEL, padx=10, pady=10)
        ladder.pack(side="right", fill="y", padx=(12, 0))
        tk.Label(
            ladder,
            text="Выигрыш",
            font=("Segoe UI", 11, "bold"),
            fg=GOLD,
            bg=PANEL,
        ).pack(pady=(0, 6))
        self.ladder_labels = []
        # Сверху — миллион, снизу — первая ступень.
        for i, amount in reversed(list(enumerate(PRIZES))):
            label = tk.Label(
                ladder,
                text=f"{i + 1:2d}  {format_money(amount)}",
                font=("Consolas", 11),
                fg=GOLD if i + 1 in (5, 10, 15) else WHITE,
                bg=PANEL,
                anchor="w",
                width=18,
            )
            label.pack(anchor="w")
            self.ladder_labels.append(label)

    def _hint_button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            fg=BG,
            bg=GOLD,
            activebackground="#f0d67a",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        )

    def _build_result(self) -> None:
        box = tk.Frame(self.result_frame, bg=BG)
        box.place(relx=0.5, rely=0.5, anchor="center")
        self.result_title = tk.Label(
            box,
            text="",
            font=("Segoe UI", 26, "bold"),
            fg=GOLD,
            bg=BG,
        )
        self.result_title.pack(pady=(0, 10))
        self.result_sum = tk.Label(
            box,
            text="",
            font=("Segoe UI", 18),
            fg=WHITE,
            bg=BG,
        )
        self.result_sum.pack(pady=(0, 24))
        self._menu_button(box, "Сыграть ещё раз", self.start_game).pack(pady=8)
        self._menu_button(box, "В меню", self.show_menu).pack(pady=8)

    def start_game(self) -> None:
        self.state = GameState(questions=load_questions())
        self._hide_all()
        self.game_frame.pack(fill="both", expand=True)
        self.refresh_board()

    def refresh_board(self) -> None:
        state = self.state
        if state is None:
            return
        question = state.current
        self.question_label.config(text=f"Вопрос {state.index + 1} из 15\n\n{question.text}")
        for i, btn in enumerate(self.answer_buttons):
            hidden = i in state.hidden_options
            btn.config(
                text="" if hidden else f"{LETTERS[i]})  {question.options[i]}",
                state="disabled" if hidden else "normal",
                bg=DISABLED if hidden else BTN,
                fg=MUTED if hidden else WHITE,
            )
        self.hint_fifty.config(state="disabled" if state.fifty_used else "normal")
        self.hint_friend.config(state="disabled" if state.friend_used else "normal")
        self.hint_audience.config(state="disabled" if state.audience_used else "normal")
        self.status_label.config(
            text=f"Сейчас на кону: {format_money(PRIZES[state.index])}  ·  "
            f"несгораемая сумма: {format_money(state.safe_prize())}"
        )
        # ladder_labels[0] — миллион (индекс 14), ladder_labels[14] — 100 ₽.
        for visual_i, label in enumerate(self.ladder_labels):
            prize_index = 14 - visual_i
            if prize_index == state.index:
                label.config(bg=GOLD, fg=BG)
            else:
                fg = GOLD if prize_index + 1 in (5, 10, 15) else WHITE
                label.config(bg=PANEL, fg=fg)

    def on_answer(self, option_index: int) -> None:
        state = self.state
        if state is None or state.finished:
            return
        correct = state.current.correct
        ok = state.answer(option_index)
        if ok and not state.finished:
            messagebox.showinfo("Верно!", "Отличный ответ. Переходим к следующему вопросу.")
            self.refresh_board()
            return
        if ok and state.won:
            self.show_result(True, state.prize)
            return
        # Подсветка своего и верного вариантов перед окном поражения.
        self.answer_buttons[option_index].config(bg=WRONG)
        self.answer_buttons[correct].config(bg=CORRECT, state="normal")
        self.root.after(700, lambda: self.show_result(False, state.prize))

    def show_result(self, won: bool, prize: int) -> None:
        self._hide_all()
        self.result_frame.pack(fill="both", expand=True)
        if won:
            self.result_title.config(text="Победа!")
            self.result_sum.config(text=f"Вы выиграли {format_money(prize)}")
        else:
            self.result_title.config(text="Игра окончена")
            self.result_sum.config(text=f"Ваш выигрыш: {format_money(prize)}")

    def on_fifty(self) -> None:
        if self.state is None:
            return
        self.state.use_fifty_fifty()
        self.refresh_board()

    def on_friend(self) -> None:
        if self.state is None:
            return
        idx = self.state.use_phone_a_friend()
        question = self.state.current
        messagebox.showinfo(
            "Звонок другу",
            f"Друг считает, что правильный ответ: "
            f"{LETTERS[idx]}) {question.options[idx]}",
        )
        self.refresh_board()

    def on_audience(self) -> None:
        if self.state is None:
            return
        votes = self.state.use_audience()
        if not votes:
            return
        win = tk.Toplevel(self.root)
        win.title("Помощь зала")
        win.configure(bg=BG)
        win.geometry("420x280")
        tk.Label(
            win,
            text="Голосование зала",
            font=("Segoe UI", 14, "bold"),
            fg=GOLD,
            bg=BG,
        ).pack(pady=8)
        canvas = tk.Canvas(win, width=380, height=200, bg=PANEL, highlightthickness=0)
        canvas.pack(padx=16, pady=8)
        max_w = 280
        visible = list(self.state.visible_options) if self.state is not None else list(range(4))
        for row, i in enumerate(visible):
            y = 20 + row * 45
            pct = votes.get(i, 0)
            letter = LETTERS[i]
            canvas.create_text(24, y + 10, text=letter, fill=GOLD, font=("Segoe UI", 12, "bold"))
            canvas.create_rectangle(50, y, 50 + int(max_w * pct / 100), y + 22, fill=GOLD, outline="")
            canvas.create_text(50 + max_w + 18, y + 10, text=f"{pct}%", fill=WHITE, font=("Segoe UI", 11))
        self.refresh_board()


def run_app() -> None:
    root = tk.Tk()
    MillionaireApp(root)
    root.mainloop()
