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


def insertion_sort(tab):
    for i in range(1, len(tab)):
        value = tab[i]
        j = i - 1

        while j >= 0 and tab[j] > value:
            tab[j + 1] = tab[j]
            j -= 1
        tab[j + 1] = value
    return tab


def shell_sort(tab):
    k3 = 1
    while (k3 - 1) // 2 < len(tab) // 3:
        k3 *= 3
    gap = (k3 // 3 - 1) // 2

    while gap > 0:
        for i in range(gap, len(tab)):
            temp = tab[i]
            j = i
            while j >= gap and tab[j - gap] > temp:
                tab[j] = tab[j - gap]
                j -= gap
            tab[j] = temp
        gap //= 3
    return tab


def test1():
    l =[(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
    lo = list(map(lambda e: Element(e[1], e[0]), l))
    insertion_sort(lo)
    print(lo)
    print("STABLINE")
    lo2 = list(map(lambda e: Element(e[1], e[0]), l))
    shell_sort(lo2)
    print(lo2)
    print("STABLINE")


def test2():
    l = [random.randint(0, 99) for i in range(10000)]
    lo = list(map(lambda e: Element('a', e), l))
    t_start = time.perf_counter()
    insertion_sort(lo)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
    lo2 = list(map(lambda e: Element('a', e), l))
    t_start = time.perf_counter()
    shell_sort(lo2)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


if __name__ == '__main__':
    test = int(input())
    if test == 1:
        test1()
    if test == 2:
        test2()
