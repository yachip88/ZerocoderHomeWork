"""Логика игры «Кто хочет стать миллионером».

Отдельный модуль без Tkinter: вопросы, уровни, несгораемые суммы и подсказки.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path

# Шкала выигрыша: 15 ступеней. Несгораемые суммы — после 5-го и 10-го вопроса.
PRIZES: list[int] = [
    100,
    200,
    300,
    500,
    1_000,  # несгораемая после 5 правильных ответов
    2_000,
    4_000,
    8_000,
    16_000,
    32_000,  # несгораемая после 10 правильных ответов
    64_000,
    125_000,
    250_000,
    500_000,
    1_000_000,
]

SAFE_QUESTION_COUNTS = (5, 10)
LETTERS = ("A", "B", "C", "D")


@dataclass
class Question:
    """Один вопрос викторины из внешнего файла."""

    text: str
    options: list[str]
    correct: int
    difficulty: str

    def letter_of_correct(self) -> str:
        return LETTERS[self.correct]


def load_questions(path: str | Path | None = None) -> list[Question]:
    """Читает questions.json. Новые вопросы добавляются правкой этого файла."""
    if path is None:
        path = Path(__file__).with_name("questions.json")
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data["questions"] if isinstance(data, dict) else data
    questions: list[Question] = []
    for item in items:
        options = list(item["options"])
        if len(options) != 4:
            raise ValueError(f"У вопроса должно быть 4 варианта: {item.get('text')!r}")
        questions.append(
            Question(
                text=str(item["text"]),
                options=options,
                correct=int(item["correct"]),
                difficulty=str(item.get("difficulty", "medium")),
            )
        )
    if len(questions) < 15:
        raise ValueError("Для полной шкалы нужно не меньше 15 вопросов.")
    return questions[:15]


@dataclass
class GameState:
    """Текущая партия: номер вопроса, выигрыш, какие подсказки уже потрачены."""

    questions: list[Question]
    index: int = 0
    finished: bool = False
    won: bool = False
    prize: int = 0
    fifty_used: bool = False
    friend_used: bool = False
    audience_used: bool = False
    hidden_options: set[int] = field(default_factory=set)

    @property
    def current(self) -> Question:
        return self.questions[self.index]

    @property
    def visible_options(self) -> list[int]:
        return [i for i in range(4) if i not in self.hidden_options]

    def safe_prize(self) -> int:
        """Несгораемая сумма по числу уже взятых вопросов (ещё не текущего)."""
        answered = self.index
        if answered >= 10:
            return PRIZES[9]
        if answered >= 5:
            return PRIZES[4]
        return 0

    def answer(self, option_index: int) -> bool:
        """Проверяет ответ. True — верно (и, возможно, победа). False — проигрыш."""
        if self.finished:
            return False
        if option_index not in self.visible_options:
            return False
        if option_index == self.current.correct:
            self.prize = PRIZES[self.index]
            if self.index >= len(self.questions) - 1:
                self.finished = True
                self.won = True
            else:
                self.index += 1
                self.hidden_options.clear()
            return True
        self.prize = self.safe_prize()
        self.finished = True
        self.won = False
        return False

    def use_fifty_fifty(self) -> set[int]:
        """Прячет два неверных варианта. Повторно вызвать нельзя."""
        if self.fifty_used or self.finished:
            return set(self.hidden_options)
        wrong = [i for i in range(4) if i != self.current.correct]
        random.shuffle(wrong)
        self.hidden_options = set(wrong[:2])
        self.fifty_used = True
        return set(self.hidden_options)

    def use_phone_a_friend(self) -> int:
        """С вероятностью 80% называет верный ответ среди видимых вариантов."""
        if self.friend_used or self.finished:
            return self.current.correct
        self.friend_used = True
        visible = self.visible_options
        correct = self.current.correct
        if random.random() < 0.8 and correct in visible:
            return correct
        others = [i for i in visible if i != correct]
        return random.choice(others) if others else correct

    def use_audience(self) -> dict[int, int]:
        """Псевдографик зала: проценты по видимым кнопкам, сумма 100%."""
        if self.audience_used or self.finished:
            return {}
        self.audience_used = True
        visible = self.visible_options
        correct = self.current.correct
        # Верный вариант чаще всего получает наибольшую долю голосов.
        weights: dict[int, float] = {}
        for idx in visible:
            if idx == correct:
                weights[idx] = random.uniform(0.42, 0.72)
            else:
                weights[idx] = random.uniform(0.05, 0.28)
        total = sum(weights.values()) or 1.0
        percents = {idx: int(round(100 * weights[idx] / total)) for idx in visible}
        drift = 100 - sum(percents.values())
        percents[visible[0]] += drift
        for idx in range(4):
            percents.setdefault(idx, 0)
        return percents


def format_money(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " ₽"
