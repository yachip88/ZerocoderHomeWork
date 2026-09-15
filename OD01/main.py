# Пошаговый алгоритм: является ли строка палиндромом
# 1. Получить исходную строку.
# 2. Если строка пустая — считаем её палиндромом.
# 3. Привести строку к нижнему регистру, чтобы «А» и «а» были одинаковыми.
# 4. Оставить только буквы (пробелы, цифры и знаки препинания игнорируем).
#    Так фразы вроде «А роза упала на лапу Азора» тоже проверяются корректно.
# 5. Сравнить очищенную строку с её перевёрнутой копией.
# 6. Если строки совпадают — это палиндром, иначе нет.


def is_palindrome(text):
    # шаг 2
    if text == "":
        return True

    # шаг 3
    lowered = text.lower()

    # шаг 4: оставляем только буквы
    cleaned = ""
    for char in lowered:
        if char.isalpha():
            cleaned += char

    # шаги 5–6
    reversed_text = cleaned[::-1]
    return cleaned == reversed_text


if __name__ == "__main__":
    examples = [
        "А роза упала на лапу Азора",
        "шалаш",
        "казак",
        "level",
        "привет",
        "Python",
        "Was it a cat I saw?",
        "",
    ]

    for phrase in examples:
        result = is_palindrome(phrase)
        print(f"{phrase!r} -> {result}")
