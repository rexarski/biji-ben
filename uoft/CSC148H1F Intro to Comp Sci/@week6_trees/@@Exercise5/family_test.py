# Exercise 5, Task 2 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 5, Task 2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from family import Person


class TestDescendants(unittest.TestCase):

    def setUp(self):
        self.alice = Person('Alice')
        self.bob = Person('Bob')
        self.charlie = Person('Charlie')

        self.alice.children = [self.bob, self.charlie]

    def test_descendants_simple(self):
        self.assertEqual(self.alice.count_descendants(), 2)

    def test_descendants_none(self):
        self.assertEqual(self.bob.count_descendants(), 0)


if __name__ == '__main__':
    unittest.main(exit=False)
