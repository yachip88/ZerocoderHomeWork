# Примеры анализа сложности алгоритмов (Big-O) из урока.


def get_by_index(items, index):
    # O(1) — доступ к элементу списка по индексу
    return items[index]


def linear_search(items, target):
    # O(n) — линейный поиск: в худшем случае просматриваем все элементы
    for i, value in enumerate(items):
        if value == target:
            return i
    return -1


def binary_search(items, target):
    # O(log n) — двоичный поиск по отсортированному списку
    left = 0
    right = len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def count_pairs(items):
    # O(n^2) — вложенные циклы: каждая пара элементов
    count = 0
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j:
                count += 1
    return count


if __name__ == "__main__":
    numbers = [3, 8, 1, 15, 6, 10, 4]
    sorted_numbers = [1, 3, 4, 6, 8, 10, 15]

    print("Список:", numbers)
    print("O(1) элемент с индексом 2:", get_by_index(numbers, 2))
    print("O(n) линейный поиск 15:", linear_search(numbers, 15))
    print("O(n) линейный поиск 99:", linear_search(numbers, 99))
    print("Отсортированный список:", sorted_numbers)
    print("O(log n) двоичный поиск 10:", binary_search(sorted_numbers, 10))
    print("O(log n) двоичный поиск 99:", binary_search(sorted_numbers, 99))
    print("O(n^2) число пар:", count_pairs(numbers))
