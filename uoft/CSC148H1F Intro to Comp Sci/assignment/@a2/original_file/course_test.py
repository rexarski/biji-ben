# Assignment 2 - Unit Tests for Course
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""Unit tests for course.py

Submit this file, containing *thorough* unit tests
for your code in course.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from course import (Course, AlreadyTakenError, UntakeableError,
                    PrerequisiteError)


class TestCourse(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main(exit=False)
