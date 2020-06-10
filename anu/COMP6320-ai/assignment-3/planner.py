# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@anu.edu.au)

""" This software implements a SAT-based planning system.
    It allows different encodings and SAT solvers to be plugged in.

    You do not need to look at this file unless you wish to implement more
    complex query strategies for Part 3 of the assignment.
"""

import argparse
import errno
import os
import resource
import subprocess
import sys
import time
import traceback
from parser import Grounder, Parser, ParsingException

from cnf_encodings import EncodingException, EncodingWrapper
from plangraph import PlangraphPreprocessor, PreprocessingException
from solvers import SolverWrapper, SolvingException
from utilities import (GROUND_SUFFIX, PRE_SUFFIX, CodeException,
                       ProblemException, extracting_error_code, remove,
                       solving_error_code, tmp_path)


class PlanningException(CodeException):
    """ An exception to be raised during planning. """

    def __init__(self, message, code):
        self.message = message
        self.code = code

class PreprocessingError(Exception):
    pass


def parse_cmd_line_args(valid_encodings, default_encoding, valid_solvers, default_solver):
    """ Parse the command line arguments and return an object with attributes
        containing the parsed arguments or their default values.
        ([str], str, [str], str) -> argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_file", metavar="DOMAIN",
                        help="The PDDL domain to read.")
    parser.add_argument("problem_file", metavar="PROBLEM",
                        help="The PDDL problem to read.")
    parser.add_argument("exp_name", metavar="EXPNAME",
                        help="A name to use for tmp files.")
    parser.add_argument("horizons", metavar="HORIZONS",
                        help="The horizon(s) for the chosen query strategy.")
    parser.add_argument("-o", "--output", dest="output_file_name",
                        metavar="OUTPUT", help="Write the generated plans to this file.")
    parser.add_argument("-q", "--query_strategy", dest="query_strategy",
                        choices=["fixed", "ramp"], default="fixed",
                        metavar="QUERY", help="Query strategy " +
                        "[%(choices)s] (default: %(default)s)")
    parser.add_argument("-p", "--plangraph", dest="plangraph",
                        choices=["true", "false"], default="false",
                        metavar="PLANGRAPH", help="Compute the plangraph " +
                        "[%(choices)s] (default: %(default)s).")
    parser.add_argument("-l", "--plangraph_constraints", dest="plangraph_constraints",
                        choices=["both", "fmutex", "reachable"], default="both",
                        metavar="PGCONS", help="Which constraints to use from the plangraph " +
                        "[%(choices)s] (default: %(default)s).")
    parser.add_argument("-x", "--exec_semantics", dest="exec_semantics",
                        choices=["parallel", "serial"], default="parallel",
                        metavar="EXECSEM", help="The execution semantics of plans" +
                        "[%(choices)s] (default: %(default)s).")
    parser.add_argument("-e", "--encoding", dest="encoding",
                        choices=list(valid_encodings.keys()), default=default_encoding,
                        metavar="ENCODING", help="The encoding to use " +
                        "[%(choices)s] (default: %(default)s).")
    parser.add_argument("-s", "--solver", dest="solver",
                        choices=list(valid_solvers.keys()), default=default_solver,
                        metavar="SOLVER", help="The SAT solver to use " +
                        "[%(choices)s] (default: %(default)s).")
    parser.add_argument("-t", "--time_out", type=int, dest="time_out",
                        metavar="TIMEOUT", help="SAT solver time out.")
    parser.add_argument("-d", "--debug_cnf", dest="debug_cnf",
                        choices=["true", "false"], default="false",
                        metavar="DBGCNF", help="Write an annotated CNF for debugging " +
                        "[%(choices)s] (default: %(default)s).")
    parser.add_argument("-r", "--remove_tmp", dest="remove_tmp",
                        choices=["true", "false"], default="false", metavar="REMOVETMP",
                        help="Remove tmp files [%(choices)s] (default: %(default)s).")

    args = parser.parse_args()

    args.domain_file_name = args.domain_file
    args.problem_file_name = args.problem_file

    args.plangraph = args.plangraph.lower() == "true"
    args.remove_tmp = args.remove_tmp.lower() == "true"
    args.debug_cnf = args.debug_cnf.lower() == "true"

    if args.query_strategy == "ramp":
        try:
            horizon, horizon_max, horizon_step = list(
                map(int, args.horizons.split(":")))
            if horizon < 1:
                raise Exception("Starting horizon < 1.")
            if horizon_max < horizon:
                raise Exception("Max horizon < horizon.")
            if horizon_step < 1:
                raise Exception("The horizon step is < 1.")
            args.horizons = list(range(horizon, horizon_max + 1, horizon_step))
        except Exception as e:
            print("Error: invalid horizons for ramp up.", args.horizons)
            print(e.message)
            print("    You must supply start:end:step.")
            return None
    elif args.query_strategy == "fixed":
        try:
            horizons = list(map(int, args.horizons.split(":")))
            if min(horizons) < 1:
                raise Exception()
            args.horizons = horizons
        except:
            print("Error: invalid enumerated list of horizons.", args.horizons)
            print("    You must supply h1:h2:h3:...")
            return None

    print("Command line options:")
    print("    Domain file:          {}".format(args.domain_file_name))
    print("    Problem file:         {}".format(args.problem_file_name))
    print("    Experiment name:      {}".format(args.exp_name))
    if args.query_strategy == "ramp":
        print("    Query strategy:        ramp, min_h =", horizon, "max_h =", horizon_max,
              "step_h =", horizon_step)
    elif args.query_strategy == "fixed":
        print("    Query strategy:        enum, h =",
              ", ".join(map(str, args.horizons)))
    else:
        assert False
    print("    Compute plangraph:     {}".format(args.plangraph))
    print("    Plangraph constraints: {}".format(args.plangraph_constraints))
    print("    Encoding:              {}".format(args.encoding))
    print("    Solver                 {}".format(args.solver))
    print("    SAT solver time out    {}".format(args.time_out))
    print("    Write debug CNF:       {}".format(args.debug_cnf))
    print("    Remove tmp files:      {}".format(args.remove_tmp))

    return args


def main():
    start_time = time.time()

    print("Starting SAT-based planner...")
    print("Checking for plugins...")
    try:
        encoding_wrapper = EncodingWrapper()
        encoding_wrapper.read_encoding_list()

        solver_wrapper = SolverWrapper()
        solver_wrapper.read_solver_list()

    except (EncodingException, SolvingException) as e:
        print(e.message)
        sys.exit(1)

    print("Encodings registered:    {}".format(
        len(encoding_wrapper.valid_encodings)))
    print("Solvers registered:      {}".format(
        len(solver_wrapper.valid_solvers)))

    args = parse_cmd_line_args(
        encoding_wrapper.valid_encodings, encoding_wrapper.default_encoding,
        solver_wrapper.valid_solvers, solver_wrapper.default_solver)
    if args is None:
        sys.exit(1)
    arg_processing_time = time.time()
    print("Command line arg processing time: {}".format(
        (arg_processing_time - start_time)))

    # Ensure that the tmp_dir exists
    try:
        os.makedirs(tmp_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            print("Error: could not create temporary directory: {}".format(tmp_path))
            sys.exit(1)

    # Parse the input PDDL
    try:
        parser = Parser(args.domain_file_name, args.problem_file)
        print("Parsing the PDDL domain...")
        parser.parse_domain()
        print("Parsing the PDDL problem...")
        parser.parse_problem()

        print("Simplifying the problem representation...")
        problem = parser.problem
        problem.simplify()
        problem.assign_cond_codes()

        end_parsing_time = time.time()
        print("Parsing time: {}".format(
            (end_parsing_time - arg_processing_time)))

        print("Grounding the problem...")
        pre_file_name = os.path.join(tmp_path, args.exp_name + PRE_SUFFIX)
        ground_file_name = os.path.join(
            tmp_path, args.exp_name + GROUND_SUFFIX)

        grounder = Grounder(problem, pre_file_name, ground_file_name)
        grounder.ground()

        end_grounding_time = time.time()
        print("Grounding time: {}".format(
            end_grounding_time - end_parsing_time))

        print("Simplifying the ground encoding...")
        problem.compute_static_preds()
        problem.link_groundings()
        problem.make_flat_preconditions()
        problem.make_flat_effects()
        problem.get_encode_conds()
        problem.make_cond_and_cond_eff_lists()
        problem.link_conditions_to_actions()
        problem.make_strips_conditions()
        problem.compute_conflict_mutex()

        end_linking_time = time.time()
        print("Simplify time: {}".format(end_linking_time - end_grounding_time))

        object_invariants = []
        if args.plangraph:
            print("Generating Plangraph invariants...")
            plangraph_preprocessor = PlangraphPreprocessor(problem)
            object_invariants = plangraph_preprocessor.run()
            if object_invariants is False:
                raise PreprocessingError('Cannot preprocess plangraph.')

        end_plangraph_time = time.time()
        if args.plangraph:
            print("Plangraph invariants time:",
                  (end_plangraph_time - end_linking_time))

        strips_problem = problem.make_strips_problem()

    except (ParsingException, PreprocessingException, ProblemException) as e:
        print(e)
        sys.exit(1)
    finally:
        if args.remove_tmp:
            try:
                os.system("rm " + pre_file_name)
            except:
                pass
            try:
                os.system("rm " + ground_file_name)
            except:
                pass

    print("Planning...\n")
    try:
        for horizon in args.horizons:
            print("Step:", horizon)
            print("-------------------------------------------------")
            step_start_time = time.time()

            try:
                print("Generating base encoding:", args.encoding, "...")
                encoding_wrapper.instantiate_encoding(
                    args.encoding, strips_problem)
                encoding = encoding_wrapper.encoding
                encoding.encode(horizon, args.exec_semantics,
                                args.plangraph_constraints)
                end_encoding_base_time = time.time()
                print("Encoding generation time:",
                      (end_encoding_base_time - step_start_time))

                print("Writing CNF file...")
                cnf_file_name = os.path.join(tmp_path,
                                             args.exp_name + "_" + str(horizon) + ".cnf")
                encoding.write_cnf(cnf_file_name)
                end_writing_cnf_time = time.time()
                print("Writing time:",
                      (end_writing_cnf_time - end_encoding_base_time))
            except Exception as e:
                print("Exception while generating the CNF!\n")
                print(traceback.format_exc())
                try:
                    os.system("rm " + cnf_file_name)
                except:
                    pass
                sys.exit(0)

            if args.debug_cnf:
                print("Writing debug CNF...")
                encoding.write_debug_cnf(cnf_file_name + "_dbg")
            end_writing_dbg_cnf_time = time.time()
            if args.debug_cnf:
                print(
                    ("Writing time:", (end_writing_dbg_cnf_time - end_writing_cnf_time)))

            try:
                print("Solving...")
                solver_wrapper.instantiate_solver(args.solver, cnf_file_name,
                                                  tmp_path, args.exp_name, args.time_out)
                (sln_res, sln_time, true_vars) = solver_wrapper.solver.solve()
                print("SAT" if sln_res else "UNSAT")
                print("Solution time: ", sln_time)

            except SolvingException as e:
                raise PlanningException(e.message, solving_error_code)
            finally:
                if args.remove_tmp:
                    try:
                        os.system("rm " + cnf_file_name)
                    except:
                        pass
                    try:
                        os.system("rm " + solver_wrapper.solver.sln_file_name)
                    except:
                        pass

            if sln_res:
                encoding.set_true_variables(true_vars)

                try:
                    print("Extracting the plan...")
                    encoding.build_plan(horizon)
                    # problem.make_plan_from_strips(encoding.plan)
                    plan = encoding.plan
                except:
                    print("Exception while extracting the plan!\n")
                    print(traceback.format_exc())
                    sys.exit(0)

                output_file = None
                if args.output_file_name is not None:
                    try:
                        output_file = open(args.output_file_name, "w")
                    except:
                        print("Error: could not open plan file! Not saving plan.")

                num_actions = 0
                print("Plan:")
                for step, s_actions in enumerate(plan):
                    for action in s_actions:
                        a_str = str(action)
                        print(str(step) + ": " + a_str)
                        if output_file is not None:
                            output_file.write(str(step) + ": " + a_str + "\n")
                        num_actions += 1
                if output_file is not None:
                    output_file.close()

                print("Simulating plan for validation.")

                sim_res, plan_cost = problem.simulate_strips_plan(
                    strips_problem, plan)

                if sim_res:
                    print("Plan valid. {} actions.".format(num_actions))
                else:
                    raise PlanningException(
                        "INVALID PLAN!", solving_error_code)

                step_end_time = time.time()
                print("Step time: {}".format(step_end_time - step_start_time))

                break
            step_end_time = time.time()
            print("Step time: {}\n".format(step_end_time - step_start_time))

        end_time = time.time()
        print("Total time: {}\n".format(end_time - start_time))

    except PlanningException as e:
        print("Planning Error: {}\n".format(e.message))
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
