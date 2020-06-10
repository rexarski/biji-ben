# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the
# course
"""
    Enter your details below:

    Name: Rui Qiu
    Student ID: u6139162
    Email: u6139152@anu.edu.au

    This class contains heuristics which are used for the search procedures
    that you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the
    algorithms that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

# ----------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem
# You do not need to modify any of these.
# ----------------------------------------------------------------------------


def null_heuristic(pos, problem):
    """ The null heuristic. It is fast but uninformative. It always returns 0.
        (State, SearchProblem) -> int
    """
    return 0


def manhattan_heuristic(pos, problem):
    """ The Manhattan distance heuristic for a PositionSearchProblem.
      ((int, int), PositionSearchProblem) -> int
    """
    return abs(pos[0]-problem.goal_pos[0]) + abs(pos[1]-problem.goal_pos[1])


def euclidean_heuristic(pos, problem):
    """ The Euclidean distance heuristic for a PositionSearchProblem
        ((int, int), PositionSearchProblem) -> float
    """
    return ((pos[0] - problem.goal_pos[0]) ** 2 + (
            pos[1] - problem.goal_pos[1]) ** 2) ** 0.5


# Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic

# ----------------------------------------------------------------------------
# You have to implement the following heuristics for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
# ----------------------------------------------------------------------------

# You can make helper functions here, if you need them


def bird_counting_heuristic(state, problem):
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """
    heuristic_value = len(yellow_birds)  # simply COUNT the number of birds

    return heuristic_value


bch = bird_counting_heuristic


def every_bird_heuristic(state, problem):
    """
        (((int, int), ((int, int))), MultiplePositionSearchProblem) -> number
    """
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """

    yellow_birds = list(yellow_birds)
    current_bird = position
    distance = problem.distance

    # Tie-breaking scaling heuristics
    # Reference link:
    # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    #
    # This is introduced because there might be multiple paths with the same
    # f-value. So the hack is to differ those f-values by scaling them
    # slightly. Say we scale them down by 1%.

    # Why do we choose to scale down? Because we want to prevent
    # overestimation, so that the heuristics is admissible.

    # Every time, we find the closed the yellow bird, assume it is the next
    # position
    while len(yellow_birds) > 0:
        # distance dict is updated every time a yb got eaten
        distance_dict = dict()
        target = None
        for a_bird in yellow_birds:
            distance_dict[a_bird] = distance[current_bird, a_bird]
        for item in distance_dict:
            if distance_dict[item] == min(distance_dict.values()):
                target = item
        heuristic_value += min(distance_dict.values()) * 0.99  # scaling down
        current_bird = target
        yellow_birds.remove(current_bird)
    return heuristic_value


every_bird = every_bird_heuristic
