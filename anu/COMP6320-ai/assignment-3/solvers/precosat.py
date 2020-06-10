# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This file is responsible for calling the PrecoSAT binary and extracting the
    satisfying valuation which it returns (or detecting unsat, time out etc.)
"""

import os
import platform
import subprocess
import sys
import time

from .solver_base import (Solver, SolvingException, solver_error_code,
                          solver_sat_code, solver_time_out_code,
                          solver_unsat_code)

solver_class = 'PrecoSAT'

if platform.system() == 'Linux':
    PRECOSAT_FILE = "precosat-570-linux"
elif platform.system() == 'Darwin':
    PRECOSAT_FILE = "precosat-576-macos"
else:
    raise OSError("Your system {} is not supported. Please run on Mac or Linux".format(
        platform.system()))


class PrecoSAT(Solver):

    solver_sat_code = 10
    solver_unsat_code = 20
    solver_unknown_code = 0

    solver_path = os.path.join(os.path.dirname(__file__), PRECOSAT_FILE)

    def __init__(self, cnf_file_name, tmp_path, exp_name, time_out):
        self.cnf_file_name = cnf_file_name
        self.tmp_path = tmp_path
        self.exp_name = exp_name
        self.time_out = time_out

        self.sln_file_name = os.path.join(tmp_path, exp_name + '.sln')
        # See https://stackoverflow.com/a/13143013
        self.run_str = 'exec {}'.format(self.solver_path)
        self.run_str += " " + cnf_file_name + " > " + self.sln_file_name

    def solve(self):
        cpu_time = 0
        try:
            with open(self.sln_file_name, 'w') as sln_file:
                cpu_time = time.time()
                solver_res = subprocess.call(
                    self.run_str, stdout=sln_file, stderr=sln_file, shell=True, timeout=self.time_out)
                cpu_time = time.time() - cpu_time
            if solver_res not in [self.solver_sat_code, self.solver_unsat_code,
                                  self.solver_unknown_code]:
                with open(self.sln_file_name, 'r') as sln_file:
                    sln_lines = sln_file.readlines()
                raise SolvingException("There was a problem running precosat. Return code: {}\n{}".format(
                    str(solver_res), '\n'.join(sln_lines)), solver_error_code)
        except IOError as e:
            raise SolvingException("Error: could not open solution file: " + self.sln_file_name,
                                   solver_error_code)
        except OSError as e:
            sys.stdout.flush()
            raise SolvingException("Error: There was a problem running the solver: " + self.run_str,
                                   solver_error_code)
        except subprocess.TimeoutExpired as e:
            raise SolvingException(
                "The SAT solver has timed out after {}s.".format(self.time_out), solver_time_out_code)
        try:
            with open(self.sln_file_name, 'r') as sln_file:
                sln_lines = sln_file.readlines()
                linepos = 0
                for linepos, line in enumerate(sln_lines):
                    if line[0] == 's':
                        break
                if linepos < len(sln_lines):
                    result = sln_lines[linepos].rstrip().split(' ')[1]
                    if result == 'SATISFIABLE':
                        true_vars = []
                        for i in range(len(sln_lines)):
                            if sln_lines[i][0] == 'v':
                                current_vars = []
                                a = sln_lines[i].split(' ')[1:]
                                a = map(int, a)
                                for x in a:
                                    if x > 0:
                                        current_vars.append(x)
                                true_vars += current_vars
                        return (True, cpu_time, true_vars)
                    elif result == 'UNSATISFIABLE':
                        return (False, cpu_time, [])
                    elif sln_lines[linepos].rstrip() == 's UNKNOWN':
                        raise SolvingException(
                            "Solving timed out.", solver_time_out_code)
                    raise SolvingException("Solving CNF instance " +
                                           self.cnf_file_name + " resulted in an error:\n" +
                                           "\n".join(sln_lines),
                                           solver_error_code)

                raise SolvingException("There was a problem in the solution file: " +
                                       self.sln_file_name, solver_error_code)
        except IOError:
            raise SolvingException("could not open solution file: " +
                                   self.sln_file_name, solver_error_code)
