# Lab 4 (??) TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Lab 4 TESTS.

Write your own tests *before* writing the methods!
Developing this habit will help you greatly in the long run,
trust us!
"""
import unittest
from linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.lst = LinkedList([1, 2, 3])
        self.emp_list = LinkedList([])
        self.lst2 = LinkedList([1, 2, 2, 3])
        
    def test_simple_contains(self):
        self.assertTrue(1 in self.lst)
        self.assertTrue(2 in self.lst)
        self.assertFalse(4 in self.lst)
    
    def test_multiple_contains(self):
        self.assertTrue(1 and 2 in self.lst)
        self.assertTrue(2 and 3 in self.lst)
        self.assertTrue(self.lst.__contains__(1 and 2))
        
    def test_empty_contains(self):
        self.assertFalse(1 in self.emp_list)
        self.assertFalse(2 in self.emp_list)
        
    def test_simple_string(self):
        self.assertEqual(str(self.lst), '[1 -> 2 -> 3]')
        self.assertEqual('[1 -> 2 -> 3]', str(self.lst))
        
    def test_empty_contains(self):
        self.assertEqual(str(self.emp_list), '[]')
        
    def test_simple_set_item(self):
        #self.lst[1] = "hi"
        self.lst[1] = 'hi'
        #LinkedList.__setitem__(self.lst, 1, 'hi')
        self.assertEqual(str(self.lst), '[1 -> hi -> 3]')
        
    def test_failed_set_item(self):
        with self.assertRaises(IndexError):
            self.emp_list[11] = 0
        
    def test_delete_simple(self):
        self.lst.delete_item(3)
        self.assertEqual(str(self.lst), '[1 -> 2]')
        
        LinkedList.delete_item(self.lst, 1)
        self.assertEqual(str(self.lst), '[2]')
        
        LinkedList.delete_item(self.lst, 2)
        self.assertEqual(str(self.lst), '[]')
    
    def test_delete_nothing(self):
        LinkedList.delete_item(self.lst, 4)
        self.assertEqual(str(self.lst), '[1 -> 2 -> 3]')
    
    def test_delete_duplicate(self):
        LinkedList.delete_item(self.lst2, 2)
        self.assertEqual(str(self.lst), '[1 -> 2 -> 3]')

if __name__ == '__main__':
    unittest.main(exit=False)
