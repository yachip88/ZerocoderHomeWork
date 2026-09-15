from vowels import count_vowels


def test_only_vowels():
    assert count_vowels("аеёиоуыэюя") == 10
    assert count_vowels("aeiou") == 5


def test_no_vowels():
    assert count_vowels("bcdfg") == 0
    assert count_vowels("стрк") == 0
    assert count_vowels("") == 0


def test_mixed_case():
    assert count_vowels("Привет, WORLD") == 3
    assert count_vowels("AaEe") == 4
    assert count_vowels("PyThOn") == 1
