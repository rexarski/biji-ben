# state.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This file defines the State class which is used by the underlying system
    to represent the state of the game. You will not need to look at this as
    you will be working with SearchProblems which abstract away the details of
    this class.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""


class State:
    """ A State specifies the full game state, including the yellow birds,
        agent position and score changes.
    """

    def __init__(self, layout=None):
        """ Generates the initial state from the given layout.
            (State, State) -> None
        """
        from game_rules import YELLOW_BIRD_SCORE
        if layout is not None:
            self.yellow_birds = layout.yellow_birds
            self.red_bird_position = layout.red_bird_position
            self.black_bird_position = layout.black_bird_position
            self.score = 0
            self.terminal = False
            self.score_change = 0
            self.layout = layout
            self._agent_moved = None
            self._yellow_bird_eaten = None
            self.red_bird_dead = False
            self.black_bird_dead = False
            self.current_yellow_bird_score = YELLOW_BIRD_SCORE

    def deepcopy(self):
        """ Generates a new state by copying information from this state.
            (State, State) -> None
        """
        state = State()
        state.yellow_birds = self.yellow_birds
        state.red_bird_position = self.red_bird_position
        state.black_bird_position = self.black_bird_position
        state.score = self.score
        state.terminal = self.terminal
        state.score_change = self.score_change
        state.layout = self.layout

        state._agent_moved = None
        state._yellow_bird_eaten = None
        state.current_yellow_bird_score = self.current_yellow_bird_score
        state.red_bird_dead = self.red_bird_dead
        state.black_bird_dead = self.black_bird_dead
        return state

    def get_legal_actions(self, agent_index=0):
        """ Returns the legal actions for the agent specified (0 is red_bird)
            (State, int) -> [Action]
        """
        if self.terminal:
            return []
        if agent_index == 0:
            from game_rules import RedBirdRules
            return RedBirdRules.get_legal_actions(self)
        else:
            from game_rules import BlackBirdRules
            return BlackBirdRules.get_legal_actions(self)

    def successor(self, agent_index, action):
        """ Returns the the state that results when the given action is applied.
            (State, int, str) -> State
        """
        # Check that successors exist
        if self.terminal:
            raise Exception('Can\'t generate a successor of a terminal state.')
        # Copy current state
        state = self.deepcopy()
        # Let agent's logic deal with its action's effects on the board
        if agent_index == 0:
            from game_rules import RedBirdRules
            RedBirdRules.apply_action(state, action)
        else:
            from game_rules import BlackBirdRules
            BlackBirdRules.apply_action(state, action)

        # Book keeping
        state._agent_moved = agent_index
        state.score += state.score_change
        return state

    def get_red_bird_position(self):
        """ Return the position of the red bird.
            (State) -> (int, int)
        """
        return self.red_bird_position

    def get_black_bird_position(self):
        """ Return the position of the black bird. Returns None if there is no
            black bird.
            (State) -> (int, int)
        """
        return self.black_bird_position

    def get_yellow_birds(self):
        """ Return the set of yellow bird positions.
            (State) -> set([(int, int)])
        """
        return self.yellow_birds

    def get_num_yellow_birds(self):
        """ Return the number of yellow birds.
            (State) -> int
        """
        return len(self.yellow_birds)

    def has_yellow_bird(self, pos):
        """ Return iff the given position has a yellow bird.
            (State, (int, int)) -> bool
        """
        return pos in self.yellow_birds

    def get_score(self):
        """ Return the score as a float.
            (State) -> float
        """
        return float(self.score)

    def get_yellow_bird_score(self):
        """ Return the score as a float.
            (State) -> float
        """
        return self.current_yellow_bird_score

    def maze_distance(self, pos1, pos2):
        """ Return the shortest distance between pos1 and pos2, ignoring that a
            path may be blocked by an agent.
            (State, (int, int), (int, int)) -> int
        """
        return self.layout.get_maze_distances()[(pos1, pos2)]

    def is_terminal(self):
        """ Return iff the state is terminal.
            (State) -> bool
        """
#        print( "Red Dead?", self.red_bird_dead, "Black Dead?", self.black_bird_dead, "Yellow Birds Left", len(self.yellow_birds))
        return (len(self.yellow_birds) == 0) or self.red_bird_dead or self.black_bird_dead or (self.current_yellow_bird_score < 0.5)

    def __eq__(self, other):
        """ Allows two states to be compared.
            (State, State) -> bool
        """
        return isinstance(other, State) and\
            self.yellow_birds == other.yellow_birds and\
            self.red_bird_position == other.red_bird_position and\
            self.black_bird_position == other.black_bird_position and\
            self.current_yellow_bird_score == other.current_yellow_bird_score and\
            self.score == other.score

    def __hash__(self):
        """ Allows states to be keys of dictionaries and in sets.
            (State) -> int
        """
        return int((hash((self.red_bird_position, self.black_bird_position)) +
                    13*hash(self.yellow_birds) + 113*hash(self.current_yellow_bird_score) +
                    7*hash(self.score)) % 1048575)

    def __str__(self):
        """ Return a string representation of the state.
            (State) -> str
        """
        width, height = self.layout.width, self.layout.height
        out_str = ""
        for y in range(height-1, -1, -1):
            for x in range(width):
                pos = (x, y)
                if pos in self.yellow_birds:
                    out_str += "."
                elif self.layout.walls[x][y]:
                    out_str += "%"
                elif pos == self.red_bird_position:
                    out_str += "R"
                elif pos == self.black_bird_position:
                    out_str += "B"
                else:
                    out_str += " "
            out_str += "\n"
        return out_str + "\nScore: " + str(self.score) + "\n"
