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
from sms import run, command_stack


class TestSMS(unittest.TestCase):
    # Methods for redirecting input and output
    # Do not change these!
    def setUp(self):
        self.out = StringIO('')
        sys.stdout = self.out
        import sms_soln

        self.mod = sms_soln

    def tearDown(self):
        self.out.close()
        self.out = None
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        self.mod = None
        del sys.modules['sms_soln']

    def io_tester(self, commands, outputs):
        """ (list of str, list of str) -> NoneType

        Simulate running input sms commands,
        check whether the output corresponds to outputs.
        DO NOT CHANGE THIS METHOD!
        """
        sys.stdin = StringIO('\n'.join(commands))
        self.mod.run()
        self.assertEqual(self.out.getvalue(), '\n'.join(outputs))
        self.mod.command_stack = []

    def create_n_students(self, n):
        students = ['student{}'.format(i)
                    for i in range(n)]
        return students


class TestCreate(TestSMS):
    """
    Test create.
    """

    def test_student_created(self):
        self.io_tester(['create student david',
                        'exit'],
                       [''])

    def test_case_student(self):
        inp = ['create student david',
               'create student David',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_duplicate_student(self):
        inp = ['create student david',
               'create student david',
               'exit']
        exp = ['ERROR: Student david already exists.', '']
        self.io_tester(inp, exp)

    def test_non_duplicate_students(self):
        inp = ['create student david',
               'create student diane',
               'create student paul',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_duplicate_student_non_consecutive(self):
        inp = ['create student david',
               'create student diane',
               'create student jen',
               'create student david',
               'exit']
        exp = ['ERROR: Student david already exists.', '']
        self.io_tester(inp, exp)

    def test_many_duplicate_students(self):
        inp = ['create student david',
               'create student david',
               'create student jen',
               'create student david',
               'create student diane',
               'create student paul',
               'create student jen',
               'create student michelle',
               'exit']
        exp = ['ERROR: Student david already exists.',
               'ERROR: Student david already exists.',
               'ERROR: Student jen already exists.',
               '']
        self.io_tester(inp, exp)

    def test_invalid(self):
        inp = ['create stu david',
               'create student david liu',
               'exit']
        exp = ['Unrecognized command!',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)


class TestEnrol(TestSMS):
    """
    Test enrol.
    """

    def test_student_does_not_exist(self):
        inp = ['enrol david CSC148',
               'exit']
        exp = ['ERROR: Student david does not exist.', '']
        self.io_tester(inp, exp)

    def test_student_enrol(self):
        inp = ['create student david',
               'enrol david CSC148',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_students_enrol(self):
        inp = ['create student david',
               'enrol david CSC148',
               'enrol jen CSC148',
               'create student jen',
               'enrol jen CSC148',
               'exit']
        exp = ['ERROR: Student jen does not exist.',
               '']
        self.io_tester(inp, exp)

    def test_student_double_enrol(self):
        inp = ['create student david',
               'enrol david CSC148',
               'enrol david CSC148',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_student_enrol_in_many_courses(self):
        inp = ['create student david',
               'enrol david CSC108',
               'enrol david CSC148',
               'enrol david MAT223',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_student_enrol_many_students_in_course(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student diane',
               'enrol diane CSC148',
               'create student paul',
               'enrol paul CSC148',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_students_enrol_courses(self):
        inp = ['create student david',
               'enrol david CSC148',
               'enrol jen CSC148',
               'create student jen',
               'enrol jen CSC148',
               'enrol jen CSC108',
               'enrol jen CSC148',
               'create student paul',
               'enrol paull CSC108',
               'enrol paul CSC108',
               'enrol david CSC108',
               'enrol david CSC148',
               'exit']
        exp = ['ERROR: Student jen does not exist.',
               'ERROR: Student paull does not exist.',
               '']
        self.io_tester(inp, exp)

    def test_29_students(self):
        students = self.create_n_students(29)
        creates = ['create student {}'.format(name) for name in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        inp = creates + enrollms + ['exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_30_students(self):
        students = self.create_n_students(30)
        creates = ['create student {}'.format(name) for name in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        inp = creates + enrollms + ['exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_31_students(self):
        students = self.create_n_students(31)
        creates = ['create student {}'.format(name) for name in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        inp = creates + enrollms + ['exit']
        exp = ['ERROR: Course CSC148 is full.', '']
        self.io_tester(inp, exp)

    def test_31_students_in_two_courses(self):
        students = self.create_n_students(31)
        creates = ['create student {}'.format(name) for name in students]
        enrollms = (['enrol {} CSC148'.format(name) for name in students[:15]] +
                    ['enrol {} CSC108'.format(name) for name in students[15:]])
        inp = creates + enrollms + ['exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_invalid(self):
        inp = ['enrol',
               'enrol david csc148 hello',
               'exit']
        exp = ['Unrecognized command!',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)


class TestDrop(TestSMS):
    """
    Test drop.
    """

    def test_drop_student_does_not_exist(self):
        inp = ['enrol david CSC148',
               'drop david CSC148',
               'exit']
        exp = ['ERROR: Student david does not exist.',
               'ERROR: Student david does not exist.',
               '']
        self.io_tester(inp, exp)

    def test_drop_simple(self):
        inp = ['create student david',
               'enrol david CSC148',
               'drop david CSC148',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_drop_non_enrolled(self):
        inp = ['create student david',
               'drop david CSC148',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_full_drop_enrol_back(self):
        students = self.create_n_students(30)
        create_students = ['create student {}'.format(x) for x in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        drop = 'drop {} CSC148'.format(students[10])
        enroll = 'enrol {} CSC148'.format(students[10])
        inp = create_students + enrollms + [drop, enroll, 'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_full_drop_enrol_back_multiple(self):
        students = self.create_n_students(30)
        create_students = ['create student {}'.format(x) for x in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        drop = ['drop {} CSC148'.format(name) for name in students[5:10]]
        enroll = ['enrol {} CSC148'.format(name) for name in students[5:10]]
        inp = create_students + enrollms + drop + enroll + ['exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_drop_mixed(self):
        inp = ['create student david',
               'drop david CSC148',
               'enrol david CSC108',
               'drop david CSC148',
               'enrol david CSC148',
               'drop david CSC148',
               'drop davidd CSC148',
               'drop davidd CSC148',
               'drop david CSC148',
               'enrol david CSC148',
               'enrol david CSC148',
               'exit']
        exp = ['ERROR: Student davidd does not exist.',
               'ERROR: Student davidd does not exist.',
               '']
        self.io_tester(inp, exp)

    def test_invalid(self):
        inp = ['drop david',
               'drop david liu CSC148',
               'exit']
        exp = ['Unrecognized command!',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)


class TestListCourses(TestSMS):
    """
    Test list-courses.
    """

    def test_student_does_not_exist(self):
        inp = ['list-courses david',
               'exit']
        exp = ['ERROR: Student david does not exist.', '']
        self.io_tester(inp, exp)

    def test_no_courses(self):
        inp = ['create student david',
               'list-courses david',
               'exit']
        exp = ['david is not taking any courses.', '']
        self.io_tester(inp, exp)

    def test_one_course(self):
        inp = ['create student david',
               'enrol david CSC148',
               'list-courses david',
               'exit']
        exp = ['david is taking CSC148', '']
        self.io_tester(inp, exp)

    def test_one_course_other_students(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student paul',
               'enrol david CSC108',
               'list-courses david',
               'exit']
        exp = ['david is taking CSC108, CSC148', '']
        self.io_tester(inp, exp)

    def test_three_courses_alphabetical(self):
        inp = ['create student david',
               'enrol david STA247',
               'enrol david CSC148',
               'enrol david MAT223',
               'list-courses david',
               'exit']
        exp = ['david is taking CSC148, MAT223, STA247', '']
        self.io_tester(inp, exp)

    def test_list_courses_mixed_with_drop(self):
        inp = ['create student david',
               'enrol david STA247',
               'enrol david CSC148',
               'enrol david MAT223',
               'list-courses david',
               'drop david MAT223',
               'list-courses david',
               'exit']
        exp = ['david is taking CSC148, MAT223, STA247',
               'david is taking CSC148, STA247',
               '']
        self.io_tester(inp, exp)

    def test_list_courses_drop_all(self):
        inp = ['create student david',
               'enrol david STA247',
               'enrol david CSC148',
               'enrol david MAT223',
               'list-courses david',
               'drop david MAT223',
               'drop david STA247',
               'drop david CSC148',
               'list-courses david',
               'enrol david CSC1000',
               'list-courses david',
               'exit']
        exp = ['david is taking CSC148, MAT223, STA247',
               'david is not taking any courses.',
               'david is taking CSC1000',
               '']
        self.io_tester(inp, exp)

    def test_list_courses_mixed(self):
        inp = ['create student david',
               'list-courses diane',
               'create student diane',
               'enrol david CSC148',
               'enrol davidd MAT223',
               'list-courses david',
               'list-courses diane',
               'enrol diane CSC148',
               'list-courses diane',
               'exit']
        exp = ['ERROR: Student diane does not exist.',
               'ERROR: Student davidd does not exist.',
               'david is taking CSC148',
               'diane is not taking any courses.',
               'diane is taking CSC148',
               '']
        self.io_tester(inp, exp)

    # David added test
    def test_list_courses_full(self):
        students = self.create_n_students(30)
        create_students = ['create student {}'.format(x) for x in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        drop = 'drop {} CSC148'.format(students[10])
        enroll = 'enrol {} CSC148'.format(students[10])
        inp = create_students + enrollms + ['list-courses student10',
                                            drop,
                                            'list-courses student10',
                                            enroll,
                                            'list-courses student10',
                                            'exit']
        exp = ['student10 is taking CSC148.',
               'student10 is not taking any courses.',
               'student10 is taking CSC148.',
               '']
        self.io_tester(inp, exp)

    def test_list_courses_full(self):
        students = self.create_n_students(31)
        create_students = ['create student {}'.format(x) for x in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        inp = create_students + enrollms + ['list-courses student30', 'exit']
        exp = ['ERROR: Course CSC148 is full.',
               'student30 is not taking any courses.',
               '']
        self.io_tester(inp, exp)

    def test_invalid(self):
        inp = ['list-courses',
               'list-courses david diane',
               'exit']
        exp = ['Unrecognized command!',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)


class TestCommonCourses(TestSMS):
    """
    Test common-courses.
    """

    def test_common_students_do_not_exist(self):
        inp = ['common-courses david diane',
               'exit']
        exp = ['ERROR: Student david does not exist.',
               'ERROR: Student diane does not exist.', '']
        self.io_tester(inp, exp)

    def test_common_student2_does_not_exist(self):
        inp = ['create student david',
               'common-courses david diane',
               'exit']
        exp = ['ERROR: Student diane does not exist.', '']
        self.io_tester(inp, exp)

    def test_common_student1_does_not_exist(self):
        inp = ['create student diane',
               'common-courses david diane',
               'exit']
        exp = ['ERROR: Student david does not exist.', '']
        self.io_tester(inp, exp)

    def test_no_courses_together(self):
        inp = ['create student david',
               'create student diane',
               'common-courses david diane',
               'exit']
        exp = ['', '']
        self.io_tester(inp, exp)

    def test_one_course_together(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student diane',
               'enrol diane CSC148',
               'common-courses david diane',
               'exit']
        exp = ['CSC148', '']
        self.io_tester(inp, exp)

    def test_one_course_together_order(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student diane',
               'enrol diane CSC148',
               'common-courses david diane',
               'common-courses diane david',
               'exit']
        exp = ['CSC148', 'CSC148', '']
        self.io_tester(inp, exp)

    def test_two_courses_together(self):
        inp = ['create student david',
               'enrol david CSC108',
               'enrol david CSC148',
               'create student diane',
               'enrol diane CSC108',
               'enrol diane CSC148',
               'common-courses david diane',
               'exit']
        exp = ['CSC108, CSC148', '']
        self.io_tester(inp, exp)

    def test_two_courses_together_alphabetical(self):
        inp = ['create student david',
               'enrol david MAT223',
               'enrol david CSC148',
               'create student diane',
               'enrol diane MAT223',
               'enrol diane CSC148',
               'common-courses david diane',
               'exit']
        exp = ['CSC148, MAT223', '']
        self.io_tester(inp, exp)

    def test_three_courses_together_alphabetical(self):
        inp = ['create student david',
               'enrol david CSC108',
               'enrol david MAT223',
               'enrol david CSC148',
               'create student diane',
               'enrol diane CSC148',
               'enrol diane MAT223',
               'enrol diane CSC108',
               'common-courses david diane',
               'exit']
        exp = ['CSC108, CSC148, MAT223', '']
        self.io_tester(inp, exp)

    def test_two_courses_one_together(self):
        inp = ['create student david',
               'enrol david MAT223',
               'enrol david CSC148',
               'create student diane',
               'enrol diane MAT137',
               'enrol diane CSC148',
               'common-courses david diane',
               'exit']
        exp = ['CSC148', '']
        self.io_tester(inp, exp)

    def test_common_mixed(self):
        inp = ['create student david',
               'common-courses david diane',
               'create student diane',
               'create student david',
               'common-courses david diane',
               'enrol diane MAT137',
               'enrol diane CSC148',
               'common-courses david diane',
               'enrol david CSC108',
               'common-courses david diane',
               'enrol david CSC148',
               'common-courses david diane',
               'drop diane CSC148',
               'common-courses david diane',
               'exit']
        exp = ['ERROR: Student diane does not exist.',
               'ERROR: Student david already exists.',
               '',
               '',
               '',
               'CSC148',
               '',
               '']
        self.io_tester(inp, exp)

    def test_invalid(self):
        inp = ['common-courses david',
               'common-courses david diane lester',
               'exit']
        exp = ['Unrecognized command!',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)


class TestClassList(TestSMS):
    """
    Test class-list.
    """

    def test_empty_course(self):
        inp = ['class-list CSC148',
               'exit']
        exp = ['No one is taking CSC148.', '']
        self.io_tester(inp, exp)

    def test_drop_course(self):
        inp = ['create student david',
               'enrol david CSC148',
               'drop david CSC148',
               'class-list CSC148',
               'exit']
        exp = ['No one is taking CSC148.', '']
        self.io_tester(inp, exp)

    def test_invalid_student(self):
        inp = ['enrol david CSC148',
               'class-list CSC148',
               'exit']
        exp = ['ERROR: Student david does not exist.',
               'No one is taking CSC148.',
               '']
        self.io_tester(inp, exp)

    def test_one_student(self):
        inp = ['create student david',
               'enrol david CSC148',
               'class-list CSC148',
               'exit']
        exp = ['david', '']
        self.io_tester(inp, exp)

    def test_students_alphabetical(self):
        inp = ['create student paul',
               'create student david',
               'create student jen',
               'enrol paul CSC148',
               'enrol david CSC148',
               'enrol jen CSC148',
               'class-list CSC148',
               'exit']
        exp = ['david, jen, paul', '']
        self.io_tester(inp, exp)

    def test_students_many_courses(self):
        inp = ['create student paul',
               'create student david',
               'create student jen',
               'enrol paul CSC108',
               'enrol david CSC148',
               'enrol jen CSC207',
               'class-list CSC148',
               'exit']
        exp = ['david', '']
        self.io_tester(inp, exp)

    def test_students_many_courses_mixed(self):
        inp = ['create student paul',
               'create student david',
               'create student jen',
               'enrol paul CSC108',
               'enrol david CSC148',
               'enrol jen CSC207',
               'class-list CSC148',
               'class-list CSC108',
               'enrol jen CSC108',
               'class-list CSC108',
               'drop paul CSC108',
               'class-list CSC108',
               'exit']
        exp = ['david',
               'paul',
               'jen, paul',
               'jen',
               '']
        self.io_tester(inp, exp)

    def test_invalid(self):
        inp = ['class-list',
               'class-list csc148 csc324',
               'exit']
        exp = ['Unrecognized command!',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)

class TestUndo(TestSMS):
    """
    Test undo.
    """

    def test_no_command_to_undo(self):
        inp = ['undo', 'exit']
        exp = ['ERROR: No commands to undo.', '']
        self.io_tester(inp, exp)

    def test_undo_creation(self):
        inp = ['create student david',
               'undo',
               'create student david',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_undo_enrol(self):
        inp = ['create student david',
               'enrol david CSC148',
               'undo',
               'enrol david CSC148',
               'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_undo_failed(self):
        inp = ['create student david',
               'create student david',
               'undo',
               'create student david',
               'exit']
        exp = ['ERROR: Student david already exists.',
               'ERROR: Student david already exists.', '']
        self.io_tester(inp, exp)

    def test_undo_enrol_thorough(self):
        students = self.create_n_students(30)
        create = ['create student {}'.format(name) for name in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        enroll = 'enrol {} CSC148'.format(students[29])
        inp = create + enrollms + ['undo', enroll, 'exit']
        exp = ['']
        self.io_tester(inp, exp)

    def test_undo_drop(self):
        inp = ['create student david',
               'enrol david CSC148',
               'drop david CSC148',
               'class-list CSC148',
               'undo',
               'undo',
               'class-list CSC148',
               'exit']
        exp = ['No one is taking CSC148.', 'david', '']
        self.io_tester(inp, exp)

    def test_undo_drop_thorough(self):
        students = self.create_n_students(30)
        create = ['create student {}'.format(name) for name in students]
        enrollms = ['enrol {} CSC148'.format(name) for name in students]
        drop = 'drop {} CSC148'.format(students[0])
        create_david = 'create student david'
        enroll = 'enrol david CSC148'
        inp = create + enrollms + [drop,
                                   'undo',
                                   create_david,
                                   enroll,
                                   'exit']
        exp = ['ERROR: Course CSC148 is full.', '']
        self.io_tester(inp, exp)

    def test_undo_no_data_change(self):
        inp = ['class-list CSC148',
               'undo',
               'exit']
        exp = ['No one is taking CSC148.', '']
        self.io_tester(inp, exp)

    def test_undo_no_data_change_thorough(self):
        inp = ['create student david',
               'class-list CSC148',
               'undo',
               'create student david',
               'exit']
        exp = ['No one is taking CSC148.',
               'ERROR: Student david already exists.', '']
        self.io_tester(inp, exp)

    def test_undo_many(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student diane',
               'create student jen',
               'create student paul',
               'enrol diane CSC148',
               'enrol jen CSC148',
               'enrol paul CSC148',
               'undo',
               'undo',
               'undo',
               'class-list CSC148',
               'exit']
        exp = ['david', '']
        self.io_tester(inp, exp)

    def test_undo_many_n(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student diane',
               'create student jen',
               'create student paul',
               'enrol diane CSC148',
               'enrol jen CSC148',
               'enrol paul CSC148',
               'undo 3',
               'class-list CSC148',
               'exit']
        exp = ['david', '']
        self.io_tester(inp, exp)

    def test_undo_many_with_ignored(self):
        inp = ['create student david',
               'enrol david CSC148',
               'create student diane',
               'create student jen',
               'create student paul',
               'enrol diane CSC148',
               'class-list CSC148',
               'enrol paul CSC148',
               'undo',
               'undo',
               'class-list CSC148',
               'exit']
        exp = ['david, diane', 'david, diane', '']
        self.io_tester(inp, exp)

    def test_undo_second_enroll(self):
        inp = ['create student david',
               'create student',
               'enrol david CSC148',
               'enrol david CSC148',
               'undo',
               'class-list CSC148',
               'exit']
        exp = ['Unrecognized command!',
               'david',
               '']
        self.io_tester(inp, exp)

    # TODO: new test
    def test_undo_second_drop(self):
        inp = ['create student david',
               'create student',
               'enrol david CSC148',
               'drop david CSC148',
               'drop david CSC148',
               'undo',
               'class-list CSC148',
               'exit']
        exp = ['Unrecognized command!',
               'No one is taking CSC148.',
               '']
        self.io_tester(inp, exp)

    def test_non_consecutive(self):
        inp = ['create student david',
               'enrol david CSC148',
               'undo',
               'enrol david CSC148',
               'undo',
               'undo',
               'create student david',
               'class-list CSC148',
               'exit']
        exp = ['No one is taking CSC148.', '']
        self.io_tester(inp, exp)

    def test_non_consecutive_complex(self):
        inp = ['create student david',
               'create student diane',
               'undo 1',
               'create student diane',
               'enrol david CSC108',
               'enrol david CSC108',
               'enrol diane CSC108',
               'common-courses david diane',
               'class-list CSC108',
               'undo 3',
               'undo',
               'class-list CSC108',
               'undo 4',
               'undo',
               'exit']
        exp = ['CSC108', 'david, diane', 'david',
               'ERROR: No commands to undo.',
               '']
        self.io_tester(inp, exp)

    def test_many_not_enough_commands(self):
        inp = ['create student david',
               'undo 4',
               'create student david',
               'exit']
        exp = ['ERROR: No commands to undo.', '']
        self.io_tester(inp, exp)

    def test_invalid_numbers(self):
        inp = ['undo -1',
               'undo 0',
               'exit']
        exp = ['ERROR: -1 is not a positive natural number.',
               'ERROR: 0 is not a positive natural number.',
               '']
        self.io_tester(inp, exp)

    def test_invalid_string(self):
        inp = ['undo hi',
               'undo hi hi',
               'exit']
        exp = ['ERROR: hi is not a positive natural number.',
               'Unrecognized command!',
               '']
        self.io_tester(inp, exp)


class TestMixedCommands(TestSMS):
    def test1(self):
        inp = ['create student',
               'create student david',
               'enrol david CSC148',
               'enrol david CSC148',
               'drop david CSC148',
               'class-list CSC148',
               'undo',
               'class-list CSC148',
               'enrol david CSC108',
               'list-courses david',
               'list-courses',
               'lst-courses',
               'drop david CSC18',
               'drop CSC18 david',
               'undo',
               'drop david CSC148',
               'undo',
               'list-courses david',
               'exit']
        exp = ['Unrecognized command!',
               'No one is taking CSC148.',
               'No one is taking CSC148.',
               'david is taking CSC108',
               'Unrecognized command!',
               'Unrecognized command!',
               'ERROR: Student CSC18 does not exist.',
               'david is taking CSC108',
               '']
        self.io_tester(inp, exp)

    def test2(self):
        inp = ['create student david',
               'enrol david CSC148',
               'common-courses david david',
               'enrol david CSC108',
               'common-courses david david',
               'common-courses david diane',
               'list-courses diane',
               'create student diane',
               'enrol diane CSC343',
               'common-courses david diane',
               'enrol david CSC343',
               'course-list CSC343',
               'class-list CSC343',
               'exit']
        exp = ['CSC148',
               'CSC108, CSC148',
               'ERROR: Student diane does not exist.',
               'ERROR: Student diane does not exist.',
               '',
               'Unrecognized command!',
               'david, diane',
               '']
        self.io_tester(inp, exp)

    def test3(self):
        inp = ['create student david',
               'undo',
               'create student david',
               'drop david CSC108',
               'enrol david CSC108',
               'list-courses david',
               'class-list CSC148',
               'class-list CSC108',
               'enrol david CSC108',
               'invalid',
               'class-list CSC108',
               'enrol david MAT223',
               'enrol david MAT137',
               'drop david CSC108',
               'create student diane',
               'enrol diane MAT137',
               'enrol diane',
               'common-courses diane david',
               'exit']
        exp = ['david is taking CSC108',
               'No one is taking CSC148.',
               'david',
               'Unrecognized command!',
               'david',
               'Unrecognized command!',
               'MAT137',
               '']
        self.io_tester(inp, exp)

    def test4(self):
        inp = ['create student david',
               'undo',
               'create student david',
               'drop david CSC108',
               'enrol david CSC108',
               'list-courses david',
               'class-list CSC148',
               'class-list CSC108',
               'enrol david CSC108',
               'class-list CSC108',
               'enrol david MAT223',
               'enrol david MAT137',
               'drop david CSC108',
               'drop david',
               'undo',
               'create student diane',
               'enrol diane MAT137',
               'common-courses diane david',
               'exit']
        exp = ['david is taking CSC108',
               'No one is taking CSC148.',
               'david',
               'david',
               'Unrecognized command!',
               'MAT137',
               '']
        self.io_tester(inp, exp)

    def test5(self):
        inp = (['undo',
               'class-list CSC148',
               'enrol david CSC148',
               'create studnet david',
               'drop david CSC148',
               'create student david'] +
              ['create student s{}'.format(i) for i in range(30)] +
              ['enrol s{} CSC148'.format(i) for i in range(30)] +
               ['enrol david CSC148',
                'enrol david CSC343',
                'list-courses david',
                'class-list CSC148',
               'exit'])
        exp = ['ERROR: No commands to undo.',
               'No one is taking CSC148.',
               'ERROR: Student david does not exist.',
               'Unrecognized command!',
               'ERROR: Student david does not exist.',
               'ERROR: Course CSC148 is full.',
               'david is taking CSC343',
               ', '.join(sorted(['s{}'.format(i) for i in range(30)])),
               '']
        self.io_tester(inp, exp)


if __name__ == '__main__':
    unittest.main(exit=False)
