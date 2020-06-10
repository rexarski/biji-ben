# Assignment 2 - Course Planning!
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
"""Course prerequisite data structure.

This module contains the class that should store all of the
data about course prerequisites and track taken courses.
Note that by tracking "taken" courses, we are restricting the use
of this class to be one instance per student (otherwise,
"taken" doesn't make sense).

Course: a course and its prerequisites.
"""


class Course:
    """A tree representing a course and its prerequisites.

    This class not only tracks the underlying prerequisite relationships,
    but also can change over time by allowing courses to be "taken".

    Attributes:
    - name (str): the name of the course
    - prereqs (list of Course): a list of the course's prerequisites
    - taken (bool): represents whether the course has been taken or not
    """

    # Core Methods - implement all of these
    def __init__(self, name, prereqs=None):
        """ (Course, str, list of Courses) -> NoneType

        Create a new course with given name and prerequisites.
        By default, the course has no prerequisites (represent this
        with an empty list, NOT None).
        The newly created course is not taken.
        """
        self.name=name
        if prereqs==None:
            self.prereqs = []
        else:
            self.prereqs = prereqs
        self.taken = False;

    def is_takeable(self):
        """ (Course) -> bool

        Return True if the user can take this course.
        A course is takeable if and only if all of its prerequisites are taken.
        """
        return False not in [prereq.taken for prereq in self.prereqs]

    def take(self):
        """ (Course) -> NoneType

        If this course is takeable, change self.taken to True.
        Do nothing if self.taken is already True.
        Raise UntakeableError if this course is not takeable.
        """
        if self.is_takeable() and self.taken != True:
            self.taken = True
        else:
            raise UntakeableError()

    def add_prereq(self, prereq):
        """ (Course, Course) -> NoneType

        Add a prereq as a new prerequisite for this course.

        Raise PrerequisiteError if either:
        - prereq has this course in its prerequisite tree, or
        - this course already has prereq in its prerequisite tree
        """
        if prereq in self.prereqs or self in prereq.prereqs:
            raise PrerequisiteError
        else:
            self.prereqs.append(prereq)
        

    def missing_prereqs(self):
        """ (Course) -> list of str

        Return a list of all of the names of the prerequisites of this course
        that are not taken.

        **Clarification: this method should be recursive, i.e., if self has a
        missing prerequisite course CSC148, and CSC148 has a missing 
        prerequisite CSC108, then both "CSC108" and "CSC148" should appear in
        the returned list.**

        The returned list should be in alphabetical order, and should be empty
        if this course is not missing any prerequisites.
        """
        missingList = []
        for prereq in self.prereqs:
            missingList.append(prereq.missing_prereqs())
        return sorted(missingList)
    
class UntakeableError(Exception):
    pass
    
class PrerequisiteError(Exception):
    pass

class AlreadyTakenError(Exception):
    pass