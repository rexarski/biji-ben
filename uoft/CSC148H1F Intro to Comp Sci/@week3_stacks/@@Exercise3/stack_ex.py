# Exercise 3: More Stack Exercises
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
from stack import Stack, EmptyStackError

class SmallStackError(Exception):
    print("The stack has fewer than two elements.")

def reverse_top_two(stack):
    """ (Stack) -> NoneType

    Reverse the top two elements on stack.
    Raise a SmallStackError if stack has fewer than two elements.

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse_top_two(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    try:
        stack.is_empty() == False
    except:
        raise EmptyStackError
    else:
        try:
            t1 = stack.pop()
            t2 = stack.pop()
            stack.push(t1)
            stack.push(t2)
        except:
            raise SmallStackError
        return stack
    

def reverse(stack):
    """ (Stack) -> NoneType

    Reverse all the elements of stack.

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    
    temp = Stack()
    temp2 = Stack()
    while not stack.is_empty():
        stuff = stack.pop()
        temp.push(stuff)
    while not temp.is_empty():
        stuff = temp.pop()
        temp2.push(stuff)
    while not temp2.is_empty():
        stuff = temp2.pop()
        stack.push(stuff)
    return stack