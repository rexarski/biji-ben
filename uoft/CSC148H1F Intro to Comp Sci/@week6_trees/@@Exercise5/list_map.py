# Exercise 5 - Recursive Linked Lists
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
# Rui Qiu, qiurui2
# ---------------------------------------------
from linkedlistrec import LinkedListRec


def map_f(linked_list, f):
    """ (LinkedListRec, function) -> LinkedListRec

    Return a new recursive linked list whose items
    are obtained by applying f to the items in linked_list.

    Your implementation should access the attributes
    of the LinkedListRec class directly, and may not use
    any LinkedListRec methods other than the constructor
    and is_empty.
    """
    new_list = LinkedListRec([])
    if linked_list.is_empty():
        return linked_list
    else:
        new_list.first = f(linked_list.first)
        new_list.rest = map_f(linked_list.rest, f)
        return new_list
