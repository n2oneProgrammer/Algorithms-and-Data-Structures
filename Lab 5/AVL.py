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

    @property
    def balance(self):
        lh = 0
        rh = 0
        if self.left is not None:
            lh = self.left.height
        if self.right is not None:
            rh = self.right.height
        return lh - rh

    def calc_height(self):
        lh = 0
        rh = 0
        if self.left is not None:
            lh = self.left.height
        if self.right is not None:
            rh = self.right.height
        self.height = max(lh, rh) + 1
        return self.height

    def balancing(self):
        balance = self.balance
        balance_r = 0
        if self.right is not None:
            balance_r = self.right.balance
        balance_l = 0
        if self.left is not None:
            balance_l = self.left.balance
        if balance <= -2 and balance_r <= 0:
            return self.rotate_left(self)
        if balance <= -2 and balance_r > 0:
            self.right = self.rotate_right(self.right)
            return self.rotate_left(self)
        if balance >= 2 and balance_l >= 0:
            return self.rotate_right(self)
        if balance >= 2 and balance_l < 0:
            self.left = self.rotate_left(self.left)
            return self.rotate_right(self)
        return self

    def insert(self, key, value):
        if key == self.key:
            self.value = value
            return self
        if self.key < key:
            if self.right is None:
                self.right = Node(key, value)
                self.height = 2
                return self
            r = self.right.insert(key, value)
            self.right = r
            self.calc_height()
            return self.balancing()

        if self.left is None:
            self.left = Node(key, value)
            self.height = 2
            return self
        l = self.left.insert(key, value)
        self.left = l
        self.calc_height()
        return self.balancing()

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
            return self.balancing()
        if self.key < key and self.right is not None:
            self.right = self.right.delete(key)
        if self.key > key and self.left is not None:
            self.left = self.left.delete(key)
        self.calc_height()
        return self.balancing()

    @staticmethod
    def rotate_left(node):
        a = node.right
        b = a.left
        a.left = node
        node.right = b

        lh = 0
        rh = 0
        if node.left is not None:
            lh = node.left.height
        if node.right is not None:
            rh = node.right.height
        node.height = max(lh, rh) + 1

        lh = 0
        rh = 0
        if a.left is not None:
            lh = a.left.height
        if a.right is not None:
            rh = a.right.height
        a.height = max(lh, rh) + 1

        return a

    @staticmethod
    def rotate_right(node):
        a = node.left
        b = a.right
        a.right = node
        node.left = b

        lh = 0
        rh = 0
        if node.left is not None:
            lh = node.left.height
        if node.right is not None:
            rh = node.right.height
        node.height = max(lh, rh) + 1
        lh = 0
        rh = 0
        if a.left is not None:
            lh = a.left.height
        if a.right is not None:
            rh = a.right.height
        a.height = max(lh, rh) + 1

        return a


class BinarySearchTreeAVL:
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
        self.root = self.root.insert(key, value)

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
    tree = BinarySearchTreeAVL()
    v = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 2: 'E', 1: 'F', 11: 'G', 100: 'H', 7: 'I', 6: 'J', 55: 'K', 52: 'L',
         51: 'M', 57: 'N', 8: 'O', 9: 'P', 10: 'R', 99: 'S', 12: 'T'}
    for key, value in v.items():
        print(key)
        tree.insert(key, value)
    tree.print_tree()
    print(tree)
    print(tree.search(10))
    tree.delete(50)
    tree.delete(52)
    tree.delete(11)
    tree.delete(57)
    tree.delete(1)
    tree.delete(12)
    tree.insert(3,'AA')
    tree.insert(4, 'BB')
    tree.delete(7)
    tree.delete(8)
    tree.print_tree()
    print(tree)
