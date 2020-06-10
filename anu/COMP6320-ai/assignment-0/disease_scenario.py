""" File name:   disease_scenario.py
    Author:      Rui Qiu
    Date:        28 Feb, 2018
    Description: This file represents a scenario simulating the spread of an
                 infectious disease around Australia. It should be
                 implemented for Part 1 of Exercise 4 of Assignment 0.

                 See the lab notes for a description of its contents.
"""


class DiseaseScenario:
    """ A static disease spreading scenario."""

    def __init__(self):
        """ Initialize the object as a DiseaseScenario."""

        self.threshold = float(0)
        self.growth = float(0)
        self.spread = float(0)
        self.location = ''
        # Note: Though called 'location', it in fact stores the starting
        # location of the Health Agent.
        self.locations = []
        self.disease = {}
        self.conn = {}

    def read_scenario_file(self, path_to_scenario_file):
        """  Read the text file storing a scenario.

        (DiseaseScenario, str) -> bool

        :param path_to_scenario_file: A string indicating the path to a
        scenario file.
        :return: Boolean, indicating if the reading of a scenario file is
        successful.
        """
        try:
            with open(path_to_scenario_file) as f:
                for line in f:
                    if line.startswith('threshold '):
                        self.threshold = float(line.split()[-1])
                    elif line.startswith('growth '):
                        self.growth = float(line.split()[-1])
                    elif line.startswith('spread '):
                        self.spread = float(line.split()[-1])
                    elif line.startswith('start '):
                        self.location = str(line.split()[-1])
                    elif line.startswith('location '):
                        self.locations.append(str(line.split()[-1]))
                    elif line.startswith('disease '):
                        self.disease[line.split()[1]] = float(line.split()[2])
                    elif line.startswith('conn '):
                        [loc1, loc2] = line.split()[1:]
                        if loc1 in self.conn.keys():
                            self.conn[loc1].add(loc2)
                        else:
                            self.conn[loc1] = {loc2}
                        # a connection is two-way
                        if loc2 in self.conn.keys():
                            self.conn[loc2].add(loc1)
                        else:
                            self.conn[loc2] = {loc1}

                    # If disease of a location did not appear in the file,
                    # by default, it is set to 0.
                    target = [item for item in self.locations
                              if item not in self.disease.keys()]
                    for t in target:
                        self.disease[t] = float(0)
        except IOError:
            return False
        else:
            return True

    def valid_moves(self):
        """  Return a list of valid moves.

        (DiseaseScenario) -> [str]

        :return: A list strings, indicating the valid moves of the Agent based
        on his/her current location.
        """
        destinations = list(self.conn[self.location])
        destinations.append(self.location)
        return destinations

    def move(self, loc):
        """ Move the Agent to a new location.

        (DiseaseScenario, str) -> None

        :param loc: A string indicating the new location that Agent
        is moved to.
        :return: None.
        :raises ValueError: Raises an exception if loc is not a valid move.
        """
        if loc in self.valid_moves():
            self.location = loc
            self.disease[loc] = float(0)
        else:
            raise ValueError

    def spread_disease(self):
        """ Simulate the spread of this disease.

        (DiseaseScenario) -> None

        1. For each location, the disease value is increased by the growth.
        2. For each location, if one of its neighbouring location exceeds the
        threshold, a portion of increase in disease value is contributed by
        this neighbour.
        3. Repeat step 2 for all its neighbours.
        4. But if an Agent exists in this location, the disease value will
        always be zero.

        Note: All the growth and spread are calculated based on current disease
        values.
        """

        new_disease = self.disease.copy()
        for city in self.locations:
            internal = self.disease[city] * self.growth
            external = float(0)
            for neighbour in list(self.conn[city]):
                if self.disease[neighbour] >= self.threshold:
                    external += self.disease[neighbour] * self.spread
            if self.location != city:
                new_disease[city] = self.disease[city] + internal + external
            else:
                new_disease[city] = float(0)
        self.disease = new_disease
