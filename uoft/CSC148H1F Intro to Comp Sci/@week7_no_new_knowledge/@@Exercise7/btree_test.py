# Exercise 7, Task 2 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 7, Task 2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from btree import BinaryTree


class TestTraversals(unittest.TestCase):

    def setUp(self):
        #      1
        #     / \
        #    2    3
        #   / \   / \
        #   4  5  6   7
        self.tree1 = BinaryTree(1)
        self.tree2 = BinaryTree(2)
        self.tree3 = BinaryTree(3)
        self.tree4 = BinaryTree(4)
        self.tree5 = BinaryTree(5)
        self.tree6 = BinaryTree(6)
        self.tree7 = BinaryTree(7)
        self.tree1.left = self.tree2
        self.tree1.right = self.tree3
        self.tree2.left = self.tree4
        self.tree2.right = self.tree5
        self.tree3.left = self.tree6
        self.tree3.right = self.tree7

    def test_preorder_simple(self):
        self.assertEqual([1, 2, 4, 5, 3, 6, 7], self.tree1.preorder())

    def test_inorder_simple(self):
        self.assertEqual([4, 2, 5, 1, 6, 3, 7], self.tree1.inorder())

    def test_postorder_simple(self):
        self.assertEqual([4, 5, 2, 6, 7, 3, 1], self.tree1.postorder())


if __name__ == '__main__':
    unittest.main(exit=False)
