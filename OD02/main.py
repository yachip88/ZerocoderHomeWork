# Стек (LIFO) и очередь (FIFO) на списках Python.
# Для очереди: enqueue вставляет в начало списка (index 0),
# dequeue забирает элемент с конца через pop() — как в уроке.


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


# Необязательно: простой граф списком смежности (как в уроке)
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node, neighbour):
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append(neighbour)

    def print_graph(self):
        for node in self.graph:
            print(f"{node}: {self.graph[node]}")


if __name__ == "__main__":
    print("=== Стек ===")
    stack = Stack()
    print("Пустой?", stack.is_empty())
    stack.push("книга 1")
    stack.push("книга 2")
    stack.push("книга 3")
    print("Верхний элемент (peek):", stack.peek())
    print("Сняли (pop):", stack.pop())
    print("Верхний элемент после pop:", stack.peek())
    print("Пустой?", stack.is_empty())

    print("\n=== Очередь ===")
    queue = Queue()
    print("Пустая?", queue.is_empty())
    queue.enqueue("клиент 1")
    queue.enqueue("клиент 2")
    queue.enqueue("клиент 3")
    print("Размер:", queue.size())
    print("Первым вышел (dequeue):", queue.dequeue())
    print("Размер после dequeue:", queue.size())
    print("Пустая?", queue.is_empty())

    print("\n=== Граф ===")
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    graph.print_graph()
