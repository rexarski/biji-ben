# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez, Nathan Robinson, Enrico Scala (
# {enrico.scala,miquel.ramirez}@gmail.com)

""" Student Details

    Student Name: Rui Qiu
    Student ID: u6139152
    Email: u6139152@anu.edu.au
    Date: 2018-05-19
"""

"""
    In this file you will implement some constraints which represent
    domain-specific control knowledge for the Logistics domain
    (benchmarks/logistics).

    These constraints will be used in addition to a standard flat encoding of
    the Logistics problem instances, without plan graph mutexes (which you are
    assumed to have completed while going through Exercises 1-6).

    Those constraints should make solving the problem easier. This may be at
    the cost of optimality. That is, your additional constraints may rule out
    some solutions to make planning easier -- for example, by restricting the
    way trucks and planes can move -- but they should preserve SOME solution
    (the problems might be very easy to solve if you added a contradiction, but
    wholly uninteresting!).

    Often control knowledge for planning problems is based on LTL (Linear
    Temporal Logic - https://en.wikipedia.org/wiki/Linear_temporal_logic) and
    you might get inspired by studying this.

    We do not expect you to implement an automatic compilation of arbitrary LTL
    into SAT, just some control knowledge rules for problems from the Logistics
    domain.

    As an example rule to get you started, you could assert that if a package
    was at its destination, then it cannot leave.

    That is you could iterate over the goal of the problem to find the
    propositions which talk about where the packages should end up and make
    some constraints asserting that if one of the corresponding fluents is true
    at step t then it must still be true at step t + 1

    You will be marked based on the correctness, inventiveness, and
    effectiveness of the control knowledge you devise.

    You should aim to make at least three different control rules. Feel free to
    leave (but comment out) rules which you abandon if you think they are
    interesting and want us to look at them.

    Use the flag "-e logistics" to select this encoding and the flag "-p false"
    to disable the plangraph mutexes.
"""

from strips_problem import Action, Proposition

from .basic import BasicEncoding
import re

encoding_class = 'LogisticsEncoding'


class LogisticsEncoding(BasicEncoding):
    """ An encoding which extends BasicEncoding but adds control knowledge
        specific for the Logistics domain.
    """

