class Node:
    def __init__(self, data, next, prev):
        self.data = data
        self.next = next
        self.prev = prev


class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def destroy(self):
        while self.__head is not None:
            self.__head.prev = None
            self.__head = self.__head.next
        self.__head = None
        self.__tail = None

    def add(self, value):
        node = Node(value, self.__head, None)
        if self.__head is not None:
            self.__head.prev = node
        else:
            self.__tail = node
        self.__head = node

    def append(self, value):
        node = Node(value, None, self.__tail)
        if self.__head is None:
            self.__head = node
            self.__tail = node
            return
        self.__tail.next = node
        self.__tail = node

    def remove(self):
        if self.__head is None:
            return
        self.__head = self.__head.next
        if self.__head is None:
            self.__tail = None
        else:
            self.__head.prev = None

    def remove_end(self):
        if self.__head is None:
            return
        self.__tail = self.__tail.prev
        if self.__tail is None:
            self.__head = None
        else:
            self.__tail.next = None

    def is_empty(self) -> bool:
        return self.__head is None

    def length(self) -> int:
        counter = 0
        pointer = self.__head
        while pointer:
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

    def read_from_back(self):
        out = []
        if self.__tail is None:
            return ""
        pointer = self.__tail
        while pointer:
            out.append("-> " + str(pointer.data))
            pointer = pointer.prev
        return "\n".join(out)

if __name__ == '__main__':
    ll = [('AGH', 'Kraków', 1919),
          ('UJ', 'Kraków', 1364),
          ('PW', 'Warszawa', 1915),
          ('UW', 'Warszawa', 1915),
          ('UP', 'Poznań', 1919),
          ('PG', 'Gdańsk', 1945)]

    uczelnie = LinkedList()
    uczelnie.add(ll[3])
    uczelnie.add(ll[4])
    uczelnie.add(ll[5])
    uczelnie.append(ll[0])
    uczelnie.append(ll[1])
    uczelnie.append(ll[2])
    print(uczelnie)
    print()
    print(uczelnie.read_from_back())
    print(uczelnie.length())
    uczelnie.remove()
    print(uczelnie.get())
    uczelnie.remove_end()
    print(uczelnie)
    print()
    print(uczelnie.read_from_back())
    uczelnie.destroy()
    print(uczelnie.is_empty())
    uczelnie.remove()
    uczelnie.remove_end()
    uczelnie.append(ll[0])
    uczelnie.remove_end()
    print(uczelnie.is_empty())
