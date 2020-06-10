# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the
# course

"""
    Enter your details below:

    Name: Rui Qiu
    Student ID: u6139152
    Email: u6139152@anu.edu.au
"""

import util
from actions import Directions
from agents import Agent
from search_problems import AdversarialSearchProblem


class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
            (MinimaxAgent, str) -> None
        """
        self.max_player = max_player
        self.depth = int(depth)

    def evaluation(self, problem, state):
        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """

        player, red_pos, black_pos, yellow_birds, score, yb_score = state

        # *** YOUR CODE GOES HERE ***

        # https://en.wikipedia.org/wiki/Evaluation_function

        # In my definition of evaluation function, it consists of 4 main
        # parts:

        # 1. The original score.

        # 2. The score of eating yellow birds. We encourage our agent to chase
        # after yellow birds. But this is not a greedy strategy, it will only
        # wisely choose targets. Consider the fact that our component is
        # greedy all the time, then we only consider yellow birds that are
        # closer to us than to our component. Additionally, the closer it is,
        # the higher its value is. Thus, we encourage our agent to deal with
        # close targets first, but selectively ignore some targets beyond our
        # capability.

        # 3. The number of remaining yellow birds. The more yellow birds left,
        # the more penalty our agent receives. So, please don't stop eating
        # birds!

        # 4. Bonus for some bold moves. We want our agent to stick with the
        # component so that some risky but high-return moves are possible.

        gain = 0
        for yb in yellow_birds:
            if problem.distance[yb, red_pos] <= \
                    problem.distance[yb, black_pos]:
                gain += yb_score * 1/(problem.distance[yb, red_pos]+0.001)

        remaining_num = len(yellow_birds)
        bold_move_bonus = 1 / (problem.distance[red_pos, black_pos]+0.001)
        return 3.5 * score + 2 * gain - 10 * remaining_num + bold_move_bonus

    def maximize(self, problem, state, current_depth, alpha=float('-inf'),
                 beta=float('inf')):
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.

             (MinimaxAgent, AdversarialSearchProblem,
                 (int, (int, int), (int, int), ((int, int)), number, number)
                     -> (number, str)
        """

        # *** YOUR CODE GOES HERE ***

        # Two stopping conditions:
        # either reaches the goal or reaches the depth limit

        if current_depth == self.depth:
            return self.evaluation(problem, state), Directions.STOP
        if problem.terminal_test(state):
            return problem.utility(state), Directions.STOP

        v = float('-inf')
        action_list = dict()
        for next_state, action, _ in problem.get_successors(state):
            v = max(v, self.minimize(problem, next_state, current_depth + 1))
            action_list[action] = v
            if v >= beta:
                return v, action
            alpha = max(alpha, v)

        maximizer = max(action_list, key=action_list.get)
        return action_list[maximizer], maximizer

    def minimize(self, problem, state, current_depth, alpha=float('-inf'),
                 beta=float('inf')):
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.

            (MinimaxAgent, AdversarialSearchProblem,
                 (int, (int, int), (int, int), ((int, int)), number, number)
                     -> number
        """

        # *** YOUR CODE GOES HERE ***

        # The implementation of minimize() function is pretty similar to that
        # of maximize() function.

        if current_depth == self.depth:
            return self.evaluation(problem, state)
        if problem.terminal_test(state):
            return problem.utility(state)

        v = float('inf')
        for next_state, action, _ in problem.get_successors(state):
            v = min(v, self.maximize(problem, next_state,
                                     current_depth + 1)[0])
            # this is because maximize also has an "action"
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:", max_action,
              "Expanded:", problem._expanded)
        return max_action
