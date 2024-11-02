## Author: Sharif Afandi
## Year  : 2024

import unittest
from avl import *

class TestBST(unittest.TestCase):
    def setUp(self):
        # print(f"{self.__class__.__name__} setUp")
        self.bst = self.getBST_0()

    def getBST_0(self) -> AVL:
        bst = AVL()

        bst.root = Node(5.0, 1.0,
                        Node(1.0, 2.0, 
                             Node(0.0, 4.0),
                             Node(3.0, 5.0,
                                  None,
                                  Node(4.0, 7.0))),
                        Node(10.0, 3.0,
                             None,
                             Node(11.0, 6.0)))

        return bst
    
    def getBST_1(self) -> AVL:
        return AVL()
    
    def getBST_Empty(self) -> AVL:
        return AVL()

    def test_ceil(self):
        # 1
        key = 6.123
        expectedCeil = 10.0
        ceil = self.bst.ceil_node(key).key  
        cmp = compare(ceil, expectedCeil)
        self.assertEqual(cmp, 0)
        # 2
        key = 1.0
        expectedCeil = 3.0
        ceil = self.bst.ceil_node(key).key
        cmp = compare(ceil, expectedCeil)
        self.assertEqual(cmp, 0)
        # 3
        key = 0.12356
        expectedCeil = 1.0
        ceil = self.bst.ceil_node(key).key
        cmp = compare(ceil, expectedCeil)
        self.assertEqual(cmp, 0)
        # 4
        key = 9.999999
        expectedCeil = 10.0
        ceil = self.bst.ceil_node(key).key
        cmp = compare(ceil, expectedCeil)
        self.assertEqual(cmp, 0)
        # 5
        key = 10.0
        expectedCeil = 11.0
        ceil = self.bst.ceil_node(key).key
        cmp = compare(ceil, expectedCeil)
        self.assertEqual(cmp, 0)
        # 6
        key = 11.0
        expectedCeil = None
        ceil = self.bst.ceil_node(key)
        self.assertIsNone(ceil)
    def test_floor(self):
        # 1
        key = 6.123
        expectedFloor = 5.0
        floor = self.bst.floor_node(key).key
        cmp = compare(floor, expectedFloor)
        self.assertEqual(cmp, 0)
        # 2
        key = 1.0
        expectedFloor = 0.0
        floor = self.bst.floor_node(key).key
        cmp = compare(floor, expectedFloor)
        self.assertEqual(cmp, 0)
        # 3
        key = 0.12356
        expectedFloor = 0.0
        floor = self.bst.floor_node(key).key
        cmp = compare(floor, expectedFloor)
        self.assertEqual(cmp, 0)
        # 4
        key = 10.00001
        expectedFloor = 10.0
        floor = self.bst.floor_node(key).key
        cmp = compare(floor, expectedFloor)
        self.assertEqual(cmp, 0)
        # 5
        key = 10.0
        expectedFloor = 5.0
        floor = self.bst.floor_node(key).key
        cmp = compare(floor, expectedFloor)
        self.assertEqual(cmp, 0)
        # 6
        key = 0.0
        expectedFloor = None
        floor = self.bst.floor_node(key)
        self.assertIsNone(floor)

    def test_insert(self):
        pass

    def test_remove(self):
        self.bst.remove(5.0)
        self.assertEqual(compare(self.bst.root.key, 4.0), 0)
        self.bst.remove(11.0)
        self.assertEqual(compare(self.bst.root.right.right, None), 0)
        self.bst.remove(1.0)
        self.assertEqual(compare(self.bst.root.left.key, 0.0), 0)
        self.bst.remove(3.0)
        self.assertEqual(compare(self.bst.root.left.right, None), 0)
        self.bst.remove(4.0)
        self.bst.remove(0.0)
        self.assertEqual(compare(self.bst.root.key, 10.0), 0)
        self.bst.remove(10.0)
        self.assertIsNone(self.bst.root)

    def test_rotations(self):
        pass
