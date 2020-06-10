# Exercise 1, Task 1 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 1, Task 1 TESTS.

Note: all tests provided here. In future weeks,
only a subset of the tests will be provided,
and you'll be encouraged to write your own.
"""
import unittest
from error_library import *


class TestRuntimeErrors(unittest.TestCase):
    def test_bad_type(self):
        self.assertRaises(TypeError, bad_type)

    def test_bad_name(self):
        self.assertRaises(NameError, bad_name)

    def test_bad_attribute(self):
        self.assertRaises(AttributeError, bad_attribute)

    def test_bad_index(self):
        self.assertRaises(IndexError, bad_index)

    def test_bad_key(self):
        self.assertRaises(KeyError, bad_key)

    def test_bad_zero(self):
        self.assertRaises(ZeroDivisionError, bad_zero)

    def test_bad_import(self):
        self.assertRaises(ImportError, bad_import)


if __name__ == '__main__':
    unittest.main(exit=False)
