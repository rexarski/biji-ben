# Exercise 3, Task 1 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 3, Task 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from stack import Stack
from stack_ex import reverse_top_two, reverse, SmallStackError


class TestStack(unittest.TestCase):

    def test_simple_reverse_top_two(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        reverse_top_two(stack)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), 2)
        self.assertTrue(stack.is_empty())

    def test_reverse_two_many(self):
        stack = Stack()
        for i in range(100):
            stack.push(i)
        reverse_top_two(stack)
        self.assertEqual(stack.pop(), 98)
        self.assertEqual(stack.pop(), 99)
        for i in range(97, -1, -1):
            self.assertEqual(stack.pop(), i)
        self.assertTrue(stack.is_empty())

    def test_reverse_two_empty(self):
        stack = Stack()
        with self.assertRaises(SmallStackError):
            reverse_top_two(stack)

    def test_reverse_two_one(self):
        stack = Stack()
        stack.push(1)
        with self.assertRaises(SmallStackError):
            reverse_top_two(stack)

    def test_simple_reverse(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        reverse(stack)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), 2)
        self.assertTrue(stack.is_empty())

    def test_reverse_many(self):
        stack = Stack()
        for i in range(100):
            stack.push(i)
        reverse(stack)
        for i in range(100):
            self.assertEqual(stack.pop(), i)
        self.assertTrue(stack.is_empty())

    def test_reverse_empty(self):
        stack = Stack()
        reverse(stack)
        self.assertTrue(stack.is_empty())

    def test_reverse_one(self):
        stack = Stack()
        stack.push(1)
        reverse(stack)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())

if __name__ == '__main__':
    unittest.main(exit=False)
