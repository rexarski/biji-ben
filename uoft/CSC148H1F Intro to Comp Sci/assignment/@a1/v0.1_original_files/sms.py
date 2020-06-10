# Assignment 1 - Managing students!
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
"""Interactive console for assignment.

This module contains the code necessary for running the interactive console.
As provided, the console does nothing interesting: it is your job to build
on it to fulfill all the given specifications.

run: Run the main interactive loop.
"""


def run():
    """ (NoneType) -> NoneType

    Run the main interactive loop.
    """

    while True:
        command = input('')

        if command == 'exit':
            break
        else:
            print(command)


if __name__ == '__main__':
    run()
