"""
    Enter your details below:

    Name: Rui Qiu
    Student ID: u6139152
    Email: u6139152@anu.edu.au
"""


def solve(problem):
    """
    Return a list of directions. See handout for more details.
    :param problem: the starting set up.
    :return: a list of directions.
    """

    # *** YOUR CODE HERE ***
    from frontiers import Queue
    frontier = Queue()  # a FIFO container to store frontier nodes
    visited = set()  # a set keep track of visited nodes, prevent duplicated
    meta = dict()  # key -> (parent_state, action_to_child)

    root = problem.get_initial_state()
    meta[root] = (None, None)  # root has no parent and no action leading to it
    frontier.push(root)
    action_list = []

    while not frontier.is_empty():

        subtree_root = frontier.pop()  # expands the shallowest nodes

        # if it is the goal, end
        if problem.goal_test(subtree_root):

            # backtrack the actions
            while True:
                path = meta[subtree_root]
                if None not in path:
                    subtree_root = path[0]
                    action = path[1]
                    action_list.append(action)
                else:
                    break
            return list(reversed(action_list))

        # if not the goal, expands all its children
        for successor, action, cost in problem.get_successors(subtree_root):
            if successor in visited:
                continue
            if successor not in frontier.contents:
                meta[successor] = (subtree_root, action)
                frontier.push(successor)

        visited.add(subtree_root)
