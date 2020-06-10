# agents.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file defines a set of Agents which interact with the system via actions.
    All of the agents defined in the program extend the class Agent.

    The only thing you may need to look at in here is the class GreedyBlackBirdAgent
    at the bottom of the file, in case you want to see exactly how the black bird
    acts in adversarial search.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import random
import sys
import time

import heuristics
import search_problems
import search_strategies
import util
from actions import Actions, Directions
from graphics_utils import keys_pressed, keys_waiting, sleep


class Agent:
    """ An agent must define a get_action method which the system uses to solicit
        an action from the agent. All agents in the game will derive from this class.
    """

    def __init__(self, agent_index=0):
        """ Make a new agent. All agents have an index. Index 0 is the red bird,
            index 1 is the black bird.
            (Agent, int) -> None
        """
        self.agent_index = agent_index

    def get_action(self, state):
        """ The Agent will receive a state and must return an action from
            Directions.{North, South, East, West, Stop}
            (Agent, state) -> Direction
        """
        util.raise_not_defined()


class SearchAgent(object):
    """ This general search agent finds a path using a supplied search algorithm
        for a supplied search problem, then returns actions to follow that path.

        This planning is done when the system calls the register_initial_state
        method. The system then gets actions from this plan with the get_action
        method.

        As a default, this agent runs depth-first search with a blind heuristic
        on a PositionSearchProblem.
    """

    def __init__(self, agent_index, fn='depth_first_search',
                 prob='PositionSearchProblem', heuristic='blind_heuristic'):
        """ Set up the agent, look for the implementations of its search function,
            problem, and heuristic.

            Warning: some advanced Python magic is employed below to find the
            right functions and problems.
            (SearchAgent, str, str, str) -> None
        """
        self.agent_index = agent_index
        # Get the search function from the name and heuristic
        if fn not in dir(search_strategies):
            raise AttributeError(
                fn + ' is not a search function in search_strategies.py.')
        func = getattr(search_strategies, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            sys.stderr.write('[SearchAgent] using function {} \n'.format(fn))
            self.search_function = func
        else:
            if heuristic in dir(heuristics):
                heur = getattr(heuristics, heuristic)
            else:
                raise AttributeError(
                    heuristic + ' is not a function in heuristics.py')
            sys.stderr.write(
                '[SearchAgent] using function %s and heuristic %s\n' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.search_function = lambda x: func(x, heuristic=heur)
        # Get the search problem type from the name
        if prob not in dir(search_problems) or not prob.endswith('Problem'):
            raise AttributeError(
                prob + ' is not a search problem type in agents.py.')
        self.search_type = getattr(search_problems, prob)
        sys.stderr.write('[SearchAgent] using problem type %s \n' % prob)

    def register_initial_state(self, state):
        """ This is the first time that the agent sees the layout of the game board.
            It will run the given search algorithm with the given heuristic to
            make a plan to the goal. All of the work is done in this method!

            (SearchAgent, state) -> None
        """
        if self.search_function is None:
            raise Exception("No search function provided for SearchAgent")
        start_time = time.time()
        problem = self.search_type(state)  # Makes a new search problem
        self.actions = self.search_function(problem)  # Find a path
        end_time = time.time()
        self.result = {}
        self.result['plan'] = self.actions

        total_cost = problem.get_cost_of_actions(self.actions)
        self.result['cost'] = total_cost
        self.result['time'] = end_time - start_time
        sys.stderr.write('Path found with total cost of {0:d} in {1:.1f} seconds\n'.format(
            total_cost, time.time() - start_time))

        if '_expanded' in dir(problem):
            sys.stderr.write('Search nodes expanded: %d\n' % problem._expanded)
            self.result['expanded'] = problem._expanded

    def get_action(self, state):
        """ Returns the next action in the path chosen earlier (in
            register_initial_state). Return Directions.STOP if there is no
            further action to take.

            (SearchAgent, State) -> str
        """
        if 'action_index' not in dir(self):
            self.action_index = 0
        i = self.action_index
        self.action_index += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class SearchAlgorithm:
    def __init__(self, search_func, heuristic_func):
        self.S = search_func
        self.H = heuristic_func

    def __call__(self, x):
        from inspect import signature
        if len(signature(self.S).parameters) == 2:
            return self.S(x, self.H)
        else:
            return self.S(x)


class TestAgent(SearchAgent):
    def __init__(self, agent_index, prob, search_func, heuristic_func):
        """ Set up the agent, look for the implementations of its search function,
            problem, and heuristic.

            Warning: some advanced Python magic is employed below to find the
            right functions and problems.
            (SearchAgent, str, str, str) -> None
        """
        self.agent_index = agent_index
        self.search_function = SearchAlgorithm(search_func, heuristic_func)
        # Get the search problem type from the name
        if prob not in dir(search_problems) or not prob.endswith('Problem'):
            raise AttributeError(
                prob + ' is not a search problem type in agents.py.')
        self.search_type = getattr(search_problems, prob)
        sys.stderr.write('[SearchAgent] using problem type %s \n' % prob)


class KeyboardAgent(Agent):
    """ An agent controlled by the keyboard. """

    # NOTE: Arrow keys also work.
    WEST_KEY, EAST_KEY, NORTH_KEY, SOUTH_KEY = "adws"

    def get_action(self, state):
        """ Wait for the user to enter a valid action on the keyboard.
            Return the first valid action entered since the last check.
            (KeyboardAgent, State) -> str
        """
        legal = state.get_legal_actions(self.agent_index)
        while True:
            keys = keys_waiting() + keys_pressed()
            if (self.WEST_KEY in keys or 'Left' in keys) and Directions.WEST in legal:
                move = Directions.WEST
                break
            if (self.EAST_KEY in keys or 'Right' in keys) and Directions.EAST in legal:
                move = Directions.EAST
                break
            if (self.NORTH_KEY in keys or 'Up' in keys) and Directions.NORTH in legal:
                move = Directions.NORTH
                break
            if (self.SOUTH_KEY in keys or 'Down' in keys) and Directions.SOUTH in legal:
                move = Directions.SOUTH
                break
            sleep(0.05)
        return move


class BlackBirdAgent(Agent):
    """ A BlackBirdAgent represents an adversary that is out to find more yellow
        birds than the red bird. The basic black bird moves randomly and will only
        stop if there are no other legal moves that it can make.
    """

    def get_action(self, state):
        """ Get the action that the BlackBird will perform in the given state.
            (BlackBirdAgent, State) -> str
        """
        legal_actions = [a for a in state.get_legal_actions(self.agent_index)
                         if a != Directions.STOP]
        if not legal_actions:
            return Directions.STOP
        return random.choice(legal_actions)


class GreedyBlackBirdAgent(BlackBirdAgent):
    """ A black bird that will rush blindly to the closest yellow bird, ignoring
        the position of the red bird.
    """

    def get_action(self, state):
        """ Get the action that the black bird will perform in the given state.
            The black bird will move towards the closet current yellow bird.
            It moves along the shortest path as determined by the maze_distance
            supplied with a layout. It will never stay still unless it cannot
            move.

            (GreedyBlackBirdAgent, State) -> str
        """
        # First, find the closest yellow bird
        own_pos = state.black_bird_position
        state.yellow_birds
        min_dist = float("inf")
        min_yb = None
        for yb in state.yellow_birds:
            dist = state.layout.distance[(own_pos, yb)]
            if dist < min_dist:
                min_dist = dist
                min_yb = yb
        if min_yb is None:
            return Directions.STOP
        # Next, find the direction to move to get closer to it
        legal_actions = state.get_legal_actions(self.agent_index)
        min_dist = float("inf")
        min_action = None
        for action in legal_actions:
            if action == Directions.STOP:
                continue
            dist = state.layout.distance[
                (Actions.get_successor(own_pos, action), min_yb)]
            if dist < min_dist:
                min_dist = dist
                min_action = action
        if min_action is None:
            return Directions.STOP
        return min_action
