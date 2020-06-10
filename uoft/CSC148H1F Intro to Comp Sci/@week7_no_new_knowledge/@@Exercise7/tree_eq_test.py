# Exercise 7, Task 1 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 7, Task 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from tree import Tree


class TestTreeEq(unittest.TestCase):

    def setUp(self):
        self.tree = Tree(1)
        self.tree.subtrees = [Tree('Hi'), Tree(3)]

    def test_simple(self):
        tree2 = Tree(1)
        tree2.subtrees = [Tree('Hi'), Tree(3)]
        self.assertTrue(self.tree == tree2)

    def test_empty(self):
        tree2 = Tree()
        tree3 = Tree()
        self.assertTrue(tree2 == tree3)
    
    def test_empty_v_non(self):
        tree2 = Tree()
        self.assertFalse(tree2 == self.tree)
        
    def test_complex(self):
        tree2 =Tree(3)
        self.assertFalse(tree2 == self.tree)
        
    def test_reversed(self):
        tree2 = Tree(1)
        tree2.subtrees = [Tree(3), Tree('Hi')]
        self.assertFalse(tree2 == self.tree)
        
    def test_3(self):
        self.tree = Tree(1)
        tree11 = Tree(11)
        tree12 = Tree(12)
        tree2 = Tree(1)
        tree21 = Tree(11)
        self.subtrees = [tree11, tree12]
        tree2.subtrees = [tree21]
        self.assertFalse(self.tree == tree2)
        
if __name__ == '__main__':
    unittest.main(exit=False)
