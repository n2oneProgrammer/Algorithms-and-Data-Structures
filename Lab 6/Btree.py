class Node:
    def __init__(self, n, is_leaf=True):
        self.keys = [None] * n
        self.children:list[Node] = [None] * (n + 1)
        self.size = 0
        self.is_leaf = is_leaf

    def insert(self, key):
        pointer = 0
        while pointer < self.size:
            if self.keys[pointer] > key:
                break
            pointer += 1
        if self.is_leaf:
            if self.size >= len(self.keys):
                raise IndexError
            self.keys[pointer:self.size] = self.keys[pointer+1:self.size+1]
            self.keys[pointer] = key
            return None,None
        else:
            if self.children[pointer] is not None:
                k,ans = self.children[pointer].insert(key)
                if k is None:
                    return None,None


class Btree:
    def __init__(self, n):
        self.max_n = n
        self.root = Node

    def insert(self, value):
        if self.root is None:
            self.root = Node(self.max_n)

        self.root.insert(value)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size + 1):
                self._print_tree(node.children[i], lvl + 1)
                if i < node.size:
                    print(lvl * '  ', node.keys[i])


if __name__ == "__main__":
    btree = Btree(3)
    for i in [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]:
        btree.insert(i)
