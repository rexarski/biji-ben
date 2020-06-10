""" File name:   health_agents.py
    Author:      Rui Qiu
    Date:        28 Feb, 2018
    Description: This file contains agents which fight disease. It is used
                 in Exercise 4 of Assignment 0.
"""

import random


class HealthAgent:
    """ A simple disease fighting agent. """

    def __init__(self, locations, conn):
        """ This constructor does nothing except save the locations and conn.
            Feel free to overwrite it when you extend this class if you want
            to do some initial computation.

            (HealthAgent, [str], { str : set([str]) }) -> None
        """
        self.locations = locations
        self.conn = conn

    def choose_move(self, location, valid_moves, disease, threshold,
                    growth, spread):
        """ Using given information, return a valid move from valid_moves.
            Returning an invalid move will cause the system to stop.

            Changing any of the mutable parameters will have no effect
            on the operation of the system.

            This agent will locally move to the highest disease, of there is
            is no nearby disease, it will act randomly.

            (HealthAgent, str, [str], [str], { str : float },
                                                float, float, float) -> str
        """
        max_disease = None
        max_move = None
        for move in valid_moves:
            if max_disease is None or disease[move] > max_disease:
                max_disease = disease[move]
                max_move = move

        if not max_disease:
            return random.choice(valid_moves)

        return max_move


# Make a new agent here called SmartHealthAgent, which extends HealthAgent and
# acts a bit more sensibly. Feel free to add other helper functions if needed.

class SmartHealthAgent(HealthAgent):
    """ A smarter Health Agent comparing with the previous one."""

    def __init__(self, locations, conn):
        """ Inherit from its parent class. """
        super().__init__(locations, conn)

    def choose_move(self, location, valid_moves, disease, threshold, growth,
                    spread):
        """ Choose an efficient move based on current overall situation, in
        order to eradicate the disease completely as quickly as possible.

        (SmartHealthAgent, str, [str], {str: float}, float, float, float)
                                                    -> str

        The general idea can be divided into two basic cases:

        1. If the neighbouring locations have disease, the Agent goes to the
        one with highest disease values.
        (This is exactly the same as previous.)

        2. If the neighbouring locations don't have disease yet, the Agent will
        quickly do a calculation on DISEASE COST and decide which move it
        will take.

        The DISEASE COST is roughly defined as below:

        For each valid move given a current location,

        DISEASE COST = DISEASE@location1 * distance(location1, next_move) *
                        num(neighbours of location1)
                    + DISEASE@location2 * distance(location2, next_move) *
                        num(neighbours of location2)
                    + ...

        In other words, the disease cost is the weighted sum of disease values
        given the assumption that we make a valid move.

        The reason why we use distances as weights is because we know the
        disease of some locations far away might grow beyond control
        if we don't act towards them immediately.

        Similarly, if two locations share the same disease value, the one with
        more neighbours should be paid more attention to since it is more
        likely to spread the disease.

        :param location: A string of location our Agent is currently in.
        :param valid_moves: A list of strings indicating possible moves for
        this Agent.
        :param disease: A dictionary of the disease values of locations.
        :param threshold: A floating number indicating the threshold of such
        disease, determining the spreading condition.
        :param growth: A floating number indicating the increasing rate within
        a location regardless of spreading from its neighbours.
        :param spread: A floating number indicating the rate of the disease
        spreading from one location to another.
        :return: A string of next move, i.e. the next location this Agent is
        going to.
        """

        # If neighbouring locations have disease
        max_disease = None
        max_move = None
        for move in valid_moves:
            if max_disease is None or disease[move] > max_disease:
                max_disease = disease[move]
                max_move = move

        # If no disease around
        if not max_disease:
            max_cost = {}
            optimum_moves = list(valid_moves)
            optimum_moves.remove(location)
            for m in optimum_moves:
                m_cost = 0
                for l in self.locations:
                    if len(self.find_shortest_path(m, l)) >= 1:
                        l_distance = len(self.find_shortest_path(m, l)) - 1
                        # The distance is number of vertices on path minus one.
                    else:
                        l_distance = 0
                    l_disease = disease[l] * (1 + growth)
                    for n in list(self.conn[l]):
                        if disease[n] >= threshold:
                            l_disease += disease[n] * spread
                    # DISEASE COST:
                    m_cost += l_disease * l_distance * len(list(self.conn[l]))
                max_cost[m] = m_cost
            lowest = min(max_cost.values())
            possible_moves = [k for k, v in max_cost.items() if v == lowest]
            # If multiple locations have the same DISEASE COST, just pick one
            max_move = random.choice(possible_moves)
        return max_move

    def find_shortest_path(self, start, end, path=list()):
        """ Find the shortest path between two locations.

        :param start: A string of starting location.
        :param end: A string of ending location.
        :param path: A list of strings of locations, by default it's empty.
        :return: A list of strings of locations.
        """
        path = path + [start]
        if start == end:
            return path
        if start not in self.conn.keys():
            return None  # Isolated location has no path to outside locations.
        shortest = None
        for node in self.conn[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)  # recursive
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
