TAB_LENGTH = 6


class Node:
    def __init__(self):
        self.tab = [None for i in range(TAB_LENGTH)]
        self.load = 0
        self.next = None

    def insert(self, index, element):
        if index >= TAB_LENGTH:
            return False
        if index >= self.load:
            self.tab[self.load] = element
            self.load += 1
            return True
        for i in range(self.load, index, -1):
            self.tab[i] = self.tab[i - 1]
        self.tab[index] = element
        self.load += 1

    def get(self, index):
        if index >= self.load:
            return None
        return self.tab[index]

    def delete(self, index):
        if index >= self.load:
            return None

        del self.tab[index]
        self.load -= 1
        self.tab.append(None)

    def __str__(self):
        if self.load == 0:
            return ""
        return ", ".join(map(str, self.tab[0:self.load]))


class UnrolledLinkedList:
    def __init__(self):
        self.__head = Node()

    def get(self, index):
        if index < 0:
            return None
        pointer = self.__head
        while index >= pointer.load:
            index -= pointer.load
            if pointer.next is None:
                return pointer.get(index)
            pointer = pointer.next
        return pointer.get(index)

    def insert(self, index, element):
        if index < 0:
            return None
        pointer = self.__head
        while index >= pointer.load:
            index -= pointer.load
            if pointer.next is None:
                if pointer.load < TAB_LENGTH:
                    pointer.insert(TAB_LENGTH - 1, element)
                    return
                pointer.next = Node()
                pointer.next.insert(0, element)
                return
            pointer = pointer.next
        if pointer.load >= TAB_LENGTH:
            new_node = Node()
            new_node.tab = pointer.tab[TAB_LENGTH // 2:] + [None for _ in range(TAB_LENGTH - TAB_LENGTH // 2)]
            new_node.load = TAB_LENGTH - TAB_LENGTH // 2
            pointer.tab = pointer.tab[:TAB_LENGTH // 2] + [None for _ in range(TAB_LENGTH // 2)]
            pointer.load = TAB_LENGTH // 2
            new_node.next = pointer.next
            pointer.next = new_node
            if index >= TAB_LENGTH // 2:
                index -= TAB_LENGTH // 2
                pointer = new_node
        pointer.insert(index, element)

    def delete(self, index):
        if index < 0:
            return None
        pointer = self.__head
        while index >= pointer.load:
            index -= pointer.load
            if pointer.next is None:
                return pointer.delete(index)
            pointer = pointer.next
        pointer.delete(index)
        if pointer.load < TAB_LENGTH // 2 and pointer.next is not None:
            if pointer.load + pointer.next.load <= TAB_LENGTH:
                pointer.tab[pointer.load:pointer.load + pointer.next.load] = pointer.next.tab[:pointer.next.load]
                pointer.load = pointer.load + pointer.next.load
                pointer.next = pointer.next.next
                return
            while pointer.load < TAB_LENGTH // 2:
                pointer.insert(TAB_LENGTH - 1, pointer.get(0))
                pointer.next.delete(0)

    def __str__(self):
        out = []
        pointer = self.__head
        while pointer:
            out.extend(pointer.tab[:pointer.load])
            pointer = pointer.next

        return "[" + ", ".join(map(str, out)) + "]"

    def to_list(self):
        out = []
        pointer = self.__head
        while pointer:
            out.extend(pointer.tab[:pointer.load])
            pointer = pointer.next
        return out

    def get_structure(self):
        out = []
        pointer = self.__head
        while pointer:
            out.append(str(pointer.tab))
            pointer = pointer.next

        return "->".join(out)


if __name__ == "__main__":
    ll = UnrolledLinkedList()
    for i in range(9):
        ll.insert(i, i + 1)
    print(ll.get(4))
    ll.insert(1, 10)
    ll.insert(8, 11)
    print(ll)
    ll.delete(1)
    ll.delete(2)
    print(ll)
