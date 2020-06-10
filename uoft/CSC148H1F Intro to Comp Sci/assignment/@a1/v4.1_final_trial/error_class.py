class StudentAlreadyExistsError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'ERROR: Student {0} already exists.'.format(name)


class StudentNotExistError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'ERROR: Student {0} does not exist.'.format(name)


class Student2NotExistError(Exception):
    pass


class BothStudentsNotExistError(Exception):
    pass


class FullCourseError(Exception):

    def __init__(self, course):
        self.course = course

    def __str__(self):
        return 'ERROR: Course {0} is full.'.format(course)


class NoCommandsUndoError(Exception):

    def __str__(self):
        return 'ERROR: No commands to undo.'


class NotNaturalNumberUndoError(Exception):

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return 'ERROR: {0} is not a positive natural number.'.format(n)
