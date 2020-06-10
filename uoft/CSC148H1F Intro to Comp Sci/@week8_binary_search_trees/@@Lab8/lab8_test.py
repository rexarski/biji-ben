# Lab 8 Tests
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
import unittest
from bst import BinarySearchTree, EmptyBSTError


class TestCountAll(unittest.TestCase):

    def setUp(self):
        # Create FIVE BSTs:
        # - an empty BST
        # - a BST with one with just one node
        # - a BST with a left subtree, but an empty right subtree
        # - a BST with a right subtree, but an empty left subtree
        # - a BST with both a left and right subtree, with >= 6 nodes in all
        #
        # You should manually set the subtrees here (e.g., "self.left = ...")
        # It's your responsibility to ensure your BST actually satisfies
        # the Binary Search Tree property!
        self.b0 = BinarySearchTree()
        
        self.b1 = BinarySearchTree(4)
        
        self.b2 = BinarySearchTree(5)
        self.b2.left = BinarySearchTree(5)
        
        self.b3 = BinarySearchTree(5)
        self.b3.right = BinarySearchTree(6)
        
        self.b4 = BinarySearchTree(10)
        self.b4.left = BinarySearchTree(5)
        self.b4.left.left = BinarySearchTree(2)
        self.b4.left.right = BinarySearchTree(7)
        self.b4.right = BinarySearchTree(12)
        self.b4.right.left = BinarySearchTree(11)
        
        

    def test_empty(self):
        # Test count_all on an empty BST
        self.assertEqual(self.b0.count_all(5), 0)

    def test_one_success(self):
        # Test on a 1-node BST, where the root item is in the range
        self.assertEqual(self.b1.count_all(4), 1)

    def test_one_fail(self):
        # Test on a 1-node BST, where the root item isn't in the range
        self.assertEqual(self.b1.count_all(6), 0)      
        
    def test_no_left(self):
        # Test on a BST with no left subtree
        self.assertEqual(self.b3.count_all(6), 1)

    def test_no_right(self):
        # Test on a BST with no right subtree
        self.assertEqual(self.b2.count_all(5), 2)

    def test_both(self):
        # Test on a BST with both a left and right subtree
        self.assertEqual(self.b4.count_all(5), 1)
        

    def test_other(self):
        # Make up your own test; what cases are you missing?
        # (Think about putting duplicates in different places in the BST)
        self.b4.left.left.left = BinarySearchTree(2)
        self.b4.left.left.right = BinarySearchTree(5)
        self.assertEqual(self.b4.count_all(5), 2)
        self.assertEqual(self.b4.count_all(2), 2)


class TestNumInRange(unittest.TestCase):
    # Use the same test strategies as TestCountAll;
    # it's perfectly acceptable to use the same setUp() method!
    def setUp(self):
        self.b0 = BinarySearchTree()
        
        self.b1 = BinarySearchTree(4)
        
        self.b2 = BinarySearchTree(5)
        self.b2.left = BinarySearchTree(4)
        
        self.b3 = BinarySearchTree(5)
        self.b3.right = BinarySearchTree(6)
        
        self.b4 = BinarySearchTree(10)
        self.b4.left = BinarySearchTree(5)
        self.b4.left.left = BinarySearchTree(2)
        self.b4.left.right = BinarySearchTree(7)
        self.b4.right = BinarySearchTree(12)
        self.b4.right.left = BinarySearchTree(11)        

    def test_empty(self):
        self.assertEqual(self.b0.range(0, 1), 0)
        
    def test_single_node(self):
        self.assertEqual(self.b1.range(4, 6), 1)
        self.assertEqual(self.b1.range(2, 4), 1)
        self.assertEqual(self.b1.range(2, 5), 1)
        self.assertEqual(self.b1.range(2, 3), 0)
    def test_no_right(self):
        self.assertEqual(self.b2.range(4, 5), 2)
        self.assertEqual(self.b2.range(5, 5), 1)
        self.assertEqual(self.b2.range(3, 4), 1)
    def test_no_left(self):
        self.assertEqual(self.b3.range(4, 5), 1)
        self.assertEqual(self.b3.range(5, 6), 2)
        self.assertEqual(self.b3.range(6, 9), 1)
    def test_both(self):
        self.assertEqual(self.b4.range(2, 12), 6)
        self.assertEqual(self.b4.range(10, 15), 3)
        self.assertEqual(self.b4.range(7, 10), 2)
        self.assertEqual(self.b4.range(4, 9), 2)
        self.assertEqual(self.b4.range(13, 15), 0)
        self.assertEqual(self.b4.range(4, 5), 1)
        self.assertEqual(self.b4.range(3, 11), 4)

class TestDeleteNum(unittest.TestCase):
    def setUp(self):
        self.b1 = BinarySearchTree()
        self.b2 = BinarySearchTree(4)
        self.b3 = BinarySearchTree(5)
        
        self.b3.left = BinarySearchTree(3)
        self.b3.left.left = BinarySearchTree(3)
        self.b3.left.left.left = BinarySearchTree(2)
        self.b3.right = BinarySearchTree(10)
        self.b3.right.left = BinarySearchTree(7)
        self.b3.right.right = BinarySearchTree(12)
        
        
    def test_simple(self):
        self.assertTrue(self.b3.__contains__(10))
        self.b3.delete(10)
        self.assertFalse(self.b3.__contains__(10))
    def test_simple2(self):
        self.assertTrue(self.b3.__contains__(5))
        self.b3.delete(5)
        self.assertFalse(self.b3.__contains__(5))
    def test_simple3(self):
        self.assertTrue(self.b3.__contains__(3))
        self.b3.delete(3)
        self.assertTrue(self.b3.__contains__(3))
        
    def test_omplex(self):
        b = BinarySearchTree(5)
        b.left = BinarySearchTree(3)
        b.left.left = BinarySearchTree(2)
        b.left.right = BinarySearchTree(4)
        b.right = BinarySearchTree(10)
        b.right.left = BinarySearchTree(7)
        b.right.right = BinarySearchTree(12)
        
        self.b3.delete(3)
        
        self.assertEqual
        
        
        
if __name__ == '__main__':
    unittest.main(exit=False)
