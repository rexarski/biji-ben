# Exercise 5 - Family Tree
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
#
# ---------------------------------------------


class Person:
    """Person class.

    Attributes:
    - name (str): The name of this Person
    - children (list of Person): a list of the Person objects who
                                 are the children of this Person
    """

    def __init__(self, name):
        """ (Person, str) -> NoneType
        Create a new person with the given name, and no children.
        """
        self.name = name
        self.children = []

    def count_descendants(self):
        """ (Person) -> int
        Return the number of descendants of self.
        """
        num = 0
        if len(self.children) == 0:
            return num
        else:
            num += len(self.children)
            for name in self.children:
                num += name.count_descendants()
            return num
