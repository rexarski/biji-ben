# Exercise 2: Stack Preview
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
# <Rui Qiu>, <999292509>
# ---------------------------------------------

# This import will fail unless you've downloaded
# the stack.pyc file from the website
from stack import Stack


def remove_second(stack):
    """ (Stack) -> object

    Remove and return the second-highest item on stack.
    You may assume that stack always has at least two items.

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(10)
    >>> stack.push(30)
    >>> stack.push(40)
    >>> remove_second(stack)
    30 # Second most recent element added
    >>> stack.pop()
    40 # Top element remains unchanged
    >>> stack.pop()
    10 # Next element is now 10; the 30 has been removed
    >>> stack.pop()
    1
    >>> stack.is_empty()
    True
    """

    # YOUR CODE GOES HERE
    # HINT: this requires no more than a few lines of code.
    # If you're stuck, first try removing the top two elements.
    
    temp = stack.pop()
    result = stack.pop()
    stack.push(temp)
    return result
