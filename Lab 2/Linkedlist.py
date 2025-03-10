class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.__head = None

    def destroy(self):
        self.__head = None

    def add(self, value):
        node = Node(value, self.__head)
        self.__head = node

    def append(self, value):
        node = Node(value, None)
        if self.__head is None:
            self.__head = node
            return
        pointer = self.__head
        while pointer.next:
            pointer = pointer.next
        pointer.next = node

    def remove(self):
        if self.__head is None:
            return
        self.__head = self.__head.next

    def remove_end(self):
        if self.__head is None:
            return
        pointer = self.__head
        if pointer.next is None:
            self.__head = None
            return
        while pointer.next.next:
            pointer = pointer.next
        pointer.next = None

    def is_empty(self) -> bool:
        return self.__head is None

    def length(self) -> int:
        counter = 0
        pointer = self.__head
        while pointer.next:
            pointer = pointer.next
            counter += 1
        return counter

    def get(self):
        if self.__head is None:
            return None
        return self.__head.data

    def __str__(self) -> str:
        out = []
        if self.__head is None:
            return ""
        pointer = self.__head
        while pointer:
            out.append("-> " + str(pointer.data))
            pointer = pointer.next
        return "\n".join(out)


if __name__ == '__main__':
    ll = [('AGH', 'Kraków', 1919),
          ('UJ', 'Kraków', 1364),
          ('PW', 'Warszawa', 1915),
          ('UW', 'Warszawa', 1915),
          ('UP', 'Poznań', 1919),
          ('PG', 'Gdańsk', 1945)]

    uczelnie = LinkedList()
    uczelnie.append(ll[0])
    uczelnie.append(ll[1])
    uczelnie.append(ll[2])
    uczelnie.add(ll[3])
    uczelnie.add(ll[4])
    uczelnie.add(ll[5])
    print(uczelnie)
    print(uczelnie.length())
    uczelnie.remove()
    print(uczelnie.get())
    uczelnie.remove_end()
    print(uczelnie)
    uczelnie.destroy()
    print(uczelnie.is_empty())
    uczelnie.remove()
    uczelnie.remove_end()
    uczelnie.append(ll[0])
    uczelnie.remove_end()
    print(uczelnie.is_empty())