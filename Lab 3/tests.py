import unittest
from UnrolledLinkedList import UnrolledLinkedList


class UnrolledLinkedListTest(unittest.TestCase):

    def test_empty_output(self):
        ll = UnrolledLinkedList()
        self.assertEqual(ll.to_list(), [])

    def test_insert_10_elements(self):
        ll = UnrolledLinkedList()
        t = []
        for i in range(10):
            ll.insert(20, i)
            t.append(i)
            self.assertEqual(ll.to_list(), t)

    def test_insert_10_elements_start(self):
        ll = UnrolledLinkedList()
        t = []
        for i in range(10):
            ll.insert(0, i)
            t.insert(0, i)
            self.assertEqual(ll.to_list(), t)

    def test_insert_10_elements_index_4(self):
        ll = UnrolledLinkedList()
        t = []
        for i in range(10):
            ll.insert(4, i)
            t.insert(4, i)
            self.assertEqual(ll.to_list(), t)

    def test_insert_10_elements_index_4_2(self):
        ll = UnrolledLinkedList()
        t = []
        for i in range(10):
            ll.insert(4, i)
        ref = [
            [0, 1, 2, None, None, None],
            [3, 9, 8, 7, None, None],
            [6, 5, 4, None, None, None]
        ]
        head_inside = ll.__dict__['_UnrolledLinkedList__head']
        self.assertEqual(head_inside.tab, ref[0])
        head_inside = head_inside.next
        self.assertEqual(head_inside.tab, ref[1])
        head_inside = head_inside.next
        self.assertEqual(head_inside.tab, ref[2])
        head_inside = head_inside.next
        self.assertEqual(head_inside, None)

    def test_get(self):
        ll = UnrolledLinkedList()
        for i in range(10):
            ll.insert(i, i)

        self.assertEqual(ll.get(0), 0)
        self.assertEqual(ll.get(5), 5)
        self.assertEqual(ll.get(100), None)
        self.assertEqual(ll.get(-100), None)

    def test_remove_1(self):
        ll = UnrolledLinkedList()
        ll.delete(0)
        t = []
        for i in range(10):
            ll.insert(0, i)
            t.insert(0, i)

        for i in range(10):
            ll.delete(0)
            del t[0]
            self.assertEqual(ll.to_list(), t)

    def test_remove_2(self):
        ll = UnrolledLinkedList()
        ll.delete(0)
        t = []
        for i in range(10):
            ll.insert(0, i)
            t.insert(0, i)

        for i in range(10):
            ll.delete(len(t) // 2)
            del t[len(t) // 2]
            self.assertEqual(ll.to_list(), t)
if __name__ == '__main__':
    unittest.main()
