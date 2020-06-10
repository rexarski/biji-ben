# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This file contains a bunch of general stuff.
    You should not need to look at it.
"""

import os
import platform

# Error codes
parsing_error_code = -1
grounding_error_code = -2
preprocessing_error_code = -3
encoding_error_code = -4
solving_error_code = -5
extracting_error_code = -6

# Paths
if platform.system() == 'Linux':
    GRINGO_FILE = "gringo-4.5.4-linux"
elif platform.system() == 'Darwin':
    GRINGO_FILE = "gringo-4.5.4-macos"
else:
    raise OSError("Your system {} is not supported. Please run on Mac or Linux".format(
        platform.system()))

grounder_path = os.path.join(os.path.dirname(__file__), "gringo", GRINGO_FILE)
tmp_path = os.path.join(os.path.dirname(__file__), "tmp_files")

PRE_SUFFIX = ".pre"
GROUND_SUFFIX = ".grd"
grounder_run_success_code = 0
var_alphabet = "ABCDEFGHIJKLMNOPQRSTUFWXYZ"
lower_var_alphabet = var_alphabet.lower()

# Problem
default_type_name = "object"
cond_prefix = 'c'
neg_prec_prefix = "nprec_"
equality_prefix = "equal"
inequality_prefix = "not_equal"

NOT_CONDITION = "not"
AND_CONDITION = "and"
OR_CONDITION = "or"
IMPLY_CONDITION = "imply"
FORALL_CONDITION = "forall"
EXISTS_CONDITION = "exists"
INCREASE_CONDITION = "increase"
EQUALS_CONDITION = "="
NOT_EQUALS_CONDITION = "!="
CONDITIONAL_EFFECT = "when"

valid_requirements = [':typing', ':action-costs', ':adl', ":strips",
                      ":negative-preconditions", ":equality", ":derived-predicates"]

# Precisely Split Encoding
PRE_COND = 0
POST_COND = 1
split_id_conds = {(PRE_COND,  False): "PRE", (PRE_COND, True):  "NPRE",
                  (POST_COND, False): "ADD", (POST_COND, True): "DEL"}


class CodeException(Exception):
    """ This class extends the standard exception with an error code. """

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class ProblemException(CodeException):
    """ An exception to be used when things in this module go wrong. """


def remove(file_name):
    """ Remove the file with the given file name.

        (str) -> None
    """
    from os import system
    system('rm ' + file_name)


def asp_convert(string):
    """ Convert the given string to be suitable for ASP. Currently this means
        replacing - with _. It is a bit unsafe in that if name exist that are
        identical except one has a - and one has a _ in the same place, then
        this wont catch it, but if you do that stuff you.

       (str) -> str
    """
    return string.replace("-", "__").lower()
