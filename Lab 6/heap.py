class Element(object):
    def __init__(self, data, priority):
        self.__data = data
        self.__priority = priority

    def __lt__(self, other):
        return self.__priority < other.__priority

    def __eq__(self, other):
        return self.__priority == other.__priority

    def __gt__(self, other):
        return self.__priority > other.__priority

    def __str__(self):
        return str(self.__priority) + ": " + str(self.__data)


class Heap:
    def __init__(self):
        self.__heap = []
        self.__size = 0

    def is_empty(self):
        return self.__size == 0

    def peek(self):
        if self.is_empty():
            return None
        return self.__heap[0]

    def enqueue(self, data, priority):
        element = Element(data, priority)
        if len(self.__heap) <= self.__size:
            self.__heap.append(element)
        else:
            self.__heap[self.__size] = element
        self.__size += 1
        start = self.__size - 1
        parent_id = self.parent(start)

        parent = self.__get_node(parent_id)

        while parent < element:
            self.__swap_nodes(start, parent_id)
            start = parent_id
            parent_id = self.parent(start)
            parent = self.__get_node(parent_id)
            if parent_id < 0:
                break

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.__heap[0]
        self.__heap[0] = self.__heap[self.__size - 1]
        self.__size -= 1
        self.repair_struct_after_dequeue(0)
        return temp

    def repair_struct_after_dequeue(self, start):
        left_id = self.left(start)
        right_id = self.right(start)
        node = self.__get_node(start)
        left = self.__get_node(left_id)
        right = self.__get_node(right_id)

        if (left is not None and node < left) or (right is not None and node < right):
            if right is None or left > right:
                self.__swap_nodes(start, left_id)
                self.repair_struct_after_dequeue(left_id)
            else:
                self.__swap_nodes(start, right_id)
                self.repair_struct_after_dequeue(right_id)

    def __swap_nodes(self, id_a, id_b):
        if id_a >= self.__size:
            raise IndexError("Index out of range")
            return
        if id_b >= self.__size:
            raise IndexError("Index out of range")
            return
        temp = self.__heap[id_a]
        self.__heap[id_a] = self.__heap[id_b]
        self.__heap[id_b] = temp

    def print_tab(self):
        print('{', end=' ')
        print(*self.__heap[:self.__size], sep=', ', end=' ')
        print('}')

    def __get_node(self, id):
        if id > self.__size:
            return None
        return self.__heap[id] if self.__heap[id] else None

    def right(self, id):
        return 2 * (id + 1)

    def left(self, id):
        return 2 * (id + 1) - 1

    def parent(self, id):
        return (id - 1) // 2

    def print_tree(self, idx, lvl):
        if idx < self.__size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.__heap[idx] if self.__heap[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)


if __name__ == '__main__':
    heap = Heap()
    for i, priority in enumerate([7, 5, 1, 2, 5, 3, 4, 8, 9]):
        heap.enqueue("GRYMOTYLA"[i], priority)
    heap.print_tab()
    heap.print_tree(0, 0)
    t = heap.dequeue()
    print(heap.peek())
    heap.print_tab()
    print(t)
    while not heap.is_empty():
        print(heap.dequeue())

    heap.print_tab()
