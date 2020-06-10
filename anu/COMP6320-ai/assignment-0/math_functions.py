""" File name:   math_functions.py
    Author:      Rui Qiu
    Date:        23 Feb, 2018
    Description: This file defines a set of variables and simple functions.

                 It should be implemented for Exercise 1 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""

import math

ln_e = math.log(math.exp(1))  # The natural logarithm of e.

twenty_radians = math.radians(20)  # 20 degree angle in radians.


def quotient_ceil(numerator, denominator):
    """ Return the ceiling of a division.

    :param numerator: A floating number or integer as numerator.
    :param denominator: A floating number or integer as denominator.
    :return: An integer.
    """

    return int(math.ceil(numerator / denominator))


def quotient_floor(numerator, denominator):
    """ Return the floor of a division.

    :param numerator: A floating number or integer as numerator.
    :param denominator: A floating number or integer as denominator.
    :return: An integer.
    """

    return int(math.floor(numerator / denominator))


def manhattan(x1, y1, x2, y2):
    """ Return the Manhattan distance between two 2-dimension points.

    :param x1: The x-value of point (x1, y1).
    :param y1: The y-value of point (x1, y1).
    :param x2: The x-value of point (x2, y2).
    :param y2: The y-value of point (x2, y2).
    :return: An floating number or an integer as the Manhattan distance
    between two points.
    """

    return abs(x1-x2)+abs(y1-y2)
