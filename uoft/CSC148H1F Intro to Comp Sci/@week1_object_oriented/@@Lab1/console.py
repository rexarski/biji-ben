# Lab 1 - Python (Re-)Introduction
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Lab 1: interactive console.

This module contains a script to run an interactive console,
in which the user types in commands and sees results.
Your task is to add to the (very bare) functionality.
"""

import sys

# Constants in Python generally named with ALL_CAPS
EASTER_EGG = 'I\'m giving up on you'
EASTER_EGG_RESPONSE = 'That\'s not very nice!'


def start_interaction():
    """ () -> NoneType

    Begin an infinite loop that repeatedly asks for a command
    and then executes an action.
    """

    # Loop infinitely
    while True:
        # Prints 'Say something: ' and then waits for user input
        # Note: line gets a string value
        line = input('Say something: ')

        # Right now, not very interesting...?
        if line == EASTER_EGG:
            print(EASTER_EGG_RESPONSE)
        else:
            print(repeat(line))


def repeat(s):
    """ (str) -> str

    Return a string identical to the input.
    Note the difference between *returning* a string and printing it out!

    Params
    - s: string to repeat
    """

    return s


# This is the main function; called when program is run.
if __name__ == '__main__':
    start_interaction()
