class Queque:
    def __init__(self):
        self.__tab = [None for _ in range(5)]
        self.__index_save = 0
        self.__index_read = 0

    def is_empty(self):
        return self.__index_save == self.__index_read

    def peek(self) -> any:
        if self.is_empty():
            return None
        return self.__tab[self.__index_read]

    def dequeue(self):
        element = self.peek()
        if element is not None:
            self.__tab[self.__index_read] = None
            self.__index_read = (self.__index_read + 1) % len(self.__tab)
        return element

    def enqueue(self, element):
        self.__tab[self.__index_save] = element
        self.__index_save = (self.__index_save + 1) % len(self.__tab)
        if self.__index_save == self.__index_read:
            tab =  [None for _ in range(len(self.__tab)*2)]
            pointer = self.__index_read
            pp = 0
            end = (self.__index_save+len(self.__tab) - 1) % len(self.__tab)
            while pointer != end:
                tab[pp] = self.__tab[pointer]
                pointer = (pointer + 1) % len(self.__tab)
                pp = pp + 1

            tab[pp] = self.__tab[pointer]
            self.__index_save = pp + 1
            self.__index_read = 0
            self.__tab = tab

    def __str__(self):
        pointer = self.__index_read
        t = []
        while pointer != self.__index_save:
            t.append(str(self.__tab[pointer]))
            pointer = (pointer + 1) % len(self.__tab)

        return "["+', '.join(t)+"]"

    def get_state(self):
        return self.__tab


if __name__ == "__main__":
    que = Queque()
    for i in range(1,5):
        que.enqueue(i)
    print(que.dequeue())
    print(que.peek())
    print(que)
    for i in range(5,9):
        que.enqueue(i)
    print(que.get_state())
    while not que.is_empty():
        print(que.dequeue())
    print(que)


