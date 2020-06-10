# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This file defines the class Encoding, which all encodings in the system
    will extend. This contains methods for adding clauses and variables
    to the encoding, generating CNF files from encodings, etc.

    You may want to look at this file. The comments should direct you to the
    relevant parts.
"""

import abc
import itertools
import os
from importlib import import_module

from problem import Predicate, PredicateCondition
from utilities import CodeException

encoding_error_code = -4

encoding_list_file_name = os.path.join(
    os.path.dirname(__file__), "encoding_list")


class EncodingException(CodeException):
    """ An exception to be raised in the event that something goes wrong with
        the encoding process. """


class Encoding(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self, horizon):
        """ Make the variables and clauses which will be written out when required.

           (Encoding, int) -> None
        """

    @abc.abstractmethod
    def build_plan(self, horizon):
        """Build a plan from the true variables in self.true_variables.
           Save the plan in the list self.plan

            (Encoding, int) -> None
        """

################################################################################
#   You will need to call the following methods when making your encodings.    #
################################################################################

    def new_cnf_code(self, step, name, obj):
        """ Return a new CNF variable which has the given step, name, and object
            which the variable represents (such as an Action of Fluent, for example).

            (Encoding, int, str, object) -> int
        """
        self.cnf_code += 1
        self.cnf_code_steps[self.cnf_code] = step
        self.cnf_code_names[self.cnf_code] = name
        self.cnf_code_objects[self.cnf_code] = obj
        return self.cnf_code

    def num_cnf_codes(self):
        """ Return the number of CNF variable codes which have been issued.
            (Encoding) -> int
        """
        return self.cnf_code

    def add_clause(self, clause, clause_type):
        """ Add a clause to the problem with the given type string.
            The type string should be a short string describing the type of
            clause -- i.e. pre, post, mutex, start, etc.

            (Encoding, [int], str) -> None
        """
        self.clauses.append(clause)
        self.clause_types.append(clause_type)


################################################################################
#      You will not need to deal with the rest of this file directly.          #
################################################################################

    def __init__(self, problem):
        """ Set encoding parameters.

            (Encoding, Problem) -> None
        """
        self.problem = problem

        self.cnf_code = 0
        self.cnf_code_names = {}
        self.cnf_code_steps = {}
        self.cnf_code_objects = {}

        self.clauses = []
        self.clause_types = []

        self.true_variales = set()
        self.plan = []

    def write_cnf(self, file_name):
        """Write a DIAMCS CNF file to file_name representing the current encoding.

            (Encoding, str) -> None
        """
        try:
            with open(file_name, 'w') as cnf_file:
                print("Total variables:", self.cnf_code)
                print("Total clauses:", len(self.clauses))

                cnf_file.write("p cnf " + str(self.cnf_code) + " " +
                               str(len(self.clauses)) + "\n")
                for clause in self.clauses:
                    for lit in clause:
                        cnf_file.write(str(lit) + " ")
                    cnf_file.write(" 0\n")

        except IOError:
            raise EncodingException("Error: cannot open CNF file: " + file_name,
                                    encoding_error_code)

    def write_debug_cnf(self, file_name):
        """Write an annotated CNF file to file_name representing the current encoding.

            (Encoding, str) -> None
        """
        try:
            with open(file_name, 'w') as cnf_file:
                cnf_file.write("p cnf " + str(self.cnf_code-1) +
                               " " + str(len(self.clauses)) + "\n")
                for cid, clause in enumerate(self.clauses):
                    for lit in clause:
                        cnf_file.write(str(lit)+"["+self.cnf_code_names[abs(lit)] +
                                       " step"+str(self.cnf_code_steps[abs(lit)])+"] ")
                    cnf_file.write("0 - " + self.clause_types[cid] + "\n")
        except IOError:
            raise EncodingException("Error: cannot open CNF file: " + file_name,
                                    encoding_error_code)

    def write_annotation_file(self, file_name):
        """ Write a file to file_name that describes the variables and clauses
            used in the current encoding.

            (FlatEncoding, str) -> None
        """
        try:
            with open(file_name, 'w') as anno_file:
                for cnf_code in range(1, self.cnf_code):
                    anno_file.write("v " + str(cnf_code) + " " +
                                    self.cnf_code_names[cnf_code] + " step" +
                                    str(self.cnf_code_steps[cnf_code]) + "\n")

                for cid, clause in enumerate(self.clauses):
                    anno_file.write("c " + str(cid) + " " +
                                    self.clause_types[cid] + "\n")
        except IOError:
            raise EncodingException("Error: cannot open annotation file: " +
                                    file_name, encoding_error_code)

    def set_true_variables(self, true_vars):
        """Set the true variables of the encoding.

            (Encoding, [int]) -> None
        """
        self.true_vars = true_vars

    def print_true_variables(self, v_type):
        """Print the true variables of the given type

            (Encoding, str) -> None
        """
        for cnf_code in self.true_vars:
            step, var = self.cnf_code_to_variable[cnf_code]
            print(cnf_code, self.cnf_code_name[cnf_code],
                  "step", self.cnf_code_step[cnf_code])


class EncodingWrapper(object):
    """ This class serves as a wrapper for the encodings implemented in the planner.
        It allows encodings to be registered and instantiated by putting them
        in the cnf_encodings package and adding their names to the registration
        list.
    """

    def __init__(self):
        """ Make a new EncodingWrapper

            (EncodingWrapper) -> None
        """
        self.valid_encodings = {}
        self.default_encoding = ''

    def read_encoding_list(self):
        """ Read the list of encodings and the default encoding. Register
            the listed encodings.

            (EncodingWrapper) -> None
        """
        try:
            with open(encoding_list_file_name, 'r') as encoding_list_file:
                encoding_lines = encoding_list_file.readlines()
                if len(encoding_lines) < 2:
                    raise EncodingException("Error: encoding list does not have enough lines.",
                                            encoding_error_code)
                self.default_encoding = encoding_lines[0].rstrip()
                for line in encoding_lines[1:]:
                    try:
                        line_tokens = line.rstrip().split(' ')
                        self.valid_encodings[line_tokens[0]] = line_tokens[1]
                    except IndexError:
                        raise EncodingException("Error: badly formed line in encoding list: {}".
                                                format(line.rstrip()), encoding_error_code)
        except IOError:
            raise EncodingException("Error: failed to load encoding list {}.".
                                    format(encoding_list_file_name), encoding_error_code)

    def instantiate_encoding(self, encoding_name, problem):
        """ Instantiate the encoding with the given name and options.

            (EncodingWrapper, {str : str}, Problem, bool) -> None
        """
        if encoding_name not in self.valid_encodings:
            raise EncodingException("Error: invalid encoding: {}".format(encoding_name),
                                    encoding_error_code)

        encoding_module = import_module(os.path.dirname(__file__).split("/")[-1] +
                                        '.' + self.valid_encodings[encoding_name])
        self.encoding = getattr(
            encoding_module, encoding_module.encoding_class)(problem)
