# Exercise 8, Task 2 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 8, Task 2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from list_binary_tree import ListBinaryTree


class TestGoDownGreedy(unittest.TestCase):
    def setUp(self):
        self.tree = ListBinaryTree([4, 5, 3])
        
    def test_empty(self):
        self.tree1 = ListBinaryTree([])
        self.assertEqual(self.tree1.go_down_greedy(), [])
    
    def test_single(self):
        self.tree2 = ListBinaryTree([1])
        self.assertEqual(self.tree2.go_down_greedy(), [1])
        
    def test_simple(self):
        self.assertEqual(self.tree.go_down_greedy(), [4, 3])
        
    def test_complex(self):
        self.large_tree = ListBinaryTree([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(self.large_tree.go_down_greedy(), [1, 2, 4, 8])
    
    def test_complex_duplicate(self):
        self.large2 = ListBinaryTree([1, 2, 2, 3, 3, 4, 4, 6, 5])
        self.assertEqual(self.large2.go_down_greedy(), [1, 2, 3, 5])
    
    def test_complex_special_index(self):
        self.large3 = ListBinaryTree([5, 2, 3, 3, 3, 6, 9, 4, 10, 23, 3, 7, 9])
        #                    5
        #                   / \
        #                  2   3
        #                / \   / \
        #                3  3  6   9
        #              /\  /\  /\  
        #             4 10 23 3 7 9 
        # if go down greedy, like this: 5, 2, 3, 4
        self.assertEqual(self.large3.go_down_greedy(), [5, 2, 3, 4])
        self.assertEqual(self.large3.go_down_greedy(5), [3, 3])
        self.assertEqual(self.large3.go_down_greedy(7), [9])
        self.assertEqual(self.large3.go_down_greedy(3), [3, 6, 7])


if __name__ == '__main__':
    unittest.main(exit=False)
