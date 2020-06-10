# Assignment 1 - Managing Students!
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
"""The back-end data model for the program.

TODO: fill in this doctring with information about your
class(es)!
"""
# create student Bob-> undo_stack.push(('create', name))
# enrol Bob Course -> undo_stack.push(('enrol', name, course))
# drop Bob Course -> undo_stack.push(('drop', name, course))

class EmptyStackError(Exception):
    pass

class Stack:
    
    def __init__(self):
        self.command_stack = []
    
    def push(self, item):
        self.command_stack.append(item)
        
    def pop(self):
        try:
            self.comand_stack.pop()
        except IndexError:
            raise EmptyStackError
    
    def is_empty(self):
        return len(self.command_stack) == 0
    
class School:
    
    def __init__(self, name):
        self.name = name
        self.student_list = []
        self.course_list = [] # course_list should not be empty, it should be given
        self.undo_stack = Stack()
        
    def student_creater(self, name):
        if object_caller(name, self.student_list)[0]:
            print ("ERROR: Student", name, "already exists.")
        else:
            new_student = Student(name)
            self.student_list.append(new_student)
    
class Student:

    def __init__(self, name):
        self.name = name
        self.course_list = []
        
    def list_courses(name):
        personal_course_list = []
        if name not in self.student_list:
            print('ERROR: Student {0} does not exist.'.format(name))
        else:
            for course in School.course_list:
                if name in course.student_list:
                    personal_course_list += course
            if len(personal_course_list) == 0:
                print('{0} is not taking any courses.'.format(name))
            else:
                ablist = personal_course_list.sort()
                abstr = ', '.join(ablist)
                print('{0} is taking '.format(name) + abstr)
class Course:
    
    def __init__(self, name, student):
        self.name = name
        self.student_list = [student]
    
    def enrol_student_to_course(self, student, name):
        if student not in School.student_list:
            print('ERROR: Student {0} does not exist'.format(student))
        elif student in self.student_list:
            pass
        elif len(self.student_list) == 30:
            print('ERROR: Course {0} is full.'.format(name))
        else:
            self.student_list.append(student)
    
    def class_list(name):
        enrolled_students = []
        for student in School.student_list:
            if course in student.course_list:
                enrolled_students += studnet
        if len(enrolled_students) == 0:
            print('No one is taking {0}.'.format(name))
        else:
            ablist = enrolled_students.sort()
            print(ablist) # not sure whether here we shoult print a list or a stirng or strings?
    
def object_caller(name, target_list):
    for object in target_list:
        if object.name == name:
            return True, object
    return False, object