""" File name:   truth_tables.py
    Author:      Rui Qiu
    Date:        23 Feb, 2018
    Description: This file defines a number of functions which implement
                 Boolean expressions.

                 It also defines a function to generate and print truth tables
                 using these functions.

                 It should be implemented for Exercise 2 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""


def boolean_fn1(a, b, c):
    """ Return the truth value of (a ∨ b) → (-a ∧ -b)

    :param a: Boolean.
    :param b: Boolean.
    :param c: Boolean.
    :return: Truth value of (a ∨ b) → (-a ∧ -b).
    """

    left = a or b
    right = not a and not b
    return (not left) or right


def boolean_fn2(a, b, c):
    """ Return the truth value of (a ∧ b) ∨ (-a ∧ -b)

    :param a: Boolean.
    :param b: Boolean.
    :param c: Boolean.
    :return: Truth value of (a ∧ b) ∨ (-a ∧ -b).
    """

    return (a and b) or (not a and (not b))


def boolean_fn3(a, b, c):
    """ Return the truth value of ((c → a) ∧ (a ∧ -b)) ∨ (-a ∧ b)

    :param a: Boolean.
    :param b: Boolean.
    :param c: Boolean.
    :return: Truth value of ((c → a) ∧ (a ∧ -b)) ∨ (-a ∧ b)
    """

    first = not c or a
    return first and (a and not b) or (not a and b)


def draw_truth_table(boolean_fn):
    """ This function prints a truth table for the given boolean function.
        It is assumed that the supplied function has three arguments.

        ((bool, bool, bool) -> bool) -> None

        If your function is working correctly, your console output should look
        like this:

        >>> from truth_tables import *
        >>> draw_truth_table(boolean_fn1)
        a     b     c     res
        -----------------------
        True  True  True  False
        True  True  False False
        True  False True  False
        True  False False False
        False True  True  False
        False True  False False
        False False True  True
        False False False True

    :param boolean_fn: A pre-defined function which takes 3 boolean variables
    as input.
    :return: A string displayed as a truth table which includes all the
    combinations of
    input values, and the corresponding truth values of that Boolean formula.
    """

    combo = [(x, y, z) for x in [True, False] for y in [True, False]
             for z in [True, False]]

    print(
        "a     b     c     res\n"
        "-----------------------\n"
        "True  True  True  "+str(boolean_fn(
            combo[0][0], combo[0][1], combo[0][2]))+"\n"
        "True  True  False "+str(boolean_fn(
            combo[1][0], combo[1][1], combo[1][2]))+"\n"
        "True  False True  "+str(boolean_fn(
            combo[2][0], combo[2][1], combo[2][2]))+"\n"
        "True  False False "+str(boolean_fn(
            combo[3][0], combo[3][1], combo[3][2]))+"\n"
        "False True  True  "+str(boolean_fn(
            combo[4][0], combo[4][1], combo[4][2]))+"\n"
        "False True  False "+str(boolean_fn(
            combo[5][0], combo[5][1], combo[5][2]))+"\n"
        "False False True  "+str(boolean_fn(
            combo[6][0], combo[6][1], combo[6][2]))+"\n"
        "False False False "+str(boolean_fn(
            combo[7][0], combo[7][1], combo[7][2])))
