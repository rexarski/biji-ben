# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This is the file you should look at to understand the data-structures
    required to make your CNF encodings.

    There is a Problem, which has a start state and goal and lists of
    actions and propositions.

    Each Action has a precondition and positive and negative effect.
    These are lists of Propositions.

    Each Propositions has a list of Actions for which it is a precondition,
    a positive and a negative effect.

    self.action_first_step will either be None (in which case you will not have to deal with it)
    otherwise it will be a dictionary {Action : int} mapping each action
    to the first step it could possible be executed (as computed by the plangraph).

    self.fluent_mutex will either be None (in which case you will not have to deal with it)
    otherwise it will be a dictionary {int : [(Proposition, Proposition), ...]} which maps
    each time t step up to some N to a list of pairs of propositions.
    Each pair of Propositions is mutex at the time step t.

    All Propositions which are mutex at step N are also mutex at steps > N.
"""

from utilities import ProblemException


class Proposition:
    """ A state proposition. """

    def __init__(self, name, variables):
        """ Make a new Proposition

            (Proposition, str, [str]) -> None
        """
        self.name = name
        self.variables = variables

        self.preconditions = []
        self.pos_effects = []
        self.neg_effects = []

    def __str__(self):
        """ Return a short string representation of the Proposition.
            (Predicate) -> str
        """
        return " ".join([self.name] + self.variables)

    def __repr__(self):
        return self.__str__()


class Action:
    """ A grounded planning action """

    def __init__(self, name, parameters):
        """ Make a new a action.

            (Action, str, [str]) -> None
        """
        self.name = name
        self.parameters = parameters
        self.preconditions = []
        self.pos_effects = []
        self.neg_effects = []

    def __dump__(self):
        """ Write a string representation of the action.
            (Action, file) -> None
        """
        out_str = "Action: " + str(self) + "\n"
        out_str += "Pre:     " + \
            " ".join(["("+str(f)+")" for f in self.preconditions]) + "\n"
        out_str += "Pos Eff: " + \
            " ".join(["("+str(f)+")" for f in self.pos_effects]) + "\n"
        out_str += "Neg Eff: " + \
            " ".join(["("+str(f)+")" for f in self.neg_effects]) + "\n"
        return out_str

    def __str__(self):
        """ Return a short string representation of the action.
            (Action) -> str
        """
        return " ".join([self.name] + self.parameters)

    def __repr__(self):
        return self.__str__()


class Problem:
    """ An instance of a STRIPS planning problem. After parsing this class also
        represents a PDDL planning problem. Note that these problems may have
        negative preconditions.
    """

    def __init__(self):
        """ Make a new problem instance with the given name.
            (Problem, str) -> None
        """
        self.propositions = []
        self.actions = []
        self.pos_initial_state = []
        self.neg_initial_state = []
        self.goal = []

        self.action_first_step = None
        self.fluent_mutex = None

    def __str__(self):
        """ Return a short string representation of the problem
            (Problem) -> str
        """
        return self.name

    def __repr__(self):
        return self.__str__()
