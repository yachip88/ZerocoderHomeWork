"""Проверка логики без GUI."""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from game_logic import (
    GameState,
    PRIZES,
    Question,
    QuestionError,
    format_money,
    load_questions,
    select_game_questions,
    shuffle_options,
    start_new_game,
)


def _write_json(payload: object) -> Path:
    directory = Path(tempfile.mkdtemp())
    path = directory / "questions.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def _bank(per_level: int = 8) -> list[Question]:
    questions: list[Question] = []
    for difficulty in ("easy", "medium", "hard"):
        for i in range(per_level):
            questions.append(
                Question(
                    text=f"{difficulty}-{i}",
                    options=["alpha", "beta", "gamma", "delta"],
                    correct=i % 4,
                    difficulty=difficulty,
                )
            )
    return questions


class SamplingTests(unittest.TestCase):
    def test_load_questions_keeps_more_than_fifteen(self) -> None:
        questions = load_questions()
        self.assertGreater(len(questions), 15)
        counts = Counter(question.difficulty for question in questions)
        self.assertGreaterEqual(counts["easy"], 5)
        self.assertGreaterEqual(counts["medium"], 5)
        self.assertGreaterEqual(counts["hard"], 5)

    def test_selects_five_questions_per_difficulty(self) -> None:
        selected = select_game_questions(_bank(), rng=random.Random(0))
        self.assertEqual(len(selected), 15)
        counts = Counter(question.difficulty for question in selected)
        self.assertEqual(counts, {"easy": 5, "medium": 5, "hard": 5})
        difficulties = [question.difficulty for question in selected]
        self.assertEqual(difficulties, ["easy"] * 5 + ["medium"] * 5 + ["hard"] * 5)

    def test_sampling_is_not_always_the_first_fifteen(self) -> None:
        bank = _bank(8)
        later_texts = {question.text for question in bank if not question.text.endswith(("-0", "-1", "-2", "-3", "-4"))}
        found_later = False
        for seed in range(40):
            selected = select_game_questions(bank, rng=random.Random(seed))
            if later_texts & {question.text for question in selected}:
                found_later = True
                break
        self.assertTrue(found_later)

    def test_different_seeds_can_pick_different_sets(self) -> None:
        bank = _bank(8)
        first = {q.text for q in select_game_questions(bank, rng=random.Random(1))}
        second = {q.text for q in select_game_questions(bank, rng=random.Random(2))}
        self.assertNotEqual(first, second)


class ShuffleTests(unittest.TestCase):
    def test_shuffled_options_keep_the_right_answer(self) -> None:
        original = Question(
            text="Столица?",
            options=["Альфа", "Бета", "Гамма", "Дельта"],
            correct=1,
            difficulty="easy",
        )
        correct_text = original.options[original.correct]
        changed_order = False
        for seed in range(30):
            shuffled = shuffle_options(original, random.Random(seed))
            self.assertEqual(shuffled.options[shuffled.correct], correct_text)
            self.assertEqual(set(shuffled.options), set(original.options))
            self.assertEqual(shuffled.text, original.text)
            if shuffled.options != original.options:
                changed_order = True
        self.assertTrue(changed_order)

    def test_game_answer_uses_shuffled_index(self) -> None:
        question = shuffle_options(
            Question("Q", ["нет", "да", "нет-2", "нет-3"], 1, "easy"),
            random.Random(7),
        )
        padding = [
            Question(f"pad-{i}", ["a", "b", "c", "d"], 0, "easy" if i < 4 else "medium" if i < 9 else "hard")
            for i in range(14)
        ]
        state = GameState(questions=[question, *padding])
        self.assertTrue(state.answer(question.correct))
        self.assertEqual(state.index, 1)


