class FullTable(Exception):
    pass


class ElementNotExist(Exception):
    pass


class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f'{self.key}: {self.value}'


class HashTable:
    def __init__(self, n=10, c1=1, c2=0):
        self.__tab: list[Element | None] = [None for i in range(n)]
        self.__c1 = c1
        self.__c2 = c2

    def hash(self, key):
        if isinstance(key, str):
            s = 0
            for c in key:
                s += ord(c)
            return s % len(self.__tab)
        return key % len(self.__tab)

    def search(self, key) -> any:
        id = self.hash(key)

        for i in range(len(self.__tab)):#
            new_id = (id + self.__c1 * i + self.__c2 * i * i) % len(self.__tab)
            if isinstance(self.__tab[new_id], Element) and key == self.__tab[new_id].key:
                return self.__tab[new_id].value
        return None

    def insert(self, key, value):
        id = self.hash(key)
        for i in range(len(self.__tab)):
            new_id = (id + self.__c1 * i + self.__c2 * i * i) % len(self.__tab)
            if isinstance(self.__tab[new_id], Element) and key == self.__tab[new_id].key:
                self.__tab[new_id].value = value
                return
            if not isinstance(self.__tab[new_id], Element):
                self.__tab[new_id] = Element(key, value)
                return
        raise FullTable

    def remove(self, key):
        id = self.hash(key)
        for i in range(len(self.__tab)):
            new_id = (id + self.__c1 * i + self.__c2 * i * i) % len(self.__tab)
            if isinstance(self.__tab[new_id], Element) and key == self.__tab[new_id].key:
                self.__tab[new_id] = None
                return
        raise ElementNotExist

    def __str__(self):
        out = []
        for el in self.__tab:
            out.append(str(el))
        return "{" + ", ".join(out) + "}"


if __name__ == "__main__":
    def test1(c1, c2):
        table = HashTable(13, c1, c2)
        ids = [1, 2, 3, 4, 5, 18, 31, 8, 9, 10, 11, 12, 13, 14, 15]
        values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
        for el in zip(ids, values):
            try:
                table.insert(el[0], el[1])
            except FullTable:
                print("Brak miejsca")

        print(table)
        print(table.search(5))
        print(table.search(14))
        table.insert(5, 'Z')
        print(table.search(5))
        table.remove(5)
        print(table)
        print(table.search(31))

        table.insert("test",'W')
        print(table)

    def test2(c1,c2):
        table = HashTable(13, c1, c2)
        ids = [1, 2, 3, 4, 5, 18, 31, 8, 9, 10, 11, 12, 13, 14, 15]
        values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
        for el in zip(ids, values):
            try:
                table.insert(el[0]*13, el[1])
            except FullTable:
                print("Brak miejsca")
        print(table)
    test1(1, 0)
    print()
    test2(1, 0)
    print()
    test1(1, 1)
    print()
    test2(1, 1)
    print()
