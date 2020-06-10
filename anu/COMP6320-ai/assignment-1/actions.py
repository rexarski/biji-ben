# actions.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file defines the classes Directions and Actions.

    In this system actions are directions which an agent can travel. These are
    represented as strings as defined in the Directions class.

    Both of these classes are used statically throughout the code whenever we are
    working with actions (which are stored as strings representing directions).

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""


class Directions:
    """ Actions representing the directions that can be moved. """

    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST:  NORTH,
            WEST:  SOUTH,
            STOP:  STOP}

    RIGHT = dict([(y, x) for x, y in list(LEFT.items())])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}


class Actions:
    """ A collection of static methods for manipulating move actions. """

    directions = {Directions.NORTH: (0, 1),
                  Directions.SOUTH: (0, -1),
                  Directions.EAST:  (1, 0),
                  Directions.WEST:  (-1, 0),
                  Directions.STOP:  (0, 0)}

    directions_list = list(directions.items())

    @staticmethod
    def get_legal_actions(pos, walls):
        """ Return the legal actions for a given position, given the wall matrix
            and position of the other agent.
            ((int, int), [[bool]]) -> [str]
        """
        x, y = pos
        possible = []
        for dir, vec in Actions.directions_list:
            next_x = x + vec[0]
            if next_x < 0 or next_x == len(walls):
                continue
            next_y = y + vec[1]
            if next_y < 0 or next_y == len(walls[0]):
                continue
            if not walls[next_x][next_y]:
                possible.append(dir)
        return possible

    @staticmethod
    def get_successor(pos, action):
        """ Return the successor position to pos for the given action.
            ((int, int), str) -> (int, int)
        """
        dx, dy = Actions.directions[action]
        x, y = pos
        return (x + dx, y + dy)
