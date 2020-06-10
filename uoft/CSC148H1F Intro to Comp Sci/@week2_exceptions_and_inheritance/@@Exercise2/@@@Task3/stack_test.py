# Exercise 2, Task 3 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 2, Task 3 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from stack import Stack
from stack_usage import remove_second


class TestRemoveSecond(unittest.TestCase):

    def test_simple_remove(self):
        stack = Stack()
        stack.push(1)
        stack.push(10)
        stack.push(30)
        stack.push(40)

        self.assertEqual(remove_second(stack), 30)
        self.assertEqual(stack.pop(), 40)
        self.assertEqual(stack.pop(), 10)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())


if __name__ == '__main__':
    unittest.main(exit=False)
