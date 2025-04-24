import random
import time


class Element(object):
    def __init__(self, data, priority):
        self.__data = data
        self.__priority = priority

    def __lt__(self, other):
        return self.__priority < other.__priority

    def __ge__(self, other):
        return self.__priority >= other.__priority

    def __eq__(self, other):
        return self.__priority == other.__priority

    def __gt__(self, other):
        return self.__priority > other.__priority

    def __str__(self):
        return str(self.__priority) + ": " + str(self.__data)

    def __repr__(self):
        return str(self.__priority) + ": " + str(self.__data)


class HeapSort:
    def __init__(self, tab=None):
        if tab is None:
            self.__heap = []
            self.__size = 0
        else:
            self.__heap = tab
            self.__size = len(tab)

            for i in range(self.__size // 2, -1, -1):
                self.repair_struct_after_dequeue(i)

    def is_empty(self):
        return self.__size == 0

    def peek(self):
        if self.is_empty():
            return None
        return self.__heap[0]

    def sorted(self):
        while not self.is_empty():
            self.dequeue()
        return self.__heap

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
        self.__swap_nodes(0, self.__size - 1)
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
        if id >= self.__size:
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


def selection_sort_swap(tab):
    for i in range(len(tab) - 1):
        min_idx = i
        min_v = tab[i]
        for j in range(i + 1, len(tab)):
            if min_v > tab[j]:
                min_idx = j
                min_v = tab[j]
        tab[min_idx], tab[i] = tab[i], tab[min_idx]
    return tab


def insertion_sort_move(tab):
    for i in range(len(tab) - 1):
        min_idx = i
        min_v = tab[i]
        for j in range(i + 1, len(tab)):
            if min_v > tab[j]:
                min_idx = j
                min_v = tab[j]
        tab.pop(min_idx)
        tab.insert(0, min_v)
    return tab


def test1():
    l = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    lo = list(map(lambda e: Element(e[1], e[0]), l))
    heap = HeapSort(lo)
    heap.print_tab()
    heap.print_tree(0, 0)
    heap.sorted()
    print(lo)
    print("NIESTABLINE")
    print(selection_sort_swap(list(map(lambda e: Element(e[1], e[0]), l))))
    print("NIESTABLINE")
    print(insertion_sort_move(list(map(lambda e: Element(e[1], e[0]), l))))
    print("STABLINE")


def test2():
    l = [random.randint(0, 99) for i in range(10000)]
    lo = list(map(lambda e: Element('a', e), l))
    t_start = time.perf_counter()
    heap = HeapSort(lo)
    heap.sorted()
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


if __name__ == '__main__':
    test = int(input())
    if test == 1:
        test1()
    if test == 2:
        test2()
