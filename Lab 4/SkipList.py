import random


def randomLevel(p=0.5, maxLevel=16):
    lvl = 1
    while random.random() < p and lvl < maxLevel:
        lvl += 1
    return lvl


class SkipListNode:
    def __init__(self, key, data, level):
        self.key = key
        self.data = data
        self.level = level
        self.tab = [None] * level

# Klasa reprezentująca listę z przeskokami (skip-list)
class SkipList:
    def __init__(self, max_level=16, p=0.5):
        self.max_level = max_level
        self.head = SkipListNode(None, None, self.max_level)  # Głowa listy
        self.p = p

    # Wyszukiwanie elementu po kluczu
    def search(self, key):
        current = self.head
        for level in range(self.max_level - 1, -1, -1):
            while current.tab[level] and current.tab[level].key < key:
                current = current.tab[level]
        current = current.tab[0]
        if current and current.key == key:
            return current.data
        return None

    # Wstawianie elementu o podanym kluczu i wartości
    def insert(self, key, data):
        update = [None] * self.max_level  # tablica przechowująca poprzedników
        current = self.head
        for level in range(self.max_level - 1, -1, -1):
            while current.tab[level] and current.tab[level].key < key:
                current = current.tab[level]
            update[level] = current

        # Sprawdzenie, czy element już istnieje
        current = current.tab[0]
        if current and current.key == key:
            current.data = data
            return

        # Losowanie poziomu dla nowego elementu
        level = randomLevel(self.p, self.max_level)
        new_node = SkipListNode(key, data, level)

        # Wstawianie nowego elementu na odpowiednich poziomach
        for i in range(level):
            new_node.tab[i] = update[i].tab[i]  # Przypisanie wskazań
            update[i].tab[i] = new_node

    # Usuwanie elementu o podanym kluczu
    def remove(self, key):
        update = [None] * self.max_level
        current = self.head
        for level in range(self.max_level - 1, -1, -1):
            while current.tab[level] and current.tab[level].key < key:
                current = current.tab[level]
            update[level] = current

        current = current.tab[0]
        if current and current.key == key:
            for level in range(self.max_level):
                if update[level].tab[level] != current:
                    break
                update[level].tab[level] = current.tab[level]

    # Zwrócenie reprezentacji listy (poziom 0)
    def __str__(self):
        result = []
        current = self.head.tab[0]
        while current:
            result.append(f"{current.key}:{current.data}")
            current = current.tab[0]
        return "[" + ", ".join(result) + "]"

    # Wypisanie całej listy (poziomy 0, 1, ..., max_level-1)
    def displayList_(self):
        for lvl in range(self.max_level - 1, -1, -1):
            print(f"{lvl}  ", end=" ")
            current = self.head.tab[lvl]
            while current:
                print(f"{current.key:2d}:{current.data:2s}", end=" ")
                current = current.tab[lvl]
            print()

# Testowanie funkcjonalności
if __name__ == "__main__":
    random.seed(42)  # Ustawienie ziarna dla generatora liczb losowych

    # Tworzymy pustą listę
    skip_list = SkipList()

    # Wstawiamy 15 elementów do listy
    for i in range(1, 16):
        skip_list.insert(i, chr(64 + i))  # Przypisujemy litery A, B, C, ..., O

    # Wypisujemy listę
    print("Lista po wstawieniu 15 elementów:")
    skip_list.displayList_()

    # Wyszukujemy element o kluczu 2
    print("\nWyszukano element o kluczu 2:", skip_list.search(2))

    # Wstawiamy nową wartość dla klucza 2
    skip_list.insert(2, 'Z')
    print("\nPo nadpisaniu wartości dla klucza 2:")
    skip_list.displayList_()

    # Wyszukujemy element o kluczu 2 po nadpisaniu
    print("\nWyszukano element o kluczu 2:", skip_list.search(2))

    # Usuwamy elementy o kluczach 5, 6, 7
    skip_list.remove(5)
    skip_list.remove(6)
    skip_list.remove(7)
    print("\nPo usunięciu elementów o kluczach 5, 6, 7:")
    skip_list.displayList_()

    # Wstawiamy element o kluczu 6
    skip_list.insert(6, 'W')
    print("\nPo wstawieniu elementu o kluczu 6:")
    skip_list.displayList_()

    # Wypisujemy listę poziomu 0
    print("\nLista poziomu 0:", skip_list)

    # Teraz wstawiamy elementy w odwrotnej kolejności
    skip_list = SkipList()  # Tworzymy nową pustą listę
    for i in range(15, 0, -1):
        skip_list.insert(i, chr(64 + i))  # Przypisujemy litery O, N, M, ..., A

    # Wypisujemy listę
    print("\nLista po wstawieniu 15 elementów w odwrotnej kolejności:")
    skip_list.displayList_()
