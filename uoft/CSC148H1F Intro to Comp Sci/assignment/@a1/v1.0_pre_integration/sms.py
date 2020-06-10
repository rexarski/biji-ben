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
    
    UOFT = School('University of Toronto')
    
    while True:
        command = input('')

        if command == 'exit':
            break
        elif command == 'undo':
            pass # call undo function
        else:
            clist = command.split()
            if len(clist) == 3:
                if clist[0:1] == ['create', 'student']:
                    pass # call create student function
                elif clist[0] == 'enrol':
                    pass # call enrol function
                elif clist[0] == 'common-courses':
                    pass # call common-courses function
                else:
                    print('Unrecognized command!')
                    UOFT.undo_stack.push(1)
            elif len(clist) == 2:
                if clist[0] == 'list-courses':
                    pass # call list-courses function
                elif clist[0] == 'class-list':
                    pass # call class-list function
                elif clist[0] == 'undo':
                    pass # call undo n function
                else:
                    print('Unrecognized command!')
                    UOFT.undo_stack.push(1)
            else:
                print('Unrecognized command!')
                UOFT.undo_stack.push(1)


if __name__ == '__main__':
    run()
