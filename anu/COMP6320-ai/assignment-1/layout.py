# layout.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file defines a Layout which is read from a file. The Layout class
    contains static information about the game.

    We have structured this assignment so that you should not need to access
    this information directly.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import os
import random


class Layout:
    """ A Layout manages the static information about the game board. """

    def get_width(self):
        """ Return the width of the game board.
            (Layout) -> int
        """
        return self.width

    def get_height(self):
        """ Return the height of the game board.
            (Layout) -> int
        """
        return self.height

    def get_walls(self):
        """ Return the walls of the game board.
            (Layout) -> [[bool]]
        """
        return self.walls

    def is_wall(self, pos):
        """ Return iff a given position is a wall.
            (Layout, (int, int)) -> bool
        """
        return self.walls[pos[0]][pos[1]]

    def get_maze_distances(self):
        """ Return the dictionary holding the shortest distances between positions.
            (Layout) -> {(int, int) : int}
        """
        return self.distance

    def has_black_bird(self):
        """ Return iff there is a black bird in the maze.
            (Layout) -> int
        """
        return self.black_bird_position is not None

    def __init__(self, layout_text):
        """ Initialise the layout from the given layout text.
            (Layout, str) -> None
        """
        self.width = len(layout_text[0])
        self.height = len(layout_text)
        self.walls = [[False for y in range(self.height)]
                      for x in range(self.width)]
        self.yellow_birds = []
        self.red_bird_position = None
        self.black_bird_position = None
        self.distance = {}
        self.process_layout_text(layout_text)
        self.layout_text = layout_text

    def __str__(self):
        """ Return the string representation of the layout that we read in.
            (Layout) -> str
        """
        return "\n".join(self.layout_text)

    def deepcopy(self):
        """ Return a new layout that is a copy of this one.
            (Layout) -> Layout
        """
        return Layout(self.layout_text[:])

    def process_layout_text(self, layout_text):
        """ Coordinates are flipped from the input format to the (x,y) convention here
        The shape of the maze. Each character represents a different type of object.
         % - Wall
         . - yellow_bird
         B - BlackBird
         R - RedBird
         Other characters are ignored.
        """
        max_y = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                layout_char = layout_text[max_y - y][x]
                if layout_char == "%":
                    self.walls[x][y] = True
                elif layout_char == ".":
                    self.yellow_birds.append(pos)
                elif layout_char == "R":
                    self.red_bird_position = pos
                elif layout_char == "B":
                    self.black_bird_position = pos
        self.yellow_birds = tuple(sorted(self.yellow_birds))

    def save_maze_distances(self, dist_text):
        """ Save the maze distances given in dist_text.
            (Layout, [[str]]) -> None
        """
        dist_text = iter(dist_text)
        for x1 in range(self.width):
            for y1 in range(self.height):
                if self.walls[x1][y1]:
                    continue
                pos1 = (x1, y1)
                for x2 in range(self.width):
                    for y2 in range(self.height):
                        if self.walls[x2][y2]:
                            continue
                        self.distance[(pos1, (x2, y2))] = int(
                            next(dist_text).strip())


def get_layout(name, back=2):
    """ Try to load a layout with the given name from the various places we
        might expect to find it relative to where the system is run from.
        Back specified how many layers up from the current path we are willing
        to look. Return None on failure.
        (str, int) -> Layout
    """
    if name.endswith('.lay'):
        layout = try_to_load('layouts/' + name)
        if layout == None:
            layout = try_to_load(name)
    else:
        layout = try_to_load('layouts/' + name + '.lay')
        if layout == None:
            layout = try_to_load(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = get_layout(name, back - 1)
        os.chdir(curdir)
    return layout


def try_to_load(full_name):
    """ Try to load the file with the name specified by full name.
        Return the resulting Layout or None on failure.

        (str) -> Layout
    """
    if(not os.path.exists(full_name)):
        return None
    f = open(full_name)
    try:
        lay = Layout([line.strip() for line in f])
        distance_file = full_name[:-4]+".dst"
        if os.path.exists(distance_file):
            with open(distance_file) as d_file:
                lay.save_maze_distances([l.strip() for l in d_file])
        return lay
    finally:
        f.close()
