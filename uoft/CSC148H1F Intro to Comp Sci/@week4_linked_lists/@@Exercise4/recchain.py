# Exercise 4: Recursive PeopleChain
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
#
# ---------------------------------------------
"""Recursive PeopleChain implementation.

This is an alternate implementation of the PeopleChain class
from Exercise 3.
The major difference is that there is no more Person class;
links are stored between PeopleChain objects, rather than Person objects.

Thus most methods now use the following approach:
- do something with the leader of the chain
- do something with the rest of the chain
  (which is another) PeopleChain objects
"""


class PeopleChain:
    """A chain of people, recursive style.

    Attributes:
    - leader (str): the name of the leader of a chain, or None if the chain
                    is empty.
    - rest (PeopleChain): an object representing all other people in the chain
    """
    def __init__(self, names):
        """ (PeopleChain, list of str) -> NoneType

        Create a chain of people in the order provided in names.
        Set the leader of the chain as the first person in names.
        """

        self.names = names
        if len(names) == 0:
            # No leader, and an empty chain!
            self.leader = None
            self.rest = None
        else:
            # The leader attribute now just stores the name of a person
            # Note: no Person class
            self.leader = names[0]
            # The rest of the chain is another chain with the other names
            self.rest = PeopleChain(names[1:])

    def get_leader(self):
        """ (PeopleChain) -> str

        Return the name of the leader of the chain.
        You may assume there is at least one person in the chain.
        """
        
        return self.leader

    def get_second(self):
        """ (PeopleChain) -> str

        Return the name of the second person in the chain,
        i.e., the one the leader is holding onto.
        You may assume the chain has at least two people.
        """
        # Hint: the second person in the chain is the
        # leader of the rest of the chain.
        return self.rest.leader

    def get_third(self):
        """ (PeopleChain) -> str

        Return the name of the third person in the chain.
        You may assume the chain has at least three people.
        """
        # Hint: the third person in the chain is the...
        return self.rest.rest.leader

    def get_nth(self, n):
        """ (PeopleChain) -> str

        Return the name of the nth person in the chain.
        You may assume the chain has at least n people.

        *** DO NOT USE ANY LOOPS!! ***
        """
        # Hint: the nth persion in the chain is the leader of the people chain starting from nth person (to the end)
        
        x = self.names[n-1:]
        return x[0]