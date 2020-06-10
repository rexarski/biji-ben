'''
Special Extra Module used to store various Error Classes
'''


# If student already exists (for student create)
class StudentAlreadyExistsError(Exception):
    pass


# If student does not exist
class StudentNotExistError(Exception):
    pass


# Student2 and BothStudent not exist are for common-courses functions
class Student2NotExistError(Exception):
    pass


class BothStudentsNotExistError(Exception):
    pass


# If course is full (enrolment)
class FullCourseError(Exception):
    pass


# If there are no more courses to undo
class NoCommandsUndoError(Exception):
    pass


# If not a natural number.
class NotNaturalNumberUndoError(Exception):
    pass
