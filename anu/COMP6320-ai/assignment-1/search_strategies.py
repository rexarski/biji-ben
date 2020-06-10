# search_strategies.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course


import time

import frontiers
import heuristics
import util


class SearchNode:
    """ The data structure representing a search node. It has
        state:      A state as defined by the appropriate SearchProblem
        action:     The action that led to this state from its parent
        path_cost:  The cost to get to this state from the start state
        parent:     The parent SearchNode

        This is created for you to use when implementing the search problems
        later in this file. You do not need to modify this.
    """

    def __init__(self, state, action=None, path_cost=0, parent=None, depth=0):
        """ Make a new search node with the given parameters.
            (SearchNode, state, str, int, SearchNode) -> None
        """
        self.state = state
        self.action = action
        self.path_cost = path_cost
        self.parent = parent
        self.depth = depth

    def __str__(self):
        """ Return a string representation of the SearchNode
            (SearchNode) -> str
        """
        return "SearchNode({}, {}, {}, {}, {})".format(
            self.state, self.action, self.path_cost, self.parent, self.depth
        )


def breadth_first_search(problem):
    from brfs_search import solve
    start = time.clock()
    rv = solve(problem)
    end = time.clock()
    print("Search time", end - start, "seconds")
    return rv


def ids_search(problem):
    from ids_search import solve
    start = time.clock()
    rv = solve(problem)
    end = time.clock()
    print("Search time", end - start, "seconds")
    return rv


def a_star_search(problem, heuristic=heuristics.null_heuristic):
    from a_star_search import solve
    start = time.clock()
    rv = solve(problem, heuristic)
    end = time.clock()
    print("Search time", end - start, "seconds")
    return rv



# Abbreviations to be used elsewhere in the program
bfs = breadth_first_search
ids = ids_search
astar = a_star_search
