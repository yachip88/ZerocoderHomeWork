"""Проверка логики без GUI."""

from game_logic import GameState, load_questions, format_money, PRIZES


def main() -> None:
    questions = load_questions()
    assert len(questions) == 15
    assert all(len(q.options) == 4 for q in questions)
    assert all(0 <= q.correct <= 3 for q in questions)

    state = GameState(questions=list(questions))
    # 5 верных, затем ошибка → несгораемые 1 000
    for i in range(5):
        assert state.answer(state.current.correct)
    assert state.index == 5
    assert state.prize == PRIZES[4]
    wrong = next(i for i in range(4) if i != state.current.correct)
    assert state.answer(wrong) is False
    assert state.finished and not state.won
    assert state.prize == 1_000

    state = GameState(questions=list(questions))
    for i in range(10):
        assert state.answer(state.current.correct)
    wrong = next(i for i in range(4) if i != state.current.correct)
    assert state.answer(wrong) is False
    assert state.prize == 32_000

    state = GameState(questions=list(questions))
    hidden = state.use_fifty_fifty()
    assert len(hidden) == 2
    assert state.current.correct not in hidden
    assert state.fifty_used

    state = GameState(questions=list(questions))
    votes = state.use_audience()
    assert sum(votes.values()) == 100
    assert state.audience_used

    state = GameState(questions=list(questions))
    for _ in range(15):
        assert state.answer(state.current.correct)
    assert state.won and state.prize == 1_000_000
    assert format_money(1_000_000) == "1 000 000 ₽"
    print("logic ok")


if __name__ == "__main__":
    main()
