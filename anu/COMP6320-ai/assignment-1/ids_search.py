"""
    Enter your details below:

    Name: Rui Qiu
    Student ID: u6139152
    Email: u6139152@anu.edu.au
"""

import util
from frontiers import Stack


def solve(problem):
    """
    Return a list of directions. See handout for more details.
    :param problem: the starting set up.
    :return: a list of directions.
    """

    # *** YOUR CODE HERE ***

    # The core of Iterative Deepening Search are iterations of Depth Limited
    # Search with given increasing depth.

    # A recursive version of Depth Limited Search
    def depth_limited_search(problem, limit):
        """
        Return a list of nodes we traversed (or None).
        :param problem: the starting set up.
        :param limit: a given numeric depth limit.
        :return: a list of nodes.
        """

        # in this case, we simply use a list to keep track of nodes we
        # traversed, instead of the data structure, Stack.
        path = list()
        visited = set()  # as before, to prevent duplicated nodes
        root = problem.get_initial_state()

        def rec_dls(state, action, depth):

            visited.add(state)

            # if it is a goal
            if problem.goal_test(state):
                path.append((state, action))
                return path

            # or if it reaches a certain depth, but not a goal
            elif depth == 0:
                visited.remove(state)
                return None

            else:
                path.append([state, action])
                for successor, action, cost in problem.get_successors(state):
                    if successor not in visited:
                        # recursively expands the deepest node
                        res = rec_dls(successor, action, depth-1)
                        if res is not None:
                            return res
                path.pop()
                visited.remove(state)

        # "Stared From the Bottom" (root)
        result = rec_dls(root, 'None', limit)
        # return the path if the we DID have achieved something
        if result is not None:
            return path

    import sys
    for depth in range(sys.maxsize):  # depth from 0 to infinity
        print("Lower-bound of the optimal cost is {}".format(depth))
        res2 = depth_limited_search(problem, depth)
        if res2 is not None:
            action_list = list()
            for move in res2:
                action_list.append(move[1])  # recall index 0 is the parent
            # do not forget a None returned in iteration 0 (with depth 0)
            action_list.remove('None')
            return action_list

# Note:
# For anuSearch, the IDS is pretty inefficient. As the depth increases,
# the runtime of each iteration increases exponentially. (I only ran 24 depths
# for testing.)
