# search_problems.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file contains a number of different search problems which you will
    be working with throughout the assignment.

    You are not required to look at this file unless you really want to.
    The comments in the code for the various exercises explain methods that
    you will require from these classes.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import sys

import util
from actions import Actions, Directions
from game_rules import TIME_PENALTY, YELLOW_BIRD_SCORE


class SearchProblem(object):
    """ Abstract class outlining structure of a search problem. All of the
        search problems defined in this file will derive from this class and
        inherit or overwrite its methods.

        The one exception to this is AdversarialSearchProblem which uses
        the method terminal_test(state) in place of goal_test(state).
    """

    def __init__(self, state):
        """ Make a new SearchProblem - this will be called by all subclasses.
            This saves the static info from the problem layout. This can be
            accessed via accessor methods.
            (SearchProblem, State) -> None
        """
        self.width = state.layout.get_width()
        self.height = state.layout.get_height()
        self.walls = state.layout.get_walls()

        # A dictionary for heuristics to store information
        self.heuristic_info = {}

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def get_initial_state(self):
        """ Return the initial state (position)
            (PositionSearchProblem) -> (int, int)
        """
        return self.initial_state

    def goal_test(self, state):
        """ Returns True iff the given state is a goal state.
            This will be overridden by all subclasses except AdversarialSearchProblem
            which uses a method called 'terminal' instead.
            (SearchProblem, state) -> bool
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """ Returns a list of triples (next_state, action, cost), where
            - next_state is an expanded successor to the given state
            - action is the action required to get to 'next_state'
            - cost is the cost of getting to 'next_state'
            (SearchProblem, state) -> [(state, str, int)]
        """
        util.raise_not_defined()

    def get_width(self):
        """ Return the width of the maze.
            (SearchProblem) -> int
        """
        return self.width

    def get_height(self):
        """ Return the height of the maze.
            (SearchProblem) -> int
        """
        return self.height

    def get_walls(self):
        """ Return the matrix representing the walls.
            (SearchProblem) -> [[bool]]
        """
        return self.walls

    def maze_distance(self, pos1, pos2):
        """ Return the distance of the shortest path between two locations in
            the maze. This has been precomputed and stored with the layouts.

            This information can be used for the last three questions (on
            heuristics, minimax, and evaluation function), but it CANNOT be
            used for the first three questions (on BrFS, IDS, and A*) as it
            would defeat the purpose of these exercises.

            This method will return None if either of the given positions is a
            wall.

            (SearchProblem, (int, int), (int, int)) -> int
        """
        try:
            return self.distance[(pos1, pos2)]
        except:
            return None

    def get_cost_of_actions(self, actions):
        """ Returns the cost of a particular sequence of actions.
            If those actions include an illegal move, return 999999
            (SearchProblem, [str]) -> int
        """
        util.raise_not_defined()

    # For display purposes only. You can ignore this stuff
    #-----------------------------------------------------------------------
    def expanded(self, pos):
        """ The state has been expanded. Notify the search for display reasons.
            (SearchProblem, (int, int)) -> None
        """
        self._expanded += 1
        if pos not in self._visited:
            self._visited[pos] = True
            self._visitedlist.append(pos)

    def visited_goal(self, pos):
        """ The state has been visited, if it is a goal we should display
            the info we have collected.
            (SearchProblem, (int, int)) -> None
        """
        self._visitedlist.append(pos)
        import __main__
        if '_display' in dir(__main__):
            if 'draw_expanded_cells' in dir(__main__._display):
                __main__._display.draw_expanded_cells(self._visitedlist)
   #-----------------------------------------------------------------------


#-------------------------------------------------------------------------------
# You might want to look at this class for Q1-3
#-------------------------------------------------------------------------------

class PositionSearchProblem(SearchProblem):
    """ A search problem where the red bird is trying to visit a single location.

        A search problem defines the state space, initial_state state, goal test,
        and successor function. This search problem can be used to find paths to
        a particular point on the game board.

        The state space consists of (x,y) positions in a red_bird game.
    """

    def __init__(self, state):
        """ Sets the initial state of the problem to the position of the red bird.
            If there are yellow birds, the first is chosen to be the goal, otherwise
            the goal defaults to (1, 1).
            (PositionSearchProblem, State) -> None
        """
        super(PositionSearchProblem, self).__init__(state)
        if state.get_num_yellow_birds() != 1:
            print("Warning: this does not look like a regular search maze",
                  file=sys.stderr)
        self.initial_state = state.get_red_bird_position()
        if not state.yellow_birds:
            self.goal_pos = (1, 1)
        else:
            self.goal_pos = state.yellow_birds[0]

    def goal_test(self, state):
        """ Check if the given state (position) is the goal position.
             (PositionSearchProblem, (int, int)) -> bool
        """
        is_goal = state == self.goal_pos
        if is_goal:
            self.visited_goal(state)  # For display purposes only
        return is_goal

    def get_successors(self, state):
        """ Returns successor states, the actions they require, and a cost of 1.
            For a given state, this should return a list of triples,
            (successor, action, action_cost), where
                - successor is a successor to the current state,
                - action is the action required to get there, and
                - action_cost' cost of the action
            (PositionSearchProblem, (int, int)) -> [((int, int), str, int)]
        """
        self.expanded(state)  # Bookkeeping for display purposes
        succ = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directions[action]
            next_x, next_y = x + dx, y + dy
            if not self.walls[next_x][next_y]:
                next_state = (next_x, next_y)
                cost = 1
                succ.append((next_state, action, cost))
        return succ

    def get_cost_of_actions(self, actions):
        """ Returns the cost of a particular sequence of actions.
            If those actions include an illegal move, return 999999
            (PositionSearchProblem, [str]) -> int
        """
        if actions == None:
            return 999999
        x, y = self.get_initial_state()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directions[action]
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1

        return cost


#-------------------------------------------------------------------------------
# You might want to look at this class for Q4
#-------------------------------------------------------------------------------

class MultiplePositionSearchProblem(SearchProblem):
    """ A search problem where the goal is to visit a set of positions.

        A search state in this problem is a tuple (pos, yellow_birds):
            - pos: a tuple (x,y) of integers specifying the red bird's position
            - yellow_birds: a tuple of tuples specifying the positions of the remaining
                      yellow birds.
    """

    def __init__(self, state):
        """ Set up the search problem. Make the similified version of the inititial
            state and store the required info from the given State object.
            (MultiplePositionSearchProblem, State) -> None.
        """
        super(MultiplePositionSearchProblem, self).__init__(state)
        self.initial_state = (state.get_red_bird_position(),
                              state.get_yellow_birds())
        self.distance = state.layout.get_maze_distances()

    def goal_test(self, state):
        """ Return iff the given state is a goal.
            (MultiplePositionSearchProblem, ((int, int), ((int, int)))) -> bool
        """
        return not state[1]

    def get_successors(self, state):
        """ Returns successor states, the actions they require, and a cost of 1.
            (MultiplePositionSearchProblem, ((int, int), ((int, int)))) ->
                [((int, int), ((int, int)), str, int)]
        """
        succ = []
        self._expanded += 1
        x, y = state[0]
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directions[direction]
            next_x, next_y = x + dx, y + dy
            if next_x >= 0 and next_x < self.width and next_y >= 0 and next_y < self.height and\
                    not self.walls[next_x][next_y]:
                next_pos = (next_x, next_y)
                if next_pos in state[1]:
                    next_yellow_bird = tuple(
                        [yb for yb in state[1] if yb != next_pos])
                else:
                    next_yellow_bird = state[1]
                succ.append(((next_pos, next_yellow_bird), direction, 1))

        return succ

    def get_cost_of_actions(self, actions):
        """ Returns the cost of a particular sequence of actions.
            If those actions include an illegal move, return 999999
            (PositionSearchProblem, [str]) -> int
        """
        if actions == None:
            return 999999
        x, y = self.get_initial_state()[0]
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directions[action]
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1

        return cost


#-------------------------------------------------------------------------------
# You might want to look at this class for Q5
#-------------------------------------------------------------------------------

class AdversarialSearchProblem(SearchProblem):
    """ A search problem associated with making a single move in an adversarial
        problem. It will be used by MinimaxAgent to make decisions.

        A search state in this problem is a tuple (player, red_pos, black_pos, yellow_birds, score)
            - player is an int indicating the id of the current player (0 for red, 1 for black)
            - red_pos is a tuple (x,y) of integers specifying the red bird's position
            - black_pos is a tuple (x,y) of integers specifying the black bird's position
            - yellow_birds: a tuple of tuples specifying the positions of the remaining
                            yellow birds.
            - score: the score of the state
            - yb_value: the current value of a yellow bird
    """

    def __init__(self, state, max_player):
        """ Set up the search problem. Make the simpilified version of the inititial
            state and store the required info from the given State object and
            the agent_index which indicates which agent is the maximizing player.
            (MultiplePositionSearchProblem, State, int) -> None.
        """
        super(AdversarialSearchProblem, self).__init__(state)
        self.distance = state.layout.get_maze_distances()
        self.max_player = max_player
        self.initial_state = (max_player, state.get_red_bird_position(),
                              state.get_black_bird_position(), state.get_yellow_birds(), state.get_score(),
                              state.get_yellow_bird_score())

    def get_maximizing_player(self):
        """ Return the maximizing player.
            (AdversarialSearchProblem) -> int
        """
        return self.max_player

    def opponent(self, state):
        """ Return the id of the opponent of the player in the indicated state.
            (AdversarialSearchProblem, (int, (int, int), (int, int), ((int, int)), number, number)
                -> int
        """
        return 1 - state[0]

    def utility(self, state):
        """ The utility method just returns the score of the state as this
            reflects how many more yellow birds found by the given player bird
            than by the other player.
            (AdversarialSearchAgent, (int, (int, int), (int, int), ((int, int)), number, number))
                -> int
        """
        return state[4]

    def terminal_test(self, state):
        """ The terminal test returns iff the state is terminal.
            (AdversarialSearchAgent, (int, (int, int), (int, int), ((int, int)), number, number))
                -> bool
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state
        return (not yellow_birds) or (black_pos == red_pos) or (yb_score < 0.5)

    def get_successors(self, state):
        """ Returns successor states, the actions they require, and a cost of 1.
            Agents can only stay still if they have no other option.
            (AdversarialSearchProblem, (int, (int, int), (int, int), ((int, int)), number, number)
                -> [((int, (int, int), (int, int), ((int, int)), number, number), str, int)]
        """
        self._expanded += 1
        player, red_pos, black_pos, yellow_birds, score, yb_score = state
        succ = []
        if player == 0:
            pos = red_pos
            other_pos = black_pos
            player_yb_score = yb_score
        else:
            pos = black_pos
            other_pos = red_pos
            player_yb_score = -yb_score
        x, y = pos
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directions[action]
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if next_x >= 0 and next_x < self.width and next_y >= 0 and next_y < self.height and not self.walls[next_x][next_y]:
                next_score = score
                next_yellow_birds = yellow_birds
                if next_pos in yellow_birds:
                    next_yellow_birds = tuple(
                        [yb for yb in yellow_birds if yb != next_pos])
                    next_score += player_yb_score
                if next_pos == other_pos:  # CHOMP!
                    if player == 0:
                        next_score += 250
                    else:
                        next_score -= 250
                if player == 0:
                    succ.append(
                        ((1, next_pos, black_pos, next_yellow_birds, next_score, yb_score*0.99), action, 1))
                else:
                    succ.append(
                        ((0, red_pos, next_pos, next_yellow_birds, next_score, yb_score*0.99), action, 1))
        if not succ:
            succ.append(((1-player, red_pos, black_pos, yellow_birds,
                          score, yb_score*0.99), Directions.STOP, 1))
        return succ
