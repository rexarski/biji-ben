# Assignment 2 - Unit Tests for Course
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
# Su Young Lee, leesu9
# Rui Qiu, qiurui2
#
# ---------------------------------------------
"""Unit tests for course.py

Submit this file, containing *thorough* unit tests
for your code in course.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from course import (Course, UntakeableError, PrerequisiteError)

#            awe400
#               |
#            awe300
#            /     \
#          awe200   awe250
#          / |   \
#   awe100  awe101 awe199


class TestCourse(unittest.TestCase):
    
    def setUp(self):
        self.awe100 = Course('AWE100')
        self.awe101 = Course('AWE101')
        self.awe199 = Course('AWE199')
        self.awe200 = Course('AWE200', [self.awe100, self.awe101, self.awe199])
        self.awe250 = Course('AWE250')
        self.awe300 = Course('AWE300', [self.awe200, self.awe250])
        self.awe400 = Course('AWE400', [self.awe300])
        
    def test_takeable(self):
        # test whether a course without prereqs is takeable (it is!)
        self.assertEqual(self.awe100.is_takeable(), True)
        # test whether a course whose all prereqs are taken is takeable (it is as well!)
        self.awe100.take()
        self.awe101.take()
        self.awe199.take()
        self.assertEqual(self.awe200.is_takeable(), True)
        
    def test_untakeable(self):
        # test whether a course which lacks of certain prereq(s) is takeable (it is not!)
        self.assertEqual(self.awe200.is_takeable(), False)
    
    def test_take_takeable_untaken(self):
        self.assertEqual(self.awe100.taken, False)
        self.awe100.take()
        self.assertEqual(self.awe100.taken, True)
    
    def test_take_takeable_taken(self):
        self.awe100.take()
        self.assertEqual(self.awe100.taken, True)
        self.awe100.take()
        self.assertEqual(self.awe100.taken, True)      
    
    def test_take_untakeable(self):
        self.assertRaises(UntakeableError, self.awe400.take)
    
    def test_add_prereq_simple(self):
        self.awe099 = Course('AWE099')
        self.awe100.add_prereq(self.awe099)
        self.assertEqual(self.awe100.prereqs, [self.awe099])
    
    def test_add_prereq_itself(self):
        self.assertRaises(PrerequisiteError, self.awe100.add_prereq, self.awe100)
    
    def test_add_existing_children_prereq(self):
        self.assertRaises(PrerequisiteError, self.awe400.add_prereq, self.awe300)
        
    def test_add_existing_descendant_prereq(self):
        self.assertRaises(PrerequisiteError, self.awe400.add_prereq, self.awe100)
        
    def test_add_reversed_prereq(self):
        self.assertRaises(PrerequisiteError, self.awe300.add_prereq, self.awe400)
    
    def test_missing_nothing_first_year_course(self):
        self.assertEqual(self.awe100.missing_prereqs(), [])
    
    def test_missing_nothing_higher_year_course(self):
        self.awe100.take()
        self.awe101.take()
        self.awe199.take()
        self.assertEqual(self.awe200.missing_prereqs(), [])
    
    def test_missing_one(self):
        self.awe100.take()
        self.awe101.take()
        self.assertEqual(self.awe200.missing_prereqs(), ['AWE199'])
        
    def test_missing_many(self):
        self.assertEqual(self.awe400.missing_prereqs(), ['AWE100', 'AWE101', 'AWE199', 'AWE200', 'AWE250', 'AWE300'])
        self.awe100.take()
        self.awe101.take()
        self.awe199.take()
        self.assertEqual(self.awe400.missing_prereqs(), ['AWE200', 'AWE250', 'AWE300'])

if __name__ == '__main__':
    unittest.main(exit=False)
