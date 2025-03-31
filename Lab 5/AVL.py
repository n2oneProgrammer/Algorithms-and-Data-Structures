class Node:
    def __init__(self, key, value,height):
        self.key = key
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.height: int = height

    def __str__(self):
        l = ""
        r = ""
        if self.left is not None:
            l = str(self.left)
        if self.right is not None:
            r = str(self.right)
        return l + str(self.key) + " " + str(self.value) + "," + r


class BinarySearchTreeAVL:
    def __init__(self):
        self.root: Node | None = None

    @property
    def height(self):
        if self.root is None:
            return 0
        return self.root.height

    def search(self, key):
        pointer = self.root
        while pointer is not None:
            if pointer.key == key:
                return pointer.value
            if pointer.key < key:
                pointer = pointer.right
            else:
                pointer = pointer.left
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value,1)
            return
        pointer = self.root
        while True:
            if pointer.key == key:
                pointer.value = value
                return
            pointer.height += 1
            if pointer.key > key:
                if pointer.left is None:
                    pointer.left = Node(key, value,pointer.height-1)
                    return
                pointer = pointer.left
                continue
            else:
                if pointer.right is None:
                    pointer.right = Node(key, value,pointer.height-1)
                pointer = pointer.right




    def delete(self, key):
        pointer = self.root
        before = None
        while pointer is not None:
            if pointer.key == key:
                if before is None:
                    if pointer.left is None and pointer.right is None:
                        self.root = None
                        return
                    if pointer.left is None:
                        before.right = pointer.right
                        return
                    if pointer.right is None:
                        before.right = pointer.left
                        return
                    bbefore = pointer
                    ppointer = pointer.right
                    while ppointer.left is not None:
                        bbefore = ppointer
                        ppointer = ppointer.left
                    bbefore.left = ppointer.right
                    pointer.key = ppointer.key
                    pointer.value = ppointer.value

                    return
                if pointer.left is None and pointer.right is None:
                    if before.key > key:
                        before.left = None
                    else:
                        before.right = None
                    return
                if pointer.left is None:
                    if before.key > key:
                        before.left = pointer.right
                    else:
                        before.right = pointer.right
                    return
                if pointer.right is None:
                    if before.key > key:
                        before.left = pointer.left
                    else:
                        before.right = pointer.left
                    return
                bbefore = pointer
                ppointer = pointer.right
                while ppointer.left is not None:
                    bbefore = ppointer
                    ppointer = ppointer.left
                bbefore.right = ppointer.right
                pointer.key = ppointer.key
                pointer.value = ppointer.value
                return

            if pointer.key < key:
                before = pointer
                pointer = pointer.right
            else:
                before = pointer
                pointer = pointer.left
        return None

    def __str__(self):
        if self.root is None:
            return ""
        return str(self.root)

    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if node is not None:
            self.__print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.height)

            self.__print_tree(node.left, lvl + 5)


if __name__ == '__main__':
    tree = BinarySearchTreeAVL()
    v = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K', 24: 'L'}
    for key, value in v.items():
        tree.insert(key, value)
    tree.print_tree()
    print(tree)
    print(tree.search(24))
    tree.insert(20, 'AA')
    tree.insert(6, 'M')
    tree.delete(62)
    tree.insert(59, 'N')
    tree.insert(100, 'P')
    tree.delete(8)
    tree.delete(15)
    tree.insert(55, 'R')
    tree.delete(50)
    tree.delete(5)
    tree.delete(24)
    print(tree.height)
    print(tree)
    tree.print_tree()
