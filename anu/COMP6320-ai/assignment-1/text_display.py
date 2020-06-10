# text_display.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file defines a text alternative to the graphical display that the
    system usually runs with. If you want to use it run
        python red_bird.py --help
    to see how.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import time
import red_bird

DRAW_EVERY = 1
SLEEP_TIME = 0 # This can be overwritten by __init__
DISPLAY_MOVES = False
QUIET = False # Supresses output

class NullGraphics:

    def initialise(self, state):
        pass

    def update(self, state, agent_index):
        pass

    def check_null_display(self):
        return True

    def pause(self):
        time.sleep(SLEEP_TIME)

    def draw(self, state):
        print(state)

    def finish(self):
        pass

class RedBirdGraphics:
    def __init__(self, speed=None):
        if speed != None:
            global SLEEP_TIME
            SLEEP_TIME = speed

    def initialise(self, state):
        self.draw(state)
        self.pause()
        self.turn = 0
        self.agent_counter = 0

    def update(self, state, agent_index):
        self.turn += 1
        if DISPLAY_MOVES:
            print("Turn:", self.turn)
            if agent_index == 0:
                print("Red bird moved to:", state.get_red_bird_position())
            else:
                 print("Black bird moved to:", state.get_black_bird_position())
            print("Score:", state.get_score())
        if self.turn % DRAW_EVERY == 0:
            self.draw(state)
            self.pause()
        if state.terminal:
            self.draw(state)

    def pause(self):
        time.sleep(SLEEP_TIME)

    def draw(self, state):
        print(state)

    def finish(self):
        pass
