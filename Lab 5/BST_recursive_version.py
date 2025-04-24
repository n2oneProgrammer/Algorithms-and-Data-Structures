class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 1

    def __str__(self):
        l = ""
        r = ""
        if self.left is not None:
            l = str(self.left)
        if self.right is not None:
            r = str(self.right)
        return l + str(self.key) + " " + str(self.value) + "," + r

    def calc_height(self):
        lh = 0
        rh = 0
        if self.left is not None:
            lh = self.left.height
        if self.right is not None:
            rh = self.right.height
        self.height = max(lh, rh) + 1
        return self.height

    def search(self, key):
        if self.key == key:
            return self.value
        if self.key > key:
            if self.left is None:
                return None
            return self.left.search(key)
        if self.right is None:
            return None
        return self.right.search(key)

    def insert(self, key, value):
        if key == self.key:
            self.value = value
            return self.height
        if self.key < key:
            if self.right is None:
                self.right = Node(key, value)
                self.height = 2
                return 2
            self.right.insert(key, value)
            self.calc_height()
            return self.height

        if self.left is None:
            self.left = Node(key, value)
            self.height = 2
            return 2
        self.left.insert(key, value)
        self.calc_height()
        return self.height

    def get_min_node(self):
        if self.left is None:
            return self
        return self.left.get_min_node()

    def delete(self, key):
        if key == self.key:
            if self.right is None:
                return self.left
            if self.left is None:
                return self.right

            min_node = self.right.get_min_node()
            self.key = min_node.key
            self.value = min_node.value
            self.right = self.right.delete(min_node.key)
            self.calc_height()
            return self
        if self.key < key and self.right is not None:
            self.right = self.right.delete(key)
        if self.key > key and self.left is not None:
            self.left = self.left.delete(key)
        self.calc_height()
        return self


class BinarySearchTree:
    def __init__(self):
        self.root: Node | None = None

    @property
    def height(self):
        if self.root is None:
            return 0
        return self.root.height

    def search(self, key):
        if self.root is None:
            return None
        return self.root.search(key)

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        self.root.insert(key, value)

    def delete(self, key):
        if self.root is None:
            return
        self.root = self.root.delete(key)

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
            print(lvl * " ", node.key, node.value)

            self.__print_tree(node.left, lvl + 5)


if __name__ == '__main__':
    tree = BinarySearchTree()
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