###############################################################################
#                You need to implement the following methods                  #
###############################################################################

    def make_control_knowledge_variables(self, horizon):
        """ Make the variable for the problem.

            Use the function self.new_cnf_code(step, name, object) to make
            whatever codes for CNF variables you need to make your control
            knowledge for the Logistics problem.

            You can make variables which mean anything if you can think of
            constraints to make that enforce that meaning. As an example, if
            you were making control logic for the miconics domain, you might
            make variables which keep track if each passenger has ever
            been in an elevator and is now not.

            For a passenger p, and t > 0:
                was_boarded(p)@t <->
                    (-boarded(p)@t ^ (boarded(p)@t-1 v was_boarded(p)@t-1))

            You can then use these variables, along with the fluent and action
            variables to make your control knowledge.

            (LogisticsEncoding, int) -> None
        """
        # You might want to save your variables here, or feel free to make as
        # many data structures as you need to keep track of them.

        self.control_fluent_codes = {}

        """ *** YOUR CODE HERE *** """

        # DID NOT DEFINE ANY EXTRA VARIABLES, ALL DONE IN THE METHOD BELOW

    def make_control_knowledge(self, horizon):
        """ This is where you should make your control knowledge clauses.

            These clauses should have the type "control".

            (LogisticsEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # ADD_RULE1_COUNT = 0
        # ADD_RULE2_COUNT = 0
        # ADD_RULE3_COUNT = 0

        close = list()
        far = list()

        for g in self.problem.goal:
            for p in self.problem.propositions:
                if re.match(r'at\spackage\d+\scity\d+-\d+', str(p)):
                    p_split = str(p).split()
                    g_split = str(g).split()

                    # if "at" and "package[oo]" match
                    if p_split[0] == g_split[0] and p_split[1] == g_split[1]:
                        # also "city[oo]-[xx]" match
                        if p_split[2][:-2] == g_split[2][:-2]:
                            close.append(p)
                        else:
                            far.append(p)

        # Rule 1:
        # ===============================
        # If a package is at its goal location, then it must remain there.
        # p@t and goal@t) -> p@t+1), where p is at(package, location)
        # cnf: not p@t or not goal@t or p@t+1

        for g in self.problem.goal:
            for t in range(0, horizon):
                clause = list()
                clause.append(-self.proposition_fluent_codes[(g, t)])
                clause.append(self.proposition_fluent_codes[(g, t + 1)])
                self.add_clause(clause, "control")
                # ADD_RULE1_COUNT += 1

        for t in range(0, horizon):
            for a in self.problem.actions:

                # Rule 2
                # ===============================

                # RULE
                # close -> do not load airplane
                # p1: close@t
                # p2: at the location of an airport @t
                # p3: airplane at this location @t
                # p4: plane is not loaded
                # a: load this airplane
                #
                # p1@t and p2@t and p3@t and p4@t => a@t
                # not p1@t or not p2@t or not p3@t or not p4@t or a@t
                # cnf: not p@t or not a@t
                if str(a).startswith('load-airplane'):
                    for i in close:
                        package = str(i).split()[1]
                        if str(a).split()[1] == package:
                            clause = list()
                            clause.append(
                                -self.proposition_fluent_codes[(i, t)])
                            clause.append(-self.action_fluent_codes[(a, t)])
                            self.add_clause(clause, "control")
                            # ADD_RULE2_COUNT += 1

                # Rule 3
                # ===============================

                # RULE
                # far -> do not unload airplane
                # p@t -> not a@t, where p is far, a is unload-airplane
                # cnf: not p@t or not a@t
                if str(a).startswith('unload-airplane'):
                    for j in far:
                        package = str(j).split()[1]
                        if str(a).split()[1] == package:
                            clause = list()
                            clause.append(
                                -self.proposition_fluent_codes[(j, t)])
                            clause.append(-self.action_fluent_codes[(a, t)])
                            self.add_clause(clause, "control")
                            # ADD_RULE3_COUNT += 1

                # # RULE
                # # if an airplane has a package on it and the package's
                # # destination is close do not fly this airplane.
                # # in fact, if the destination of package is far,
                # # fly this plane to it.
                # #
                # # p1: package on airplane @ t
                # # p2: package at a place @ t
                # # p3: the place and the goal are in the same city
                # # rule: p1@t and p2@t and p@3 => not fly plane@t
                # # and unload the plane@t
                #
                # # not p1@t or not p2@t or not fly@t
                # # not p1@t or not p2@t or unload
                #
                # # rule: p1@t and p2@t and not p3@t => fly plane@t and not
                # # unload the plane@t
                #
                # if str(a).startswith('fly-airplane'):
                #     plane = str(a).split()[1]
                #     # loc_from = str(a).split()[2]
                #     for p1 in self.problem.propositions:
                #         if str(p1).startswith('in package') and str(p1).split()[2] == plane:  # in package plane
                #             package = str(p1).split()[1]
                #             for p2 in self.problem.propositions:
                #                 if p2 in close and str(p2).split()[1] == package:  # at package location
                #                     clause = list()
                #                     clause.append(-self.proposition_fluent_codes[p1, t])
                #                     clause.append(-self.proposition_fluent_codes[p2, t])
                #                     clause.append(-self.action_fluent_codes[a, t])
                #                     self.add_clause(clause, 'control')
                #                     ADD_RULE2_COUNT += 1
                #
                #
                #                     for g in self.problem.goal:
                #                         if str(g).split()[1] == package:
                #                             destination = str(g).split()[2]
                #                             for do in self.problem.actions:
                #                                 # unload-airplane package00 plane00 city00-00
                #                                 if str(do).startswith('unload') and str(do).split()[1] == package and str(do).split()[2] == plane and str(do).split()[3] == destination:
                #                                     clause2 = list()
                #                                     clause2.append(-
                #                                                    self.proposition_fluent_codes[
                #                                                        p1, t])
                #                                     clause2.append(-
                #                                                    self.proposition_fluent_codes[
                #                                                        p2, t])
                #                                     clause2.append(
                #                                         self.action_fluent_codes[
                #                                             do, t])
                #                                     self.add_clause(clause2,
                #                                                     'control')
                #
                #                                     ADD_RULE3_COUNT += 1

                # RULE
                # if there is no package needs to be transferred at a location,
                # and the location has a truck
                # drive the truck to its airport

                # p1: (at package__ city__-__ /\ (it is a goal)@t
                # p2: (at truck__ city__-__)@t
                # p3: (city__-__ is not airport)
                # not p1/\p2/\p3 => drive_truck_to_its_airport@t
                #
                #
                # CNF: p1 V not p2 V not p3 V drive_truck_to_its_airport@t
                # if str(a).startswith('DRIVE-TRUCK'):
                #     for p1 in self.problem.goal:
                #         city = str(p1).split()[2]
                #         for p2 in self.problem.propositions:
                #             if str(p2).startswith('at truck') and str(p2).split()[2] == city:
                #                 for p3 in self.problem.propositions:
                #                     if str(p3).startswith('airport') and str(p3).split()[1] == city:
                #                         clause = list()
                #                         clause.append(self.proposition_fluent_codes[(p1, t)])
                #                         clause.append(-self.proposition_fluent_codes[(p2, t)])
                #                         clause.append(-self.proposition_fluent_codes[(p3, t)])
                #                         clause.append(self.action_fluent_codes[(a, t)])
                #                         self.add_clause(clause, "control")

                # RULE
                # if there is an airplane is loaded with a package need
                # transfer (to another city), fly airplane to the corresponding
                # city.

                # p1: (at airplane__ city__-__)@t
                # p2: (in package__ airplane__)@t
                # p3: ( p2 is in far)
                # p1/\p2/\p3 => fly_airplane_to_its_airport@t
                #
                #
                # CNF: not p1@t V not p2@t V not p3@t V fly_plane_to_airport@t

        # print("ADDED RULE 1:")
        # print(ADD_RULE1_COUNT)
        #
        # print("ADDED RULE 2:")
        # print(ADD_RULE2_COUNT)
        #
        # print("ADDED RULE 3:")
        # print(ADD_RULE3_COUNT)

###############################################################################
#                    Do not change the following method                       #
###############################################################################

    def encode(self, horizon, exec_semantics, plangraph_constraints):
        """ Make an encoding of self.problem for the given horizon.

            For this encoding, we have broken this method up into a number
            of sub-methods that you need to implement.

           (LogisticsEncoding, int, str, str) -> None
        """
        super().encode(horizon, exec_semantics, plangraph_constraints)
        self.make_control_knowledge_variables(horizon)
        self.make_control_knowledge(horizon)
