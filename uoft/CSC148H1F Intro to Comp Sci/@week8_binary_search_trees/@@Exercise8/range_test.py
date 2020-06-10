# Exercise 8, Task 1 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 8, Task 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from bst import BinarySearchTree


class TestRange(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree(5)
        # Notice that we're using the interface method
        # to add values to the tree, rather than
        # manipulating the left and right attributes directly.
        self.bst.insert(3)
        self.bst.insert(10)
        
    def test_simple(self):
        self.assertEqual(self.bst.list_range(4, 7), [5])

    def test_simple_empty(self):
        self.assertEqual(self.bst.list_range(6, 7), [])


if __name__ == '__main__':
    unittest.main(exit=False)
