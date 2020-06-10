"""
    Enter your details below:

    Name: Rui Qiu
    Student ID: u6139162
    Email: u6139152@anu.edu.au
"""

import util
import heuristics


def solve(problem, heuristic):
    """
    Return a list of directions. See handout for more details.
    :param problem: the starting set up.
    :param heuristic: a heuristic function.
    :return: a list of directions.
    """

    # *** YOUR CODE HERE ***

    # SET UP
    from frontiers import PriorityQueue
    # this time, we use a predefined PriorityQueue as frontier since A* expands
    # the nodes on the frontier with minimum f-value.
    frontier = PriorityQueue()
    visited = set()
    action_list = list()
    g = dict()  # cost from s0 to current
    f = dict()  # g + heuristic to goal
    previous_action = dict()

    # INITIALIZE
    root = problem.get_initial_state()
    # g-value from root to root is 0.
    g[root] = 0
    # f-value is the expected cost from root to the goal
    fv = g[root] + heuristic(root, problem)
    f[root] = fv
    frontier.push(root, fv)
    back_start = None  # this variable is used for back tracking from the goal
    # to the root. It will be defined as the goal once we hit the goal.

    # ITERATIONS
    while not frontier.is_empty():
        current = frontier.peek()

        # if it is a goal
        if problem.goal_test(current):
            back_start = current
            break

        current = frontier.pop()
        visited.add(current)

        # expands the one with minimum f-value
        for successor, action, cost in problem.get_successors(current):
            if successor not in visited:
                g[successor] = g[current] + cost
                fv = g[successor] + heuristic(successor, problem)

                # if the child node is not yet 'to be expanded', we add it to
                # the waiting list. Note that here we don't use visited() to
                # check, simply because we need to re-expand some nodes in
                # order to achieve optimality.
                if successor not in f.keys():
                    previous_action[successor] = (current, action)
                    frontier.push(successor, fv)
                    f[successor] = fv

                # if the current child has a smaller f-value smaller than the
                # one we previously stored in the dictionary, we need to update
                # it.
                elif f[successor] > fv:
                    frontier.change_priority(successor, fv)
                    f[successor] = fv
                    previous_action[successor] = (current, action)

    # When we hit the goal, we will trace back to our root.
    while back_start is not root:
        action_list.append(previous_action[back_start][1])  # action
        back_start = previous_action[back_start][0]  # parent
    return list(reversed(action_list))  # don't forget the reverse the list
