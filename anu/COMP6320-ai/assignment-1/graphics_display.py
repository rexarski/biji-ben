# graphics_display.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file uses graphics_utils to draw the game onto the screen.

    You really don't need to look into here unless you happen to want to make
    the circles look more like birds or want to make an animation out of
    the game play.

    If you want to make an animation, look at the save_frame function at the
    bottom of this file. You should put calls to it in the run method of the
    Game class.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import math
import os
import time

from actions import Directions
from graphics_utils import *

DEFAULT_GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = format_color(20.0/255.0, 20.0/255.0, 20.0/255.0)
WALL_COLOR = format_color(255.0/255.0, 255.0/255.0, 255.0/255.0)
INFO_PANE_COLOR = format_color(0, .0, 0)
SCORE_COLOR = format_color(.0, .0, .0)
REDBIRD_OUTLINE_WIDTH = 2

BLACK_BIRD_COLORS = []
BLACK_BIRD_COLORS.append(format_color(.9, 0, 0))  # Red
BLACK_BIRD_COLORS.append(format_color(0, .3, .9))  # Blue
BLACK_BIRD_COLORS.append(format_color(.98, .41, .07))  # Orange
BLACK_BIRD_COLORS.append(format_color(.1, .75, .7))  # Green
BLACK_BIRD_COLORS.append(format_color(1.0, 0.6, 0.0))  # Yellow
BLACK_BIRD_COLORS.append(format_color(.4, 0.13, 0.91))  # Purple

BLACK_COLOR = format_color(.0, .0, .0)
WHITE_COLOR = format_color(255, 255, 255)

BLACK_BIRD_SHAPE = [
    (0,    0.3),
    (0.25, 0.75),
    (0.5,  0.3),
    (0.75, 0.75),
    (0.75, -0.5),
    (0.5,  -0.75),
    (-0.5,  -0.75),
    (-0.75, -0.5),
    (-0.75, 0.75),
    (-0.5,  0.3),
    (-0.25, 0.75)
]
BLACK_BIRD_SCALE = 0.4

BLACK_BIRD_VEC_COLORS = list(map(color_to_vector, BLACK_BIRD_COLORS))

REDBIRD_COLOR = format_color(255.0/255.0, .0, .0)
# format_color(255.0/255.0,255.0/255.0,61.0/255)
REDBIRD_SCALE = 0.35
#red_bird_speed = 0.25

# YellowBird
YELLOWBIRD_COLOR = format_color(1, 1, 0)
YELLOWBIRD_SIZE = 0.3

# Drawing walls
WALL_RADIUS = 0.2


class InfoPane:
    """ The info pane displays relevant information at the bottom of the screen. """

    def __init__(self, layout, grid_size):
        """ Make a new InfoPane with the given layout.
            (InfoPane, Layout, int) -> None
        """
        self.grid_size = grid_size
        self.width = (layout.width) * grid_size
        self.base = (layout.height + 1) * grid_size
        self.height = INFO_PANE_HEIGHT
        self.font_size = 18
        self.text_color = format_color(255, 255, 255)
        self.draw_pane()

    def to_screen(self, pos, y=None):
        """ Translates a point relative from the bottom left of the info pane.
            (InfoPane, (int, int), int) -> (int, int)
        """
        if y is None:
            x, y = pos
        else:
            x = pos
        x = self.grid_size + x  # Margin
        y = self.base + y
        return x, y

    def draw_pane(self):
        """ Draw the InfoPane.
            (InfoPane) -> None
        """
        self.score_text = text(self.to_screen(0, 0), self.text_color,
                               "SCORE:    0", "Helvetica", self.font_size, "bold")

    def update_score(self, score):
        """ Update the score text to the given score.
            (InfoPane, float) -> None
        """
        change_text(self.score_text, "SCORE: % 4d" % score)

    def draw_black_bird(self):
        pass

    def draw_red_bird(self):
        pass

    def draw_warning(self):
        pass

    def clear_icon(self):
        pass

    def update_message(self, message):
        pass

    def clear_message(self):
        pass


