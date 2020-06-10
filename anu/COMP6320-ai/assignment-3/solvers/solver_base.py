# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" All solvers in the system extend Solver, which is defined here.
"""

import abc
import os
from importlib import import_module

from utilities import CodeException

solver_path = os.path.dirname(__file__)
solver_list_file_name = os.path.join(solver_path, "solver_list")

solver_sat_code = 0
solver_unsat_code = 1
solver_time_out_code = 2
solver_error_code = 3


class SolvingException(CodeException):
    """ An exception to be raised in the even that something goes wrong with
        the solving process. """


class Solver(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        """Set runstr"""

    @abc.abstractmethod
    def solve(self, wcnf_file_name, sln_file_name, time_limit):
        """solve wcnf_file and return (time, true_vars),
            or raise a SolvingException with the appropriate code from above"""


class SolverWrapper:

    def __init__(self):
        self.valid_solvers = {}
        self.default_solver = ''

    def read_solver_list(self):
        try:
            with open(solver_list_file_name, 'r') as solver_list_file:
                solver_lines = solver_list_file.readlines()
                if len(solver_lines) < 2:
                    raise SolvingException("Error: solver list does not have enough lines.",
                                           solver_error_code)
                self.default_solver = solver_lines[0].rstrip()
                for line in solver_lines[1:]:
                    try:
                        line_tokens = line.rstrip().split(' ')
                        self.valid_solvers[line_tokens[0]] = line_tokens[1]
                    except IndexError:
                        raise SolvingException("Error: badly formed line in solver list: {}".
                                               format(line.rstrip()), solver_error_code)
        except IOError:
            raise SolvingException("Error: failed to load solver list {}.".
                                   format(solver_list_file_name), solver_error_code)

    def instantiate_solver(self, solver_name, cnf_file_name, tmp_path, exp_name, time_out):
        if solver_name not in self.valid_solvers:
            raise SolvingException("Error: invalid solver: {}".format(solver_name),
                                   solver_error_code)
        solver_module = import_module(os.path.dirname(__file__).split("/")[-1] +
                                      '.' + self.valid_solvers[solver_name])
        self.solver = getattr(solver_module, solver_module.solver_class)(
            cnf_file_name, tmp_path, exp_name, time_out)
