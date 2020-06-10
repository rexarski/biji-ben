# Exercise 1, Task 1: Runtime Errors
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
#
# <Rui Qiu>, <999292509>
# ---------------------------------------------
"""Exercise 1, Task 1: Runtime Errors."""


def bad_type():
    """When run, produces a TypeError."""
    a = 0
    b = 'thiswouldfaillol'
    return a + b


def bad_name():
    """When run, produces a NameError."""
    return this_does_not_exist


def bad_attribute():
    """When run, produces an AttributeError."""
    should_be_str = 9 
    return should_be_str.append(999)


def bad_index():
    """When run, produces an IndexError."""
    i_am_a_long_word = 'rui'
    return i_am_a_long_word[25]


def bad_key():
    """When run, produces a KeyError."""
    food_in_timmy = {'doubledouble': 'tasty', 'icedcapp': 'cool'}
    return food_in_timmy['bigmac']


def bad_zero():
    """When run, produces a ZeroDivisionError."""
    return 8/0


def bad_import():
    """When run, produces an ImportError."""
    import RobFord
    