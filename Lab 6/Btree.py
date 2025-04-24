class Node:
    def __init__(self, n, is_leaf=True):
        self.keys = [None] * n
        self.children: list[Node] = [None] * (n + 1)
        self.size = 0
        self.is_leaf = is_leaf

    def height(self):
        return max(map(lambda x: x.height() if x is not None else 0, self.children)) + 1

    def insert(self, key):
        pointer = 0
        while pointer < self.size:
            if self.keys[pointer] is None or self.keys[pointer] > key:
                break
            pointer += 1
        if self.is_leaf:
            if self.size >= len(self.keys):
                m = self.keys[self.size // 2]
                p2 = self.keys[self.size // 2 + 1:]
                node2 = Node(len(self.keys))
                node2.keys[:self.size // 2] = p2

                self.size = self.size // 2
                node2.size = self.size
                if key > m:
                    node2.insert(key)
                else:
                    self.insert(key)
                return m, node2
            self.keys[pointer + 1:self.size + 1] = self.keys[pointer:self.size]
            self.keys[pointer] = key
            self.size += 1
            return None, None
        else:
            if self.children[pointer] is not None:
                k, ans = self.children[pointer].insert(key)
                if k is None:
                    return None, None
                if self.size >= len(self.keys):
                    m = self.keys[self.size // 2]
                    p2 = self.keys[self.size // 2 + 1:]
                    pc = self.children[self.size // 2 + 1:]
                    node2 = Node(len(self.keys), False)
                    node2.keys[:self.size // 2] = p2
                    node2.children[:self.size // 2 + 1] = pc
                    self.size = self.size // 2
                    node2.size = self.size
                    if key > m:
                        node2.keys[1:node2.size + 1] = node2.keys[0:node2.size]
                        node2.children[2:node2.size + 2] = node2.children[1:node2.size + 1]
                        node2.keys[0] = k
                        node2.size += 1
                        node2.children[1] = ans
                    else:
                        self.keys[self.size] = key
                        self.children[self.size + 1] = ans
                        self.size += 1
                    return m, node2
                self.keys[pointer + 1:] = self.keys[pointer:len(self.keys) - 1]
                self.children[pointer + 2:] = self.children[pointer + 1:len(self.children) - 1]
                self.keys[pointer] = k
                self.children[pointer + 1] = ans
                self.size += 1
                return None, None

            node = Node(len(self.keys))
            node.insert(key)
            self.children[pointer] = node
            return None, None


class Btree:
    def __init__(self, n):
        self.max_n = n
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(self.max_n)

        k, ans = self.root.insert(value)
        if k is not None:
            node = Node(self.max_n, is_leaf=False)
            node.keys[0] = k
            node.children[1] = ans
            node.children[0] = self.root
            node.size = 1
            self.root = node

    def height(self):
        if self.root is None:
            return 0
        return self.root.height()

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

    print(btree.height())
    btree2 = Btree(3)
    for i in range(20):
        btree2.insert(i)
    btree2.print_tree()
    print(btree2.height())
    for i in range(20, 200):
        btree2.insert(i)
    btree2.print_tree()
    btree3 = Btree(5)
    for i in range(200):
        btree3.insert(i)
    btree3.print_tree()
    print("Tree 2", btree2.height())
    print("Tree 3", btree3.height())