class RedBirdGraphics:
    """ Is responsible for managing the grapics of the simulation."""

    def __init__(self, zoom=1.0, frame_time=0.0):
        """ Make a new RedBirdGraphics
            (RedBirdGraphics, float, bool) -> None
        """
        self.have_window = 0
        self.current_black_bird_images = {}
        self.red_bird_image = None
        self.zoom = zoom
        self.grid_size = DEFAULT_GRID_SIZE * zoom
        self.frame_time = frame_time

    def initialise(self, state):
        """ Initialise the display_window. """
        self.start_graphics(state)
        self.draw_static_objects(state)
        self.draw_state_objects(state)
        # Information
        self.previous_state = state

    def start_graphics(self, state):
        """ Start the graphics engine """
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.info_pane = InfoPane(layout, self.grid_size)
        self.currentState = layout

    def draw_static_objects(self, state):
        """ Draw those parts of the problem that don't change. I.e. the walls.
            (RedBirdGraphics, State) -> None
        """
        self.draw_walls(self.layout.walls)
        refresh()

    def draw_state_objects(self, state):
        """ Draw those parts of the problem that are in the state.
            That is, the agents and the yellow birds.
        """
        self.agent_images = []  # ((int, int), image)
        red_bird_pos = state.get_red_bird_position()
        self.agent_images.append(
            (red_bird_pos, self.draw_red_bird(red_bird_pos)))
        black_bird_pos = state.get_black_bird_position()
        if black_bird_pos is not None:
            self.agent_images.append(
                (black_bird_pos, self.draw_black_bird(black_bird_pos)))
        self.yellow_birds = self.draw_yellow_bird(state.yellow_birds)

        refresh()

    def swap_images(self, agent_index, new_pos):
        """
          Changes an image from a black_bird to a red_bird or vis versa (for capture)
        """
        prev_state, prev_image = self.agent_images[agent_index]
        for item in prev_image:
            remove_from_screen(item)
        if agent_index == 0:
            self.agent_images[agent_index] = (
                new_pos, self.draw_red_bird(new_pos))
        else:
            self.agent_images[agent_index] = (
                new_pos, self.draw_black_bird(new_pos))
        refresh()

    def update(self, new_state, agent_index):
        prev_pos, prev_image = self.agent_images[agent_index]

        if agent_index == 0:
            agent_pos = new_state.red_bird_position
        else:
            agent_pos = new_state.black_bird_position
        self.animate_bird(agent_index, agent_pos, prev_pos, prev_image)
        self.agent_images[agent_index] = (agent_pos, prev_image)

        if new_state._yellow_bird_eaten is not None:
            self.remove_yellow_bird(
                new_state._yellow_bird_eaten, self.yellow_birds)

        self.info_pane.update_score(new_state.score)

    def make_window(self, width, height):
        grid_width = (width-1) * self.grid_size
        grid_height = (height-1) * self.grid_size
        screen_width = 2*self.grid_size + grid_width
        screen_height = 2*self.grid_size + grid_height + INFO_PANE_HEIGHT

        begin_graphics(screen_width,
                       screen_height,
                       BACKGROUND_COLOR,
                       "COMP3620/6320 Search")

    def draw_red_bird(self, pos):
        """ Draw the red bird in the given position.

            (RedBirdGraphics, (int, int)) -> None
        """
        return [circle(self.to_screen(pos), REDBIRD_SCALE * self.grid_size,
                       fill_color=REDBIRD_COLOR, outline_color=REDBIRD_COLOR,
                       endpoints=None,
                       width=REDBIRD_OUTLINE_WIDTH)]

    def get_endpoints(self, direction, position=(0, 0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi * pos)

        delta = width / 2
        if (direction == 'West'):
            endpoints = (180+delta, 180-delta)
        elif (direction == 'North'):
            endpoints = (90+delta, 90-delta)
        elif (direction == 'South'):
            endpoints = (270+delta, 270-delta)
        else:
            endpoints = (0+delta, 0-delta)
        return endpoints

    def move_red_bird(self, position, image):
        screen_position = self.to_screen(position)
        r = REDBIRD_SCALE * self.grid_size
        move_circle(image[0], screen_position, r)
        refresh()

    def animate_bird(self, agent_id, bird, prev_bird, image):
        if self.frame_time < 0:
            print('Press any key to step forward, "q" to play')
            keys = wait_for_keys()
            if 'q' in keys:
                self.frame_time = 0.1
        if self.frame_time > 0.01 or self.frame_time < 0:
            start = time.time()
            fx, fy = prev_bird
            px, py = bird
            frames = 4.0
            for i in range(1, int(frames) + 1):
                pos = px*i/frames + fx * \
                    (frames-i)/frames, py*i/frames + fy*(frames-i)/frames
                if agent_id:
                    self.move_black_bird(pos, image)
                else:
                    self.move_red_bird(pos, image)
                refresh()
                sleep(abs(self.frame_time) / frames)
        else:
            if agent_id:
                self.move_black_bird(bird, image)
            else:
                self.move_red_bird(bird, image)

        refresh()

    def draw_black_bird(self, pos):
        return [circle(self.to_screen(pos), BLACK_BIRD_SCALE * self.grid_size,
                       fill_color=BLACK_COLOR, outline_color=WHITE_COLOR,
                       endpoints=None, width=0)]

    def move_black_bird(self, position, image):
        screen_position = self.to_screen(position)
        r = BLACK_BIRD_SCALE * self.grid_size
        move_circle(image[0], screen_position, r)
        refresh()

    def finish(self):
        end_graphics()

    def to_screen(self, point):
        (x, y) = point
        #y = self.height - y
        x = (x + 1)*self.grid_size
        y = (self.height - y)*self.grid_size
        return (x, y)

    # Fixes some TK issue with off-center circles
    def to_screen2(self, point):
        (x, y) = point
        #y = self.height - y
        x = (x + 1)*self.grid_size
        y = (self.height - y)*self.grid_size
        return (x, y)

    def draw_walls(self, wall_matrix):
        wall_color = WALL_COLOR
        for x_num, x in enumerate(wall_matrix):

            for y_num, cell in enumerate(x):
                if cell:  # There's a wall here
                    pos = (x_num, y_num)
                    screen = self.to_screen(pos)
                    screen2 = self.to_screen2(pos)

                    # draw each quadrant of the square based on adjacent walls
                    w_is_wall = self.is_wall(x_num-1, y_num, wall_matrix)
                    e_is_wall = self.is_wall(x_num+1, y_num, wall_matrix)
                    n_is_wall = self.is_wall(x_num, y_num+1, wall_matrix)
                    s_is_wall = self.is_wall(x_num, y_num-1, wall_matrix)
                    nw_is_wall = self.is_wall(x_num-1, y_num+1, wall_matrix)
                    sw_is_wall = self.is_wall(x_num-1, y_num-1, wall_matrix)
                    ne_is_wall = self.is_wall(x_num+1, y_num+1, wall_matrix)
                    se_is_wall = self.is_wall(x_num+1, y_num-1, wall_matrix)

                    # NE quadrant
                    if (not n_is_wall) and (not e_is_wall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.grid_size,
                               wall_color, wall_color, (0, 91), 'arc')
                    if (n_is_wall) and (not e_is_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*WALL_RADIUS, 0)),
                             add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(-0.5)-1)), wall_color)
                    if (not n_is_wall) and (e_is_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(-1)*WALL_RADIUS)),
                             add(screen, (self.grid_size*0.5+1, self.grid_size*(-1)*WALL_RADIUS)), wall_color)
                    if (n_is_wall) and (e_is_wall) and (not ne_is_wall):
                        # outer circle
                        circle(add(screen2, (self.grid_size*2*WALL_RADIUS,
                                             self.grid_size*(-2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1,
                               wall_color, wall_color, (180, 271), 'arc')
                        line(add(screen, (self.grid_size*2*WALL_RADIUS-1,
                                          self.grid_size*(-1)*WALL_RADIUS)),
                             add(screen, (self.grid_size*0.5+1, self.grid_size*(-1)*WALL_RADIUS)), wall_color)
                        line(add(screen, (self.grid_size*WALL_RADIUS,
                                          self.grid_size*(-2)*WALL_RADIUS+1)),
                             add(screen, (self.grid_size*WALL_RADIUS, self.grid_size*(-0.5))), wall_color)

                    # NW quadrant
                    if (not n_is_wall) and (not w_is_wall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.grid_size, wall_color,
                               wall_color, (90, 181), 'arc')
                    if (n_is_wall) and (not w_is_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*(-1)*WALL_RADIUS, 0)),
                             add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(-0.5)-1)), wall_color)
                    if (not n_is_wall) and (w_is_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(-1)*WALL_RADIUS)),
                             add(screen, (self.grid_size*(-0.5)-1, self.grid_size*(-1)*WALL_RADIUS)), wall_color)
                    if (n_is_wall) and (w_is_wall) and (not nw_is_wall):
                        # outer circle
                        circle(add(screen2, (self.grid_size*(-2)*WALL_RADIUS,
                                             self.grid_size*(-2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1,
                               wall_color, wall_color, (270, 361), 'arc')
                        line(add(screen, (self.grid_size*(-2)*WALL_RADIUS+1,
                                          self.grid_size*(-1)*WALL_RADIUS)), add(screen,
                                                                                 (self.grid_size*(-0.5), self.grid_size*(-1)*WALL_RADIUS)), wall_color)
                        line(add(screen, (self.grid_size*(-1)*WALL_RADIUS,
                                          self.grid_size*(-2)*WALL_RADIUS+1)),
                             add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(-0.5))), wall_color)

                    # SE quadrant
                    if (not s_is_wall) and (not e_is_wall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.grid_size, wall_color,
                               wall_color, (270, 361), 'arc')
                    if (s_is_wall) and (not e_is_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*WALL_RADIUS, 0)), add(screen,
                                                                               (self.grid_size*WALL_RADIUS, self.grid_size*(0.5)+1)), wall_color)
                    if (not s_is_wall) and (e_is_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(1)*WALL_RADIUS)),
                             add(screen, (self.grid_size*0.5+1, self.grid_size*(1)*WALL_RADIUS)), wall_color)
                    if (s_is_wall) and (e_is_wall) and (not se_is_wall):
                        # outer circle
                        circle(add(screen2, (self.grid_size*2*WALL_RADIUS,
                                             self.grid_size*(2)*WALL_RADIUS)),
                               WALL_RADIUS * self.grid_size-1, wall_color, wall_color, (90, 181), 'arc')
                        line(add(screen, (self.grid_size*2*WALL_RADIUS-1,
                                          self.grid_size*(1)*WALL_RADIUS)), add(screen,
                                                                                (self.grid_size*0.5, self.grid_size*(1)*WALL_RADIUS)), wall_color)
                        line(add(screen, (self.grid_size*WALL_RADIUS,
                                          self.grid_size*(2)*WALL_RADIUS-1)), add(screen,
                                                                                  (self.grid_size*WALL_RADIUS, self.grid_size*(0.5))), wall_color)

                    # SW quadrant
                    if (not s_is_wall) and (not w_is_wall):
                        # inner circle
                        circle(screen2, WALL_RADIUS * self.grid_size, wall_color,
                               wall_color, (180, 271), 'arc')
                    if (s_is_wall) and (not w_is_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*(-1)*WALL_RADIUS, 0)),
                             add(screen, (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(0.5)+1)), wall_color)
                    if (not s_is_wall) and (w_is_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(1)*WALL_RADIUS)),
                             add(screen, (self.grid_size*(-0.5)-1, self.grid_size*(1)*WALL_RADIUS)), wall_color)
                    if (s_is_wall) and (w_is_wall) and (not sw_is_wall):
                        # outer circle
                        circle(add(screen2, (self.grid_size*(-2)*WALL_RADIUS,
                                             self.grid_size*(2)*WALL_RADIUS)), WALL_RADIUS * self.grid_size-1,
                               wall_color, wall_color, (0, 91), 'arc')
                        line(add(screen, (self.grid_size*(-2)*WALL_RADIUS+1,
                                          self.grid_size*(1)*WALL_RADIUS)), add(screen,
                                                                                (self.grid_size*(-0.5), self.grid_size*(1)*WALL_RADIUS)), wall_color)
                        line(add(screen, (self.grid_size*(-1)*WALL_RADIUS,
                                          self.grid_size*(2)*WALL_RADIUS-1)), add(screen,
                                                                                  (self.grid_size*(-1)*WALL_RADIUS, self.grid_size*(0.5))), wall_color)

    def is_wall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= len(walls) or y >= len(walls[0]):
            return False
        return walls[x][y]

    def draw_yellow_bird(self, yellow_birds):
        yellow_bird_images = [[None for y in range(
            self.height)] for x in range(self.width)]
        for pos in yellow_birds:
            yellow_bird_images[pos[0]][pos[1]] = triangle(self.to_screen(pos),
                                                          YELLOWBIRD_SIZE * self.grid_size, YELLOWBIRD_COLOR, BLACK_COLOR)
        return yellow_bird_images

    def remove_yellow_bird(self, cell, yellow_bird_images):
        x, y = cell
        remove_from_screen(yellow_bird_images[x][y])

    def draw_expanded_cells(self, cells):
        """ Draws an overlay of expanded grid positions for search agents """
        n = float(len(cells))
        baseColor = [0.0/255, 105.0/255, 255.0/255]
        self.clear_expanded_cells()
        self.expanded_cells = []
        for k, cell in enumerate(cells):
            screen_pos = self.to_screen(cell)
            cell_color = format_color(
                *[(n-k) * c * .5 / n + .25 for c in baseColor])
            block = square(screen_pos,
                           0.5 * self.grid_size,
                           color=cell_color,
                           filled=1, behind=2)
            self.expanded_cells.append(block)
            if self.frame_time < 0:
                refresh()

    def clear_expanded_cells(self):
        if 'expanded_cells' in dir(self) and len(self.expanded_cells) > 0:
            for cell in self.expanded_cells:
                remove_from_screen(cell)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


# Saving graphical output
# -----------------------
# Note: to make an animated gif from this postscript output, try the command:
# convert -delay 7 -loop 1 -compress lzw -layers optimize frame* out.gif
# convert is part of imagemagick (freeware)

SAVE_POSTSCRIPT = False
POSTSCRIPT_OUTPUT_DIR = 'frames'
FRAME_NUMBER = 0


def save_frame():
    "Saves the current graphical output as a postscript file"
    global SAVE_POSTSCRIPT, FRAME_NUMBER, POSTSCRIPT_OUTPUT_DIR
    if not SAVE_POSTSCRIPT:
        return
    if not os.path.exists(POSTSCRIPT_OUTPUT_DIR):
        os.mkdir(POSTSCRIPT_OUTPUT_DIR)
    name = os.path.join(POSTSCRIPT_OUTPUT_DIR, 'frame_%08d.ps' % FRAME_NUMBER)
    FRAME_NUMBER += 1
    write_postscript(name)  # writes the current canvas
