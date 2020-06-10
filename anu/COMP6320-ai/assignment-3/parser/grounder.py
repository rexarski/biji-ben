# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This file represents a Problem in ASP (Answer Set Programming) and uses
    gringo, the grounding system of the clasp ASP solver) to find all reachable
    atoms. It is very efficient.
"""

import itertools
import os
import subprocess

from problem import (AndCondition, ConditionalEffect, EqualsCondition,
                     ExistsCondition, ForAllCondition, Function,
                     IncreaseCondition, NotCondition, Object, OrCondition,
                     Predicate, PredicateCondition, Type)
from utilities import (asp_convert, default_type_name, equality_prefix,
                       grounder_path, grounder_run_success_code,
                       grounding_error_code, inequality_prefix,
                       neg_prec_prefix, var_alphabet)

from .parser import ParsingException


class Grounder:
    """ Used to ground PDDL domains and problems. """

    def __init__(self, problem, pre_file_name, grounding_file_name):
        """ Create the grounding system.
            (Grounder, Problem) -> None
        """
        self.problem = problem
        self.pre_file_name = pre_file_name
        self.grounding_file_name = grounding_file_name

        #The following are simply maps from the modified names of the problem
        #components back to the components themselves
        self.asp_types = dict(problem.types)

        self.asp_objects = {}
        self.asp_predicates = {}
        self.asp_functions = {}
        self.asp_actions = {}
        self.asp_dp = {}

    def rename_asp_components(self):
        """ Rename the appropriate problem elements using the function asp_convert
            defined in utilities.
            (Grounder) -> None
        """
        #Types
        self.asp_types = {}
        for ttype in self.problem.types.values():
            ttype.asp_name = asp_convert(ttype.name)
            self.asp_types[ttype.asp_name] = ttype

        #Objects
        for obj in self.problem.objects.values():
            obj.asp_name = asp_convert(obj.name)
            self.asp_objects[obj.asp_name] = obj

        #Predicates
        for pred in self.problem.predicates.values():
            pred.asp_name = asp_convert(pred.name)
            self.asp_predicates[pred.asp_name] = pred

        #Functions
        for func in self.problem.functions.values():
            func.asp_name = asp_convert(func.name)
            self.asp_functions[func.asp_name] = func

        #Actions
        for action in self.problem.actions.values():
            action.asp_name = asp_convert(action.name)
            self.asp_actions[action.asp_name] = action

    def write_prec_asp(self, condition, out_file):
        """ Write the description of this conditon as a precondition into asp.
            (Grounder, Condition, file) -> None
        """
        if isinstance(condition, PredicateCondition):
            pred_name = condition.pred.asp_name
            if not condition.sign:
                pred_name = neg_prec_prefix + pred_name
            if condition.variables:
                v_strs, p_strs, alph_pos = [], [], 0
                for v in condition.variables:
                    if v in condition.relevant_vars:
                        v_strs.append(var_alphabet[alph_pos])
                        p_strs.append(var_alphabet[alph_pos])
                        alph_pos += 1
                    else:
                        p_strs.append(self.problem.objects[v].asp_name)
                if v_strs:
                    out_file.write("reachable(" + condition.cond_code + "(" +\
                        ", ".join(v_strs) + ")) :- reachable_f(" + pred_name +\
                        "(" + ", ".join(p_strs) + ")" + ").\n")
                else:
                    out_file.write("reachable(" + condition.cond_code + ") :- reachable_f(" +\
                        pred_name + "(" + ", ".join(p_strs) + ")" + ").\n")
            else:
                out_file.write("reachable(" + condition.cond_code + ") :- reachable_f(" +\
                    pred_name + ").\n")

        elif isinstance(condition, AndCondition):
            cond_strs = []
            for cond in condition.conditions:
                if cond.relevant_vars:
                    cond_strs.append("reachable(" + cond.cond_code + "(" +\
                        ", ".join([var_alphabet[condition.var_indices[v][0]]\
                        for v in cond.relevant_vars]) + "))")
                else:
                    cond_strs.append("reachable(" + cond.cond_code + ")")
            if condition.relevant_vars:
                out_file.write("reachable(" + condition.cond_code + "(" +\
                    ", ".join(var_alphabet[:len(condition.relevant_vars)]) + ")) :- " +\
                    ", ".join(cond_strs) + ".\n")
            else:
                out_file.write("reachable(" + condition.cond_code + ") :- " +\
                    ", ".join(cond_strs) + ".\n")

            for cond in condition.conditions:
                self.write_prec_asp(cond, out_file)

        elif isinstance(condition, OrCondition):
            for cond in condition.conditions:
                if condition.relevant_vars:
                    out_file.write("reachable(" + condition.cond_code + "(" +\
                    ", ".join(var_alphabet[:len(condition.relevant_vars)]) + ")) :- ")
                else:
                    out_file.write("reachable(" + condition.cond_code + ") :- ")

                if cond.relevant_vars:
                    out_file.write("reachable(" + cond.cond_code + "(" +\
                    ", ".join([var_alphabet[condition.var_indices[v][0]]\
                    for v in cond.relevant_vars]) + "))")
                else:
                    out_file.write("reachable(" + cond.cond_code + ")")

                extra_bindings = [condition.var_types[v].name + "(" + var_alphabet[vid] + ")"\
                    for vid, v in enumerate(condition.relevant_vars) if v not in cond.relevant_vars]
                if extra_bindings:
                    out_file.write(", " + ", ".join(extra_bindings))
                out_file.write(".\n")

            for cond in condition.conditions:
                self.write_prec_asp(cond, out_file)

        elif isinstance(condition, ForAllCondition):
            if condition.relevant_vars:
                out_file.write("reachable(" + condition.cond_code + "(" +\
                    ", ".join(var_alphabet[:len(condition.relevant_vars)]) + ")) :- ")
            else:
                out_file.write("reachable(" + condition.cond_code + ") :- ")

            cond_strs = []
            if condition.condition.relevant_vars:
                for obj in condition.v_type.objects:
                    cond_strs.append("reachable(" + condition.condition.cond_code + "(" +\
                        ", ".join([var_alphabet[condition.var_indices[v][0]]\
                        if v in condition.relevant_vars else obj.asp_name\
                        for v in condition.condition.relevant_vars]) + "))")
            else:
                cond_strs.append("reachable(" + condition.condition.cond_code + ")")
            out_file.write(", ".join(cond_strs) + ".\n")
            self.write_prec_asp(condition.condition, out_file)

        elif isinstance(condition, ExistsCondition):
            if condition.relevant_vars:
                out_file.write("reachable(" + condition.cond_code + "(" +\
                    ", ".join(var_alphabet[:len(condition.relevant_vars)]) + ")) :- ")
            else:
                out_file.write("reachable(" + condition.cond_code + ") :- ")

            if condition.condition.relevant_vars:
                cond_str = "reachable(" + condition.condition.cond_code + "(" +\
                    ", ".join([var_alphabet[condition.var_indices[v][0]]\
                    if v in condition.relevant_vars\
                    else var_alphabet[len(condition.relevant_vars)]\
                    for v in condition.condition.relevant_vars]) + "))"
            else:
                cond_str = "reachable(" + condition.condition.cond_code + ")"
            out_file.write(cond_str + ".\n")

            self.write_prec_asp(condition.condition, out_file)

        elif isinstance(condition, EqualsCondition):
            prefix = inequality_prefix if not condition.sign else equality_prefix
            v_strs, p_strs, alph_pos = [], [], 0
            for v in condition.variables:
                if v in condition.relevant_vars:
                    v_strs.append(var_alphabet[alph_pos])
                    p_strs.append(var_alphabet[alph_pos])
                    alph_pos += 1
                else:
                    p_strs.append(self.problem.objects[v].asp_name)
            out_file.write("reachable(" + condition.cond_code + "(" +\
                ", ".join(v_strs) + ")) :- " + prefix + "(" + ", ".join(p_strs) + ").\n")

        else:
            raise ParsingException("Invalid condition type in precondion: " +\
                str(condition), grounding_error_code)


    def write_eff_asp(self, condition, out_file):
        """ Write the effect of this condition into asp.
            (Grounder, Condition, file) -> None
        """
        if isinstance(condition, PredicateCondition):
            if condition.sign or condition.pred in self.problem.neg_precs:
                pred_name = condition.pred.asp_name
                if not condition.sign:
                    pred_name = neg_prec_prefix + pred_name
                if condition.variables:
                    v_strs, p_strs, alph_pos = [], [], 0
                    for v in condition.variables:
                        if v in condition.relevant_vars:
                            v_strs.append(var_alphabet[alph_pos])
                            p_strs.append(var_alphabet[alph_pos])
                            alph_pos += 1
                        else:
                            p_strs.append(self.problem.objects[v].asp_name)
                    out_file.write("reachable_f(" + pred_name +\
                        "(" + ", ".join(p_strs) + ")" + ") :- reachable(" +\
                            condition.cond_code + "(" + ", ".join(v_strs) + ")).\n")
                else:
                    out_file.write("reachable_f(" + pred_name + ") :- reachable(" +\
                        condition.cond_code + ").\n")

        elif isinstance(condition, AndCondition):
            if condition.relevant_vars:
                and_str = "reachable(" + condition.cond_code + "(" +\
                        ", ".join(var_alphabet[:len(condition.relevant_vars)]) + "))"
            else:
                and_str = "reachable(" + condition.cond_code + ")"
            for cond in condition.conditions:
                if cond.relevant_vars:
                    out_file.write("reachable(" + cond.cond_code + "(" +\
                        ", ".join([var_alphabet[condition.var_indices[v][0]]\
                        for v in cond.relevant_vars]) + ")) :- " + and_str + ".\n")
                else:
                    out_file.write("reachable(" + cond.cond_code + ") :- " + and_str + ".\n")

            for cond in condition.conditions:
                self.write_eff_asp(cond, out_file)

        elif isinstance(condition, ForAllCondition):
            if condition.relevant_vars:
                forall_str = "reachable(" + condition.cond_code + "(" +\
                    ", ".join(var_alphabet[:len(condition.relevant_vars)]) + "))"
            else:
                forall_str = "reachable(" + condition.cond_code + ")"
            forall_str += ", " + condition.v_type.name + "(" +\
                var_alphabet[len(condition.relevant_vars)] + ")"
            if condition.condition.relevant_vars:
                v_str = "reachable(" + condition.condition.cond_code + "(" +\
                    ", ".join([var_alphabet[condition.var_indices[v][0]]\
                    if v in condition.relevant_vars else\
                    var_alphabet[len(condition.relevant_vars)]\
                    for v in condition.condition.relevant_vars]) + "))"
                out_file.write(v_str + " :- " + forall_str + ".\n")
            else:
                out_file.write("reachable(" + condition.condition.cond_code + ") :- " +\
                    forall_str + ".\n")

            self.write_eff_asp(condition.condition, out_file)

        elif isinstance(condition, IncreaseCondition):
            #print "Increase: ", condition.cond_code
            pass
        elif isinstance(condition, ConditionalEffect):
            if condition.relevant_vars:
                self_str = "reachable(" + condition.cond_code + "(" +\
                    ", ".join(var_alphabet[:len(condition.relevant_vars)]) + "))"
            else:
                self_str = "reachable(" + condition.cond_code + ")"
            if condition.condition.relevant_vars:
                cond_str = "reachable(" + condition.condition.cond_code + "(" +\
                    ", ".join([var_alphabet[condition.var_indices[v][0]]\
                    for v in condition.condition.relevant_vars]) + "))"
            else:
                cond_str = "reachable(" + condition.condition.cond_code + ")"
            if condition.effect.relevant_vars:
                eff_str = "reachable(" + condition.effect.cond_code + "(" +\
                    ", ".join([var_alphabet[condition.var_indices[v][0]]\
                    for v in condition.effect.relevant_vars]) + "))"
            else:
                eff_str = "reachable(" + condition.effect.cond_code + ")"
            out_file.write(eff_str + " :- " + self_str + ", " + cond_str + ".\n")

            self.write_prec_asp(condition.condition, out_file)
            self.write_eff_asp(condition.effect, out_file)

        else:
            raise ParsingException("Invalid condition type in effect: " +\
                str(condition), grounding_error_code)

    def write_asp(self):
        """ Write an ASP representation of the problem to pre_file_name for
            grounding.

            (Grounder, file, bool) -> None
        """
        with open(self.pre_file_name, 'w') as out_file:
           #Objects
           for obj in self.problem.objects.values():
               out_file.write(obj.otype.asp_name + "(" +\
                   obj.asp_name + ").\n")

           #Typing
           for ttype in self.problem.types.values():
               if ttype.parent is not None:
                   out_file.write(ttype.parent.asp_name + "(" + var_alphabet[0] +\
                       ") :- " + ttype.asp_name + "(" + var_alphabet[0] + ").\n")

           #Actions and derived predicates
           for action in self.problem.actions.values():
               #self.problem.derived_predicates.itervalues()):
               if action.parameters:
                   action_str = action.asp_name + "(" +\
                       ", ".join(var_alphabet[:len(action.parameters)]) + ")"
               else:
                   action_str = action.asp_name

               reachable_str = "reachable_a("

               #Precondition
               if action.precondition:
                   if not action.parameters:
                       out_file.write(reachable_str + action_str + ") :- " +\
                           "reachable(" + action.precondition.cond_code + ").\n")
                   else:
                       out_file.write(reachable_str + action_str + ") :- " +\
                           "reachable(" + action.precondition.cond_code + "(" +\
                           ", ".join([var_alphabet[action.var_indices[v]]\
                           for v in action.precondition.relevant_vars]) + "))")
                       for pid, (param, ptype) in enumerate(action.parameters):
                           if param not in action.precondition.relevant_vars:
                               out_file.write(", " + ptype.name + "(" + var_alphabet[pid] + ")")
                       out_file.write(".\n")
                   self.write_prec_asp(action.precondition, out_file)
               else:
                   out_file.write(reachable_str + action_str + ").\n")

               #Effect
               if not action.parameters:
                   out_file.write("reachable(" + action.effect.cond_code + ") :- " +\
                       reachable_str + action.asp_name + ").\n")
               else:
                   eff_vars = [var_alphabet[action.var_indices[v]]\
                       for v in action.effect.relevant_vars]
                   if eff_vars:
                       out_file.write("reachable(" + action.effect.cond_code + "(" +\
                           ", ".join(eff_vars) + ")) :- " + reachable_str + action_str + ").\n")
                   else:
                       out_file.write("reachable(" + action.effect.cond_code +\
                           ") :- " + reachable_str + action_str + ").\n")
               self.write_eff_asp(action.effect, out_file)

           #start state
           for init_fact, init_args in self.problem.initial_state:
               if init_args:
                   out_file.write("reachable_f(" + init_fact.asp_name + "(" +\
                       ", ".join([self.problem.objects[v].asp_name for v in init_args]) + ")).\n")
               else:
                   out_file.write("reachable_f(" + init_fact.asp_name + ").\n")

           out_file.write(equality_prefix + "(" + var_alphabet[0] +\
               ", " + var_alphabet[1] + ") :- " + default_type_name + "(" +\
               var_alphabet[0] + "), " + default_type_name + "(" + var_alphabet[1] +\
               "), " + var_alphabet[0] + " = " + var_alphabet[1] + ".\n")

           #Inequalities
           for (v1, v2) in self.problem.inequalities:
               out_file.write(inequality_prefix + "(" + self.problem.objects[v1].asp_name +\
                   ", " + self.problem.objects[v2].asp_name + ").\n")

           #negated preconditions in start state
           for pred, grounding in self.problem.neg_initial_state:
               if not grounding:
                   out_file.write("reachable_f(" + neg_prec_prefix + pred.asp_name + ").\n")
               else:
                   out_file.write("reachable_f(" + neg_prec_prefix + pred.asp_name +\
                       "(" + ", ".join([self.problem.objects[v].asp_name for v in grounding]) + ")).\n")

           #goal
           out_file.write("reachable_goal :- " +\
                           "reachable(" + self.problem.goal.cond_code + ").\n")
           self.write_prec_asp(self.problem.goal, out_file)

           #Only show the reachability info
           out_file.write("#show reachable_a/1.\n")
           out_file.write("#show reachable_f/1.\n")
           out_file.write("#show reachable/1.\n")
           out_file.write("#show reachable_goal/0.\n")


    def ground(self):
        """ Write the problem out into ASP and use Gringo to ground it and then
            read the solution back in to the problem

            (Problem, str, str) -> None
        """
        self.rename_asp_components()
        self.write_asp()
        reachable_goal = False
        try:
           solver_res = subprocess.call(grounder_path + " " + self.pre_file_name + " > " +\
               self.grounding_file_name, shell=True)
           if solver_res != grounder_run_success_code:
                raise ParsingException("Error: There was a problem running the grounder: " +\
                    grounder_path, grounding_error_code)

           with open(self.grounding_file_name) as grounding_file:
               for line in grounding_file:
                   line = line.strip()
                   if line == "0":
                       break

               for line in grounding_file:
                   line = line.strip()
                   tokens = line.rstrip(")").split(" ")
                   if len(tokens) < 2: continue
                   tokens = tokens[1].split("(")
                   if tokens[0] == "reachable":
                       cond_name = tokens[1]
                       if len(tokens) == 3:
                           cond_args = tokens[2].split(",")
                       else:
                           cond_args = []
                       cond_args = [self.asp_objects[arg].name for arg in cond_args]
                       self.problem.code_conds[cond_name].groundings.append(tuple(cond_args))

                   elif tokens[0] == "reachable_a":
                       pred_name = tokens[1]
                       if len(tokens) == 3:
                           pred_args = tokens[2].split(",")
                       else:
                           pred_args = []

                       pred_args = [self.asp_objects[arg].name for arg in pred_args]
                       self.asp_actions[pred_name].groundings.append(tuple(pred_args))

                   elif tokens[0] == "reachable_f":
                       pred_name = tokens[1]
                       if len(tokens) == 3:
                           pred_args = tokens[2].split(",")
                       else:
                           pred_args = []
                       pred_args = [self.asp_objects[arg].name for arg in pred_args]
                       if pred_name.startswith(neg_prec_prefix):
                           self.asp_predicates[pred_name[len(neg_prec_prefix):]].\
                               neg_groundings.append(tuple(pred_args))
                       else:
                           self.asp_predicates[pred_name].groundings.append(tuple(pred_args))

                   elif tokens[0] == "reachable_goal":
                       reachable_goal = True
                   else:
                       raise ParsingException("Error: unknown line in grounding file: " +\
                           line, grounding_error_code)

        except IOError as e:
            print(e)
            raise ParsingException("Error: could not open the grounding file: " +\
                grounding_file_name, grounding_error_code)
        except OSError as e:
            sys.stdout.flush()
            print(e.message)
            raise ParsingException("Error: There was a problem running the grounder: "+\
                grounder_path, grounding_error_code)

        if not reachable_goal:
            raise ParsingException("Error: the goal is not relaxed reachable.",
                grounding_error_code)
