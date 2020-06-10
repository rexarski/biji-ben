# Assignment 1 - Sample unit tests
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sample unit tests for sms.py.

Because we're the code we're testing interacts
with the console, we need to do a bit of fiddling
to handle standard input and output.
Luckily for you, we've provided a base method
that does all of the work; you just need to provide
the actual test cases.
"""
import unittest
import sys
from io import StringIO
from sms import run


class TestSMS(unittest.TestCase):

    # Methods for redirecting input and output
    # Do not change these!
    def setUp(self):
        self.out = StringIO('')
        sys.stdout = self.out

    def tearDown(self):
        self.out.close()
        self.out = None
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    def io_tester(self, commands, outputs):
        """ (list of str, list of str) -> NoneType

        Simulate running input sms commands,
        check whether the output corresponds to outputs.
        DO NOT CHANGE THIS METHOD!
        """
        sys.stdin = StringIO('\n'.join(commands))
        run()
        self.assertEqual(self.out.getvalue(), '\n'.join(outputs))


    # YOUR TESTS GO HERE
    def test_simple(self):
        self.io_tester(['exit'], [''])

    def test_duplicate_student(self):
        self.io_tester(['create student david', 'create student david', 'exit'],
                       ['ERROR: Student david already exists.', ''])

if __name__ == '__main__':
    unittest.main(exit=False)
