class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.is_leaf = False


class SuffixTree:
    def __init__(self, text: str):
        self._root: SuffixTreeNode = SuffixTreeNode()
        self._build(text)

    def _build(self, text: str):
        for i in range(len(text)):
            current = self._root
            for c in text[i:]:
                if c not in current.children:
                    current.children[c] = SuffixTreeNode()
                current = current.children[c]
            current.is_leaf = True

    def search(self, pattern):
        current = self._root
        for c in pattern:
            if c not in current.children:
                return 0
            current = current.children[c]
        return self._count_ends(current)

    def _count_ends(self, node):
        if node.is_leaf:
            return 1
        count = 0
        for child in node.children.values():
            count += self._count_ends(child)
        return count

    def print_tree(self):
        print("==============")
        self._print_tree(self._root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in node.children.keys():
                self._print_tree(node.children[i], lvl + 1)
                print(lvl * '  ', i)

class SuffixTable:
    def __init__(self,text):
        self.text = text
        self._build()

    def _build(self):
        suffixes = [(self.text[i:], i) for i in range(len(self.text))]
        suffixes.sort()
        self.tab = [idx for (suf, idx) in suffixes]

    def search(self, pattern):
        l, r = 0, len(self.tab) - 1

        while l <= r:
            mid = (l + r) // 2
            start = self.tab[mid]
            suffix = text[start:start + len(pattern)]

            if pattern == suffix:
                return True
            elif pattern < suffix:
                r = mid - 1
            else:
                l = mid + 1

        return False

if __name__ == '__main__':
    text = "banana\0"
    tree = SuffixTree(text)
    tree.print_tree()
    patterns = ["ana", "na", "nano"]
    for pat in patterns:
        print(f'{pat} występuje {tree.search(pat)} razy')

    table = SuffixTable(text)
    print(table.tab)

    patterns = ["ana", "na", "nano"]
    for pat in patterns:
        print(f'{pat} {"" if table.search(pat) else "nie"}występuje')



