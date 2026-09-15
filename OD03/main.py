# Алгоритмы сортировки из урока (без list.sort / sorted внутри функций).
# Каждая функция работает с копией списка и возвращает новый отсортированный список.


def bubble_sort(data):
    arr = data[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(data):
    arr = data[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def quicksort(data):
    arr = data[:]
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


if __name__ == "__main__":
    numbers = [5, 2, 9, 1, 7, 3, 8, 2]
    print("Исходный список:", numbers)
    print("Пузырьковая сортировка:", bubble_sort(numbers))
    print("Сортировка вставками:", insertion_sort(numbers))
    print("Быстрая сортировка:", quicksort(numbers))
    print("Исходный список не изменился:", numbers)
