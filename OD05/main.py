# Рекурсия и динамическое программирование (практика из урока).


def factorial(n):
    # Рекурсивный факториал: базовый случай n == 0 или n == 1
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci_naive(n):
    # Наивный рекурсивный Фибоначчи (много повторных вычислений)
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memo(n, memo=None):
    # Фибоначчи с мемоизацией (сверху вниз)
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_tab(n):
    # Фибоначчи табуляцией (снизу вверх)
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def kadane(arr):
    # Алгоритм Кадане: максимальная сумма подотрезка
    max_current = max_global = arr[0]
    for value in arr[1:]:
        max_current = max(value, max_current + value)
        if max_current > max_global:
            max_global = max_current
    return max_global


if __name__ == "__main__":
    print("Факториал 5:", factorial(5))
    print("Факториал 0:", factorial(0))

    print("Наивный Фибоначчи 10:", fibonacci_naive(10))
    print("Фибоначчи с мемоизацией 10:", fibonacci_memo(10))
    print("Фибоначчи табуляцией 10:", fibonacci_tab(10))
    print("Фибоначчи с мемоизацией 30:", fibonacci_memo(30))
    print("Фибоначчи табуляцией 30:", fibonacci_tab(30))

    numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("Массив:", numbers)
    print("Максимальная сумма подотрезка (Кадане):", kadane(numbers))
