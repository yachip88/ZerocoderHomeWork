"""Логика игры «Кто хочет стать миллионером».

Отдельный модуль без Tkinter: вопросы, уровни, несгораемые суммы и подсказки.
"""

from __future__ import annotations

import json
import random
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

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
KNOWN_DIFFICULTIES = ("easy", "medium", "hard")
QUESTIONS_PER_DIFFICULTY = 5
REQUIRED_FIELDS = ("text", "options", "correct", "difficulty")


class QuestionError(ValueError):
    """Ошибка в файле вопросов: игра не должна молча зависать."""


@dataclass
class Question:
    """Один вопрос викторины из внешнего файла."""

    text: str
    options: list[str]
    correct: int
    difficulty: str

    def letter_of_correct(self) -> str:
        return LETTERS[self.correct]


def shuffle_options(
    question: Question, rng: random.Random | None = None
) -> Question:
    """Перемешивает варианты ответа и синхронизирует индекс correct."""
    mixer = rng if rng is not None else random.Random()
    order = list(range(len(question.options)))
    mixer.shuffle(order)
    return Question(
        text=question.text,
        options=[question.options[i] for i in order],
        correct=order.index(question.correct),
        difficulty=question.difficulty,
    )


def _parse_question(item: object, index: int) -> Question:
    if not isinstance(item, dict):
        raise QuestionError(f"Вопрос #{index + 1} должен быть объектом JSON.")
    missing = [name for name in REQUIRED_FIELDS if name not in item]
    if missing:
        raise QuestionError(
            f"Вопрос #{index + 1}: нет обязательных полей: {', '.join(missing)}."
        )
    options = item["options"]
    if not isinstance(options, list) or len(options) != 4:
        raise QuestionError(
            f"Вопрос #{index + 1}: должно быть ровно 4 варианта ответа."
        )
    options = [str(option) for option in options]
    correct = item["correct"]
    if isinstance(correct, bool) or not isinstance(correct, int):
        raise QuestionError(
            f"Вопрос #{index + 1}: поле correct должно быть целым числом от 0 до 3."
        )
    if not 0 <= correct <= 3:
        raise QuestionError(
            f"Вопрос #{index + 1}: поле correct должно быть от 0 до 3, получено {correct}."
        )
    difficulty = str(item["difficulty"]).strip().lower()
    if difficulty not in KNOWN_DIFFICULTIES:
        raise QuestionError(
            f"Вопрос #{index + 1}: неизвестный уровень {item['difficulty']!r}. "
            f"Допустимы: {', '.join(KNOWN_DIFFICULTIES)}."
        )
    return Question(
        text=str(item["text"]),
        options=options,
        correct=correct,
        difficulty=difficulty,
    )


def load_questions(path: str | Path | None = None) -> list[Question]:
    """Читает и проверяет questions.json целиком, без обрезки до первых 15."""
    if path is None:
        path = Path(__file__).with_name("questions.json")
    path = Path(path)
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except FileNotFoundError as exc:
        raise QuestionError(f"Файл вопросов не найден: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QuestionError(f"Некорректный JSON в файле вопросов: {exc}") from exc

    if isinstance(data, dict):
        if "questions" not in data:
            raise QuestionError("В JSON нет ключа 'questions'.")
        items = data["questions"]
    else:
        items = data
    if not isinstance(items, list):
        raise QuestionError("Список вопросов должен быть массивом.")

    questions = [_parse_question(item, index) for index, item in enumerate(items)]
    counts = Counter(question.difficulty for question in questions)
    for difficulty in KNOWN_DIFFICULTIES:
        if counts[difficulty] < QUESTIONS_PER_DIFFICULTY:
            raise QuestionError(
                f"Нужно не меньше {QUESTIONS_PER_DIFFICULTY} вопросов уровня "
                f"{difficulty!r}, есть {counts[difficulty]}."
            )
    return questions


def select_game_questions(
    questions: Sequence[Question],
    *,
    per_difficulty: int = QUESTIONS_PER_DIFFICULTY,
    rng: random.Random | None = None,
) -> list[Question]:
    """Случайно берёт по пять вопросов каждого уровня и перемешивает варианты."""
    mixer = rng if rng is not None else random.Random()
    selected: list[Question] = []
    for difficulty in KNOWN_DIFFICULTIES:
        pool = [question for question in questions if question.difficulty == difficulty]
        if len(pool) < per_difficulty:
            raise QuestionError(
                f"Нужно не меньше {per_difficulty} вопросов уровня {difficulty!r}, "
                f"есть {len(pool)}."
            )
        chosen = mixer.sample(pool, per_difficulty)
        selected.extend(shuffle_options(question, mixer) for question in chosen)
    return selected


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


def start_new_game(
    path: str | Path | None = None,
    *,
    rng: random.Random | None = None,
) -> GameState:
    """Новая партия: 5 случайных вопросов easy/medium/hard, варианты перемешаны."""
    return GameState(questions=select_game_questions(load_questions(path), rng=rng))


def format_money(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " ₽"
