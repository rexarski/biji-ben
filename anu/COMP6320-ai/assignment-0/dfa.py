""" File name:   dfa.py
    Author:      Rui Qiu
    Date:        23 Feb, 2018
    Description: This file defines a function which reads in
                 a DFA described in a file and builds an appropriate data
                 structure.

                 There is also another function which takes this DFA and a word
                 and returns if the word is accepted by the DFA.

                 It should be implemented for Exercise 3 of Assignment 0.

                 See the assignment notes for a description of its contents.
"""


def load_dfa(path_to_dfa_file):
    """ Read a text file and return a list, which contains all the information
        we need about a DFA. Specifically, we have:

        - A list of starting states, though usually there is only one starting
            state within such list.
        - A list of accepting states, stored within a tuple with the starting
            state.
        - A dictionary storing all the transitions from one state to another.
            For each Key-Value pair:
            - The key is a state,
            - The value is a sub-dictionary,
                where the key is a letter (str), the value is a another state
                this previous state mapped to.

        e.g. (['state0'], ['state4', 'state7', 'state10', 'state13']),
                {'state0': {'s': 'state1'},
                'state1': {'a': 'state5', 'i': 'state2', 'o': 'state8',
                    'u': 'state11'},
                'state11': {'n': 'state12'},
                'state12': {'g': 'state13'},
                'state2': {'n': 'state3'},
                'state3': {'g': 'state4'},
                'state5': {'n': 'state6'},
                'state6': {'g': 'state7'},
                'state8': {'n': 'state9'},
                'state9': {'g': 'state10'}}]

        (str) -> Object

    :param path_to_dfa_file: The string formatted path to a DFA file.
    :return: A list containing all information about a DFA.
    """

    transtates = {}  # transitional states are stored within a dictionary.
    start = []
    accept = []
    with open(path_to_dfa_file) as dfa_path:
        for line in dfa_path:
            if line.startswith('initial '):
                start = line.split()[1:]
            elif line.startswith('accepting '):
                accept = line.split()[1:]
            elif line.startswith('transition '):
                aline = line.split()[1:]
                if aline[0] not in transtates.keys():
                    transtates[aline[0]] = {aline[2]: aline[1]}
                else:
                    transtates[aline[0]][aline[2]] = aline[1]
    return [(start, accept), transtates]


def accepts_word(dfa, word):
    """ This function takes in a DFA (that is produced by your load_dfa
        function) and then returns True if the DFA accepts the given word,
        and False otherwise.

        (Object, str) -> bool

    :param dfa: The list returned from the function load_dfa().
    :param word: A string of word.
    :return: Boolean.
    """

    initial = dfa[0][0]  # A list of strings. (Usually only one string.)
    current = initial[0]  # Current state, or the true STARTING STATE.
    accepting = dfa[0][1]  # A list of strings.
    transitions = dfa[1]  # A dictionary of dictionaries.

    for c in word:
        try:
            if c in transitions[current].keys():
                current = transitions[current][c]  # to a new state
            else:
                return False
        # Suppose we were previously mapped to a state never appeared as
        # a key in the dictionary, a KeyError might be generated.
        except KeyError:
            return False
    return current in accepting