class ValidationTests(unittest.TestCase):
    def _valid_item(self, text: str, difficulty: str, correct: int = 0) -> dict:
        return {
            "text": text,
            "options": ["A", "B", "C", "D"],
            "correct": correct,
            "difficulty": difficulty,
        }

    def _full_bank(self, extra: list[dict] | None = None) -> dict:
        items = []
        for difficulty in ("easy", "medium", "hard"):
            for i in range(5):
                items.append(self._valid_item(f"{difficulty}-{i}", difficulty, i % 4))
        if extra:
            items.extend(extra)
        return {"questions": items}

    def test_invalid_correct_index_raises(self) -> None:
        payload = self._full_bank()
        payload["questions"][0]["correct"] = 9
        path = _write_json(payload)
        with self.assertRaises(QuestionError) as ctx:
            load_questions(path)
        self.assertIn("correct", str(ctx.exception))
        self.assertIn("0", str(ctx.exception))

    def test_negative_correct_index_raises(self) -> None:
        payload = self._full_bank()
        payload["questions"][1]["correct"] = -1
        with self.assertRaises(QuestionError):
            load_questions(_write_json(payload))

    def test_bad_json_raises_instead_of_hanging(self) -> None:
        directory = Path(tempfile.mkdtemp())
        path = directory / "questions.json"
        path.write_text("{это не json", encoding="utf-8")
        with self.assertRaises(QuestionError) as ctx:
            load_questions(path)
        self.assertIn("JSON", str(ctx.exception))

    def test_missing_field_raises(self) -> None:
        payload = self._full_bank()
        del payload["questions"][0]["options"]
        with self.assertRaises(QuestionError) as ctx:
            load_questions(_write_json(payload))
        self.assertIn("options", str(ctx.exception))

    def test_not_four_options_raises(self) -> None:
        payload = self._full_bank()
        payload["questions"][0]["options"] = ["A", "B"]
        with self.assertRaises(QuestionError):
            load_questions(_write_json(payload))

    def test_unknown_difficulty_raises(self) -> None:
        payload = self._full_bank()
        payload["questions"][0]["difficulty"] = "legend"
        with self.assertRaises(QuestionError) as ctx:
            load_questions(_write_json(payload))
        self.assertIn("legend", str(ctx.exception))

    def test_start_new_game_reports_bad_file(self) -> None:
        path = _write_json({"questions": []})
        with self.assertRaises(QuestionError):
            start_new_game(path)


class PrizeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.questions = select_game_questions(load_questions(), rng=random.Random(0))

    def test_safe_prize_after_five(self) -> None:
        state = GameState(questions=list(self.questions))
        for _ in range(5):
            self.assertTrue(state.answer(state.current.correct))
        self.assertEqual(state.index, 5)
        self.assertEqual(state.prize, PRIZES[4])
        wrong = next(i for i in range(4) if i != state.current.correct)
        self.assertFalse(state.answer(wrong))
        self.assertTrue(state.finished and not state.won)
        self.assertEqual(state.prize, 1_000)

    def test_safe_prize_after_ten(self) -> None:
        state = GameState(questions=list(self.questions))
        for _ in range(10):
            self.assertTrue(state.answer(state.current.correct))
        wrong = next(i for i in range(4) if i != state.current.correct)
        self.assertFalse(state.answer(wrong))
        self.assertEqual(state.prize, 32_000)

    def test_fifty_fifty(self) -> None:
        state = GameState(questions=list(self.questions))
        hidden = state.use_fifty_fifty()
        self.assertEqual(len(hidden), 2)
        self.assertNotIn(state.current.correct, hidden)
        self.assertTrue(state.fifty_used)

    def test_audience_votes_sum_to_100(self) -> None:
        state = GameState(questions=list(self.questions))
        votes = state.use_audience()
        self.assertEqual(sum(votes.values()), 100)
        self.assertTrue(state.audience_used)

    def test_full_win(self) -> None:
        state = GameState(questions=list(self.questions))
        for _ in range(15):
            self.assertTrue(state.answer(state.current.correct))
        self.assertTrue(state.won)
        self.assertEqual(state.prize, 1_000_000)
        self.assertEqual(format_money(1_000_000), "1 000 000 ₽")


def main() -> None:
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("logic ok")


if __name__ == "__main__":
    main()
