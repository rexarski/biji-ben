# Exercise 4, Task 1 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 4, Task 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from linked_list import LinkedList


class TestLinkedListEq(unittest.TestCase):

    def test_simple(self):
        list1 = LinkedList([1, 2])
        list2 = LinkedList([1, 2])

        # The following two tests do the same thing
        self.assertTrue(list1 == list2)
        self.assertTrue(list1.__eq__(list2))
    
    def test2(self):
        list1 = LinkedList([1, 2, 3])
        list2 = LinkedList([1, 2])
        self.assertTrue(list1 != list2)
        
    def test3(self):
        list1 = LinkedList([1, 2, 3])
        list2 = LinkedList([1, 3, 2])
        self.assertTrue(list1 != list2)
        
    def test4(self):
        list1 = LinkedList([])
        list2 = LinkedList([])
        self.assertTrue(list1 == list2)        

    def test5(self):
        list1 = LinkedList([1])
        list2 = LinkedList([])
        self.assertTrue(list1 != list2) 
        
    def test6(self):
        list1 = LinkedList([1, 2, 2, 3])
        list2 = LinkedList([1, 2, 3])
        self.assertTrue(list1 != list2)
        
    def test7(self):
        list1 = LinkedList([1, 2, 4])
        list2 = LinkedList([1, 2, 3])
        self.assertTrue(list1 != list2)
        
    def test8(self):
        list1 = LinkedList([3, 2, 3])
        list2 = LinkedList([1, 2, 3])
        self.assertTrue(list1 != list2)        
        
    def test8(self):
        list1 = LinkedList([1, 2, 3, 4])
        list2 = LinkedList([1, 2, 3, 5])
        self.assertTrue(list1 != list2)      
        
if __name__ == '__main__':
    unittest.main(exit=False)
