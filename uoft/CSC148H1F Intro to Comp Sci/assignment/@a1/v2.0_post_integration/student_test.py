# Assignment 1 - Unit Tests for Student
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
# Suyoung Lee, xxxxxxxxx 
# Rui Qiu, 999292509
#
# ---------------------------------------------
"""Unit tests for student.py

Submit this file, containing *thorough* unit tests
for your code in student.py.
Note that you should not have any tests involving
standard input or output in here.
"""
import unittest
from sms import *

class TestStudent(unittest.TestCase):
    
    def setUp(self):
        self.school1 = School('Jason enrols in CSC148')
        self.school1.student_create('Jason')
        self.school1.student_create('Sally')
        self.school1.enrol_student('Jason', 'CSC148')
        self.course1 = object_caller('CSC148', self.school1.course_list)[1]
        self.student1 = object_caller('Jason', self.school1.student_list)[1]
        
        self.school2 = School('empty school')
       
    
    def test_add_student_simple(self):
        self.assertTrue(object_caller('Jason', self.school1.student_list))

    def test_add_duplicate_student(self):
        self.school1.student_create('Jason')
        self.assertTrue(object_caller('Jason', self.school1.student_list))
        # assert also we get an error message
        
    
    def test_enrol_student_simple(self):
        self.assertTrue(self.student1 in self.school1.student_list)
        self.assertTrue(self.course1 in self.school1.course_list)
        self.assertEqual(['Jason'], self.course1.student_list)
        self.assertEqual(['CSC148'], self.student1.course_list)
    
    def test_enrol_nonexisting_student(self):
        self.school2.enrol_student('Jason', 'CSC148')
        self.assertEqual([], self.school2.student_list)
        self.assertEqual([], self.school2.course_list)
        #assert error message
    
    def test_enrol_full_course(self):
        count = 1
        for x in range(0, 31):
            self.school2.student_create('Jason' + str(count))
            self.school2.enrol_student('Jason' + str(count), 'CSC148')
            count += 1
        course = object_caller('CSC148', self.school2.course_list)[1]
        self.assertEqual(len(course.student_list), 30)
        self.assertTrue('Jason30' in course.student_list)
        self.assertTrue('Jason31' not in course.student_list)
        # assert Error message

    def test_drop_student_simple(self):
        self.school1.course_drop('Jason', 'CSC148')
        self.assertEqual([], self.student1.course_list)
        self.assertEqual([self.course1], self.school1.course_list)
    
    def test_drop_nonexisting_student(self):
        self.school1.course_drop('Nobody', 'CSC148')
        # if this passes, it's fine.
        # no error message needs to be raised
    
    def test_drop_nonexisting_course(self):
        self.school1.course_drop('Jason', 'ABC157')
        # no error message needed, if it passes, ok
    
    def test_student_list_courses_simple(self):
        self.school1.enrol_student('Jason', 'ABC157')
        self.school1.list_courses('Jason')
        self.assertEqual(self.student1.course_list, ['ABC157', 'CSC148'])
        # this needs to test print order
    
    def test_nonexisting_student_list_courses(self):
        self.school1.list_courses('Mary')
        # assert error message 
    
    def test_student_list_courses_empty(self):
        self.school1.student_create('Rob')
        self.school1.list_courses('Rob')
        # assert error message
    
    #def test_common_courses_simple(self):
        #self.school1.enrol_student('Jason', 'MAT157')
        #self.school1.enrol_student('Sally', 'MAT157')
        ## mat_course = object_caller('MAT157', self.school1.course_list)[1]
        ## self.assertEqual(len(mat_course.student_list), 2)
        #student2 = object_caller('Sally', self.school1.student_list)[1]
        #print ('previous line')
        #x = self.school1.common_check('Jason', 'Sally')
        #print (x)
        ##self.assertEqual(x, 'MAT157')
    
    def test_common_courses_nonexisting_students(self):
        self.school1.common_check('Lee', 'Qiu')
        # assert error message

    def test_common_courses_nonexisting_student_1(self):
        self.school1.common_check('Lee', 'Jason')
        # assert error message
    
    def test_common_courses_nonexisting_student_2(self):
        self.school1.common_check('Jason', 'Qiu')
        # assert error message
    
    def test_no_common_courses(self):
        self.school1.common_check('Jason', 'Sally')
        self.assertEqual(common_list, []))
    
    def test_list_students_taking_this_course(self):
        self.school1.enrol_student('Sally', 'CSC148')
        self.school1.student_create('Ed')
        self.school1.enrol_student('Ed', 'CSC148')
        self.assertEqual(self.school1.class_list('CSC148'), ['Ed', 'Jason', 'Sally'])
        
    def test_list_students_nonexisting_course(self):
        self.school1.class_list('CSC999')
        # assert error message
    
    def test_list_students_taking_an_empty_course(self):
        self.school1.course_drop('Jason', 'CSC148')
        self.assertEqual(self.school.class_list('CSC148'), [])
    
    def test_undo_create(self):
        self.school2.student_create('Ted')
        self.school2.undo_it('create student Ted'.split()) # should i undo_it or undo_once?
        self.assertEqual([], self.school2.student_list)       
    
    def test_undo_enrol(self):
        self.school2.student_create('Ted')
        self.school2.enrol_student('Ted', 'CSC148')
        self.school2.undo_it('enrol Ted CSC148'.split()) # same question
        self.assertEqual([], self.school2.list_courses('Ted'))
        
    def test_undo_drop(self):
        self.school2.student_create('Ted')
        self.school2.enrol_student('Ted', 'CSC148')
        self.school2.course_drop('Ted', 'CSC148')
        self.school2.undo_it('drop Ted CSC148'.split()) # same question
        self.assertEqual(['CSC148'], self.school12.list_courses('Ted'))
    
    def test_undo_unrecognized(self):
        self.school2.undo_it('ha ha ha ha'.split())
        #self.assertRaises(exception name blah blah blah)
    
    def test_undo_undo(self):
        self.school2.student_create('Ted')
        self.school2.enrol_student('Ted', 'CSC148')
        self.school2.course_drop('Ted', 'CSC148')
        self.undo_once()
        self.undo_once() # when run undo twice in a row, the previous two commands are reversed
        self.assertEqual([], self.school2.list_courses('Ted'))
        
    def test_undo_multiple(self):
        self.school2.student_create('Ted')
        self.school2.enrol_student('Ted', 'CSC148')
        self.school2.course_drop('Ted', 'CSC148')
        self.school2.undo_repeat(3)
        self.assertEqual([], self.school2.student_list)
    
    def test_undo_too_many_steps(self):
        self.school2.student_create('Ted')
        self.school2.undo_repeat(3)
        # assert error
    
    def test_nothing_to_undo(self):
        self.undo_once()
        self.assertRaises(EmptyStackError) # this could be problematic !!!
    
    def test_undo_valid_but_unrelated(self):
        self.school2.student_create('Ted')
        self.school2.student_create('Ted')
        self.school2.undo_it('create student Ted'.split())
        self.assertEqual(['Ted'], self.school2.student_list)           
    
    def test_undo_non_pos_steps(self):
        self.school2.undo_repeat(-5)
        #self.assertRaises(exception...)


if __name__ == '__main__':
    unittest.main(exit=False)
