import random
from typing import List


def randomLevel(p: float, maxLevel: int) -> int:
    lvl = 1
    while random.random() < p and lvl < maxLevel:
        lvl = lvl + 1
    return lvl


class Node:
    def __init__(self, key: any, value: any, maxLevel, levels=0):
        self.key: any = key
        self.value: any = value
        if levels == 0:
            self.levels: int = randomLevel(0.5, maxLevel)
        else:
            self.levels: int = levels
        self.tab: List[Node | None] = [None for _ in range(self.levels)]

    def __str__(self):
        return f'{self.key}: {self.value}'

class SkipList:
    def __init__(self, max_level: int = 5):
        self.max_level: int = max_level
        self.head: Node = Node(None, None, max_level, max_level)

    def insert(self, key, value):
        element = Node(key, value, self.max_level)
        temp_elements: List[Node | None] = [None for _ in range(self.max_level)]
        pointer = self.head
        for i in range(self.max_level):
            while pointer.tab[self.max_level - i - 1] is not None and (
                    pointer.tab[self.max_level - i - 1].key is None or key >= pointer.tab[self.max_level - i - 1].key):
                pointer = pointer.tab[self.max_level - i - 1]
            if key == pointer.key:
                pointer.value = value
                return
            temp_elements[self.max_level - i - 1] = pointer
        for i in range(len(element.tab)):
            p = temp_elements[i]
            element.tab[i] = p.tab[i]
            p.tab[i] = element

    def search(self, key: any):
        pointer = self.head
        for i in range(self.max_level):
            while pointer.tab[self.max_level - i - 1] is not None and (
                    pointer.tab[self.max_level - i - 1].key is None or key >= pointer.tab[self.max_level - i - 1].key):
                pointer = pointer.tab[self.max_level - i - 1]
            if key == pointer.key:
                return pointer.value
        return None

    def delete(self, key) -> bool:
        pointer = self.head
        before = None
        for i in range(self.max_level):
            while pointer.tab[self.max_level - i - 1] is not None and (
                    pointer.tab[self.max_level - i - 1].key is None or key >= pointer.tab[self.max_level - i - 1].key):
                before = pointer
                pointer = pointer.tab[self.max_level - i - 1]

            if key == pointer.key:
                if before.levels >= max_level - i:
                    before.tab[max_level - i - 1] = pointer.tab[max_level - i - 1]
                pointer = before

    def displayList_(self):
        node = self.head.tab[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.tab[0]

        for lvl in range(self.max_level - 1, -1, -1):
            print(f"{lvl}  ", end=" ")
            node = self.head.tab[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print(end=5 * " ")
                    idx += 1
                idx += 1
                print(f"{node.key:2d}:{node.value:2s}", end="")
                node = node.tab[lvl]
            print()

    def __str__(self):
        pointer = self.head.tab[0]
        result = []
        while pointer is not None:
            result.append(pointer)
            pointer = pointer.tab[0]
        return "[" + ",".join(map(str, result)) + "]"


if __name__ == "__main__":
    max_level = 6
    random.seed(42)
    skipList = SkipList(max_level)
    ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for el in zip(ids, values):
        skipList.insert(el[0], el[1])
    skipList.displayList_()
    print(skipList.search(2))
    skipList.insert(2, 'Z')
    print(skipList.search(2))
    for k in [5, 6, 7]:
        skipList.delete(k)
    print(skipList)
    skipList.insert(6,'W')
    print(skipList)
