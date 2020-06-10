# Exercise 3, Task 2 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 3, Task 2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from chain import PeopleChain, ShortChainError


class TestPeopleChain(unittest.TestCase):

    def setUp(self):
        self.chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        self.empty_chain = PeopleChain([])
        self.one_chain = PeopleChain(['David'])
        self.two_chain = PeopleChain(['Karen', 'Paul'])
        self.large_chain = PeopleChain(['a', 'b', 'c', 'd', 'e', 'f'])

    def test_get_leader_simple(self):
        self.assertEqual(self.chain.get_leader(), 'Iron Man')

    def test_get_second_simple(self):
        self.assertEqual(self.chain.get_second(), 'Janna')

    def test_get_third_simple(self):
        self.assertEqual(self.chain.get_third(), 'Kevan')

    def test_get_leader_empty(self):
        self.assertRaises(ShortChainError, self.empty_chain.get_leader)
    
    def test_get_second_empty(self):
        self.assertRaises(ShortChainError, self.empty_chain.get_second)
        
    def test_get_third_empty(self):
        self.assertRaises(ShortChainError, self.empty_chain.get_third)
        
    def test_get_leader_one_chain(self):
        self.assertEqual(self.one_chain.get_leader(), 'David')
        
    def test_get_second_one_chain(self):
        self.assertRaises(ShortChainError, self.one_chain.get_second)
    
    def test_get_third_one_chain(self):
        self.assertRaises(ShortChainError, self.one_chain.get_third)
    
    def test_get_leader_two_chain(self):
        self.assertEqual(self.two_chain.get_leader(), 'Karen')
    
    def test_get_second_two_chain(self):
        self.assertEqual(self.two_chain.get_second(), 'Paul')
    
    def test_get_third_two_chain(self):
        self.assertRaises(ShortChainError, self.two_chain.get_third)
    
    def test_get_nth_large_chain(self):
        self.assertEqual(self.large_chain.get_nth(5), 'e')
        self.assertEqual(self.large_chain.get_nth(3), 'c')
        self.assertRaises(ShortChainError, self.large_chain.get_nth, 9)
        self.assertEqual(self.large_chain.get_nth(6), 'f')
        
    def test_get_two_people_simple(self):
        self.assertEqual(self.chain.get_leader(), 'Iron Man')
        self.assertEqual(self.chain.get_second(), 'Janna')
        
        

if __name__ == '__main__':
    unittest.main(exit=False)
