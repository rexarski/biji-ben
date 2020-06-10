# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala ({enrico.scala,miquel.ramirez}@gmail.com)

""" This file implements a plangraph computation. It differs from
    the standard computation in that both positive and negative literals are included.
    This allows it to do slightly strong propagation and find invariants beyond standard
    -f1 v -f2 fluent mutexes. However, these more expressive invariants are
    discarded for the sake of this assignment.

    ****    You do not need to look at this file.   ****
"""

import itertools
import os
import random
import sys
import time

from problem import (Action, AndCondition, ConditionalEffect, EqualsCondition,
                     ExistsCondition, ForAllCondition, Function,
                     IncreaseCondition, NotCondition, Object, OrCondition,
                     Predicate, PredicateCondition, Type)
from utilities import CodeException, neg_prec_prefix, preprocessing_error_code


class PreprocessingException(CodeException):
    """ An exception to be raised in the even that something goes wrong with
        the preprocessing process. """


class PlangraphPreprocessor:
    """ Generate a plangraph to perform reachability analysis and produce a set
        of invariants.
    """

    def __init__(self, problem):
        """ Make a new plangraph preprocessor

            (Encoding, Problem, ArgProcessor, bool) -> None
        """
        self.problem = problem

    def run(self):
        """ Run the preprocessor and modify the problem in the required way.
            Return iff the goal might be achievable.

           (PlangraphPreprocessor) -> bool
        """
        first_layer_actions = {}
        first_layer_fluents = {}

        conflicts = self.problem.conflicts

        state_mutexes = {}
        action_mutexes = {}

        output_state_mutexes = []
        state = set()
        fluent_list = []
        for pred in self.problem.predicates.values():
            for grounding in pred.groundings:
                pg_pair = (pred, grounding)
                fluent = (pred, grounding,
                          (pg_pair in self.problem.initial_state))
                not_fluent = (pred, grounding, not fluent[2])
                fluent_list.append(fluent)
                fluent_list.append(not_fluent)

                first_layer_fluents[fluent] = 0
                first_layer_fluents[not_fluent] = None
                state.add(fluent)
                state_mutexes[fluent] = set()
                state_mutexes[not_fluent] = set()

        remaining_actions = set()
        for action in self.problem.actions.values():
            for grounding in action.groundings:
                ag_pair = (action, grounding)
                remaining_actions.add(ag_pair)
                first_layer_actions[ag_pair] = None
                action_mutexes[ag_pair] = {}

        # Add noop actions
        noops = []
        for pred in self.problem.predicates.values():
            for sign in [True, False]:

                if sign:
                    noop_name = "noop_" + pred.name
                else:
                    noop_name = "noop_not_" + pred.name

                noop_act = Action(noop_name, [], [], None, None, False)
                noop_act.is_noop = True
                noop_act.strips_preconditions = {}
                noop_act.strips_effects = {}

                for grounding in pred.groundings:
                    ag_pair1 = (noop_act, grounding)
                    noops.append(ag_pair1)
                    pre_eff = (pred, grounding, sign)
                    remaining_actions.add(ag_pair1)

                    action_mutexes[ag_pair1] = {}

                    first_layer_actions[ag_pair1] = None
                    conflicts[ag_pair1] = set()
                    noop_act.strips_preconditions[grounding] = set([pre_eff])
                    noop_act.strips_effects[grounding] = set([pre_eff])

                    # Inform preds
                    if sign:
                        pred.ground_precs[grounding].add(ag_pair1)
                        pred.ground_adds[grounding].add(ag_pair1)
                    else:
                        pred.ground_nprecs[grounding].add(ag_pair1)
                        pred.ground_dels[grounding].add(ag_pair1)

                    # Make conflicts
                    neg_pre_eff = (pred, grounding, not sign)
                    for ag_pair2 in remaining_actions:
                        if ag_pair2 == ag_pair1:
                            continue
                        a2, g2 = ag_pair2
                        if neg_pre_eff in a2.strips_preconditions[g2] or\
                                neg_pre_eff in a2.strips_effects[g2]:
                            conflicts[ag_pair1].add(ag_pair2)
                            conflicts[ag_pair2].add(ag_pair1)

        actions = set()
        step = 0
        new_actions = set([-1])
        broken_mutexes = set()
        print("Step:", end=' ')
        sys.stdout.flush()
        while new_actions or broken_mutexes:
            step_time = time.time()

            print(step, end=' ')
            sys.stdout.flush()

            new_fluents = set()
            new_actions = set()
            # Try and execute actions
            for ag_pair1 in remaining_actions:
                action1, grounding1 = ag_pair1
                exec_action = True
                for prec in action1.strips_preconditions[grounding1]:
                    if prec not in state:
                        exec_action = False
                        break
                if not exec_action:
                    continue
                for f1, f2 in itertools.combinations(action1.strips_preconditions[grounding1], 2):
                    if f1 in state_mutexes[f2]:
                        exec_action = False
                        break
                if not exec_action:
                    continue

                first_layer_actions[ag_pair1] = step
                actions.add(ag_pair1)
                new_actions.add(ag_pair1)

                # compute mutexes with existing actions
                for prec1 in action1.strips_preconditions[grounding1]:
                    for prec2 in state_mutexes[prec1]:
                        prec_pair = (prec1, prec2)
                        rev_prec_pair = (prec2, prec1)

                        if prec2[2]:
                            p_list = prec2[0].ground_precs[prec2[1]]
                        else:
                            p_list = prec2[0].ground_nprecs[prec2[1]]
                        for ag_pair2 in p_list:
                            if ag_pair2 not in actions:
                                continue

                            if ag_pair1 < ag_pair2:
                                if ag_pair2 not in action_mutexes[ag_pair1]:
                                    action_mutexes[ag_pair1][ag_pair2] = 1
                                else:
                                    action_mutexes[ag_pair1][ag_pair2] += 1
                            else:
                                if ag_pair1 not in action_mutexes[ag_pair2]:
                                    action_mutexes[ag_pair2][ag_pair1] = 1
                                else:
                                    action_mutexes[ag_pair2][ag_pair1] += 1

                for f1 in action1.strips_effects[grounding1]:
                    # break existing mutexes
                    if f1 in state:
                        for f2 in state_mutexes[f1]:
                            break_pair = (f1, f2)
                            break_mutex = f2 in action1.strips_effects[grounding1]
                            if not break_mutex:
                                if f2[2]:
                                    e_list = f2[0].ground_adds[f2[1]]
                                else:
                                    e_list = f2[0].ground_dels[f2[1]]
                                for ag_pair2 in e_list:
                                    if ag_pair2 in actions and ag_pair1 != ag_pair2 and\
                                            ag_pair2 not in conflicts[ag_pair1]:
                                        if ag_pair2 not in action_mutexes[ag_pair1] and\
                                                ag_pair1 not in action_mutexes[ag_pair2]:
                                            break_mutex = True
                                            break
                            if break_mutex:
                                if (f2, f1) not in broken_mutexes:
                                    broken_mutexes.add((f1, f2))
                    else:
                        new_fluents.add(f1)

            new_broken_mutexes = set()
            for f_mutex in broken_mutexes:
                f1, f2 = f_mutex
                rev_f_mutex = (f2, f1)

                state_mutexes[f1].remove(f2)
                state_mutexes[f2].remove(f1)

                if f1[2]:
                    p1_list = f1[0].ground_precs[f1[1]]
                else:
                    p1_list = f1[0].ground_nprecs[f1[1]]

                if f2[2]:
                    p2_list = f2[0].ground_precs[f2[1]]
                else:
                    p2_list = f2[0].ground_nprecs[f2[1]]

                for ag_pair1 in p1_list:
                    if ag_pair1 not in actions:
                        continue
                    action1, grounding1 = ag_pair1
                    for ag_pair2 in p2_list:

                        if ag_pair2 not in actions or ag_pair1 == ag_pair2:
                            continue
                        action2, grounding2 = ag_pair2

                        m_pair = (ag_pair1, ag_pair2)
                        rev_m_pair = (ag_pair2, ag_pair1)

                        if ag_pair1 < ag_pair2:
                            action_mutexes[ag_pair1][ag_pair2] -= 1

                            mutex_broken = not action_mutexes[ag_pair1][ag_pair2]
                            if mutex_broken:
                                del action_mutexes[ag_pair1][ag_pair2]
                        else:
                            action_mutexes[ag_pair2][ag_pair1] -= 1

                            mutex_broken = not action_mutexes[ag_pair2][ag_pair1]
                            if mutex_broken:
                                del action_mutexes[ag_pair2][ag_pair1]

                        if mutex_broken and ag_pair2 not in conflicts[ag_pair1]:
                            # Here we may additionally break a set of fluent mutexes in the next step
                            for eff1 in action1.strips_effects[grounding1]:
                                for eff2 in action2.strips_effects[grounding2]:
                                    if eff1 != eff2 and eff2 in state_mutexes[eff1]:
                                        new_broken_mutexes.add((eff1, eff2))

            for f1 in new_fluents:
                if f1[2]:
                    e_list1 = f1[0].ground_adds[f1[1]]
                else:
                    e_list1 = f1[0].ground_dels[f1[1]]

                # make new fluent and action mutexes
                for f2 in state:
                    # if f2 not in allowed_fluent_mutexes[f1]: continue

                    if f2[2]:
                        e_list2 = f2[0].ground_adds[f2[1]]
                    else:
                        e_list2 = f2[0].ground_dels[f2[1]]

                    any_adder = False
                    for ag_pair1 in e_list1:
                        if ag_pair1 not in actions:
                            continue
                        for ag_pair2 in e_list2:
                            if ag_pair2 not in actions:
                                continue

                            if ag_pair1 == ag_pair2 or\
                                (ag_pair2 not in conflicts[ag_pair1] and
                                 ag_pair2 not in action_mutexes[ag_pair1] and
                                 ag_pair1 not in action_mutexes[ag_pair2]):

                                any_adder = True
                                break
                        if any_adder:
                            break

                    if not any_adder:
                        state_mutexes[f1].add(f2)
                        state_mutexes[f2].add(f1)

                state.add(f1)
                first_layer_fluents[f1] = step+1

            broken_mutexes = set()
            for f_pair in new_broken_mutexes:
                f1, f2 = f_pair
                if f2 in state_mutexes[f1] and (f2, f1) not in broken_mutexes:
                    broken_mutexes.add(f_pair)

            remaining_actions.difference_update(new_actions)
            # Save the fluent mutexes
            layer_mutexes = []
            for f1, fs in state_mutexes.items():
                for f2 in fs:
                    if f1 < f2 and (f1[0] != f2[0] or f1[1] != f2[1]):
                        layer_mutexes.append((f1, f2))

            output_state_mutexes.append(layer_mutexes)
            step += 1

        # Check to see if the goal is possibly satisfiable
        for prec in self.problem.flat_ground_goal_preconditions:
            if not isinstance(prec[0], PredicateCondition):
                assert False, "Complex goal not implemented"

            fluent = (prec[0].pred,
                      prec[0].ground_conditions[prec[1]], prec[2])
            if fluent not in state:
                print("Goal is not relaxed reachable:",
                      fluent[0].name, fluent[1], fluent[2])
                return False

        for pred in self.problem.predicates.values():
            for grounding in pred.groundings:
                if sign:
                    pred.ground_precs[grounding].pop()
                    pred.ground_adds[grounding].pop()
                else:
                    pred.ground_nprecs[grounding].pop()
                    pred.ground_dels[grounding].pop()

        # Find the fluents and actions which never become true
        invalid_actions = set()
        invalid_fluents = set()
        static_fluents = set()

        for fluent, step in first_layer_fluents.items():
            if step is None:
                if fluent[2]:
                    invalid_fluents.add(fluent[:2])
                else:
                    static_fluents.add(fluent[:2])

        for action, step in first_layer_actions.items():
            if step is None and not action[0].is_noop:
                invalid_actions.add(action)

        if static_fluents:
            self.problem.static_preds.update(static_fluents)

        for pred, grounding in invalid_fluents:
            pred.groundings.remove(grounding)

        for action, grounding in invalid_actions:
            action.groundings.remove(grounding)

        # Regenerate data-structures as the problem may have changed
        self.problem.compute_static_preds()
        self.problem.link_groundings()
        self.problem.make_flat_preconditions()
        self.problem.make_flat_effects()
        self.problem.get_encode_conds()
        self.problem.make_cond_and_cond_eff_lists()
        self.problem.link_conditions_to_actions()
        self.problem.make_strips_conditions()
        self.problem.compute_conflict_mutex()

        for ag_pair in noops:
            del action_mutexes[ag_pair]
        for ag_pair1 in action_mutexes:
            m_set = action_mutexes[ag_pair1]
            new_m_set = set()
            for ag_pair2 in m_set:
                if not ag_pair2[0].is_noop:
                    new_m_set.add(ag_pair2)
            action_mutexes[ag_pair1] = new_m_set

        # Save the learned info in the problem
        self.problem.state_mutexes = {}
        for s, mutexes in enumerate(output_state_mutexes):
            step = s + 1
            self.problem.state_mutexes[step] = []
            for mutex in mutexes:
                fluent1 = mutex[0][:2]
                fluent2 = mutex[1][:2]
                if fluent1 in invalid_fluents or fluent2 in invalid_fluents or\
                        fluent1 in static_fluents or fluent2 in static_fluents:
                    continue
                self.problem.state_mutexes[step].append((mutex[0], mutex[1]))

        self.problem.first_layer_actions = first_layer_actions

        print()
        return True
