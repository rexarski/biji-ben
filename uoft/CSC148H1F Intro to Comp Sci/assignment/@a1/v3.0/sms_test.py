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
        
    def test_unrecognized(self):
        self.io_tester(['adfsdfsdf', 'exit'], ['Unrecognized command!', ''])

    def test_duplicate_student(self):
        self.io_tester(['create student david', 'create student david', 'exit'],
                       ['ERROR: Student david already exists.', ''])
    
    def test_enrol_student_simple(self):
        self.io_tester(['create student david', 'enrol david csc148', 'list-courses david', 'class-list csc148', 'exit'],
                       ['david is taking csc148', 'david', ''])
    
    def test_enrol_nonexisting_student(self):
        self.io_tester(['enrol david csc148', 'exit'], ['ERROR: Student david does not exist.', ''])

    def test_enrol_full_course(self):
        pass
    
    def test_drop_student_simple(self):
        self.io_tester(['create student david', 'enrol david csc148', 'drop david csc148', 'list-courses david', 'class-list csc148', 'exit'], ['david is not taking any courses.', 'No one is taking csc148.', ''])
        
    def test_drop_nonexisting_student(self):
        self.io_tester(['create student david', 'enrol david csc148', 'drop jack csc148', 'exit'], ['ERROR: Student jack does not exist.', ''])
    
    def test_drop_nonexisting_course(self):
        self.io_tester(['create student david', 'enrol david csc148', 'drop david csc831', 'exit'], [''])
        
    def test_student_list_courses_simple(self):
        self.io_tester(['create student david', 'enrol david csc148', 'enrol david abc123', 'enrol david mat133', 'list-courses david', 'exit'], ['david is taking abc123, csc148, mat133', ''])
    
    def test_nonexisting_student_list_courses(self):
        self.io_tester(['create student david', 'enrol david csc148', 'list-courses jack', 'exit'], ['ERROR: Student jack does not exist.', ''])

    def test_student_list_courses_empty(self):
        self.io_tester(['create student david', 'list-courses david', 'exit'], ['david is not taking any courses.', ''])
        
    def test_common_courses_simple(self):
        self.io_tester(['create student david', 'enrol david csc148', 'enrol david abc123', 'create student jack', 'enrol jack csc148', 'enrol jack abc123', 'common-courses david jack', 'exit'], ['abc123, csc148', ''])
        
    def test_common_courses_nonexisting_students(self):
        self.io_tester(['common-courses jack david', 'exit'], ['ERROR: Student jack does not exist.', 'ERROR: Student david does not exist.', ''])
        
    def test_common_courses_nonexisting_student1(self):
        self.io_tester(['create student jack', 'enrol jack csc148', 'enrol jack abc123', 'common-courses david jack', 'exit'], ['ERROR: Student david does not exist.', ''])
        
    def test_common_courses_nonexisting_student2(self):
        self.io_tester(['create student jack', 'enrol jack csc148', 'enrol jack abc123', 'common-courses jack david', 'exit'], ['ERROR: Student david does not exist.', ''])
        
    def test_no_common_courses(self):
        self.io_tester(['create student jack', 'create student david', 'common-courses jack david', 'exit'], ['', ''])
        
    def test_class_list(self):
        self.io_tester(['create student david', 'create student marry', 'create student jack', 'enrol david csc148', 'enrol jack csc148', 'enrol marry csc148', 'class-list csc148', 'exit'], ['david, jack, marry', ''])
        
    def test_class_list(self):
        self.io_tester(['class-list csc148', 'exit'], ['No one is taking csc148.', ''])
        
    def test_undo_create(self):
        self.io_tester(['create student david', 'undo', 'enrol david csc148', 'exit'], ['ERROR: Student david does not exist.', ''])
        
    def test_undo_enrol(self):
        self.io_tester(['create student david', 'enrol david csc148', 'undo', 'list-courses david', 'exit'], ['david is not taking any courses.', ''])
        
    def test_undo_drop(self):
        self.io_tester(['create student david', 'enrol david csc148', 'drop david csc148', 'undo', 'list-courses david', 'exit'], ['david is taking csc148', ''])
        
    def test_undo_unrecognized(self):
        self.io_tester(['create student david', 'sdfsfsd', 'undo', 'enrol david csc148', 'list-courses david', 'exit'], ['Unrecognized command!', 'david is taking csc148', ''])
        
    def test_undo_undo(self):
        self.io_tester(['create student david', 'enrol david csc148', 'enrol david csc108', 'undo', 'undo', 'list-courses david', 'exit'], ['david is not taking any courses.', ''])
        
    def test_undo_multiple(self):
        self.io_tester(['create student david', 'enrol david 1', 'enrol david 2', 'enrol david 3', 'enrol david 4', 'undo 4', 'list-courses david', 'exit'], ['david is not taking any courses.', ''])
        
    def test_nothing_to_undo(self):
        self.io_tester(['undo', 'exit'], ['ERROR: No commands to undo.', ''])
        
    def test_failure_undo(self):
        self.io_tester(['create student david', 'enrol david csc148', 'enrol david csc148', 'undo', 'class-list csc148', 'exit'], ['david', ''])
        
    def test_undo_non_positive_steps(self):
        self.io_tester(['create student david', 'enrol david csc148', 'undo -2', 'exit'], ['ERROR: -2 is not a positive natural number.', ''])
        
if __name__ == '__main__':
    unittest.main(exit=False)
