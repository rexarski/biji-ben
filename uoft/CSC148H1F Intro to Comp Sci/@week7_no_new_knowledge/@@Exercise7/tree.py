# Tree class
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
# Rui Qiu, qiurui2
# ---------------------------------------------
"""Tree class.

This is the recursive implementation of a tree data structure
from Week 7 of the course.

Note the relationship between this class and LinkedListRec;
the only major difference is that self.rest has been replaced
by self.subtrees to handle multiple recursive subparts.

This contains all of the linked list methods from the week:
lecture material, labs, and the exercise.
"""


class EmptyValue:
    """As with linked lists, we'll use this class
    as a dummy class to signify the root of an empty tree.
    """
    pass


class Tree:
    """A recursive tree data structure.

    Attributes:
    - root (object): the item stored at the root of the tree,
                     or EmptyValue if the tree is empty.
    - subtrees (list of Tree): a list of all subtrees of the tree
    """

    def __init__(self, root=EmptyValue):
        """ (Tree, object) -> NoneType

        Create a new tree with given root value.
        If no root value is passed in, the tree is empty
        (this is signified by setting the root value to EmptyValue).
        A new tree always has no subtrees.
        """
        self.root = root
        self.subtrees = []

    def is_empty(self):
        """ (Tree) -> bool
        Return True if self is empty.
        """
        return self.root is EmptyValue

    def add_subtrees(self, new_trees):
        """ (Tree, list of Tree) -> NoneType
        Add the trees in new_tree as subtrees of this tree.
        """
        self.subtrees = self.subtrees + new_trees

    def size(self):
        """ (Tree) -> int
        Return the number of nodes contained in this tree.
        """
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self.subtrees:
                size += subtree.size()
            return size

    def print_tree(self):
        """ (Tree) -> NoneType

        Print all of the items in this tree,
        where the root is printed before all of its subtrees.
        """
        if not self.is_empty():
            # This prints the root item before all of the subtrees.
            print(self.root)
            for subtree in self.subtrees:
                subtree.print_tree()

        # Or alternately, simply call
        # self.print_tree_indent()

    def print_tree_indent(self, depth=0):
        """ (Tree) -> NoneType

        Print all of the items in this tree,
        where the root is printed before all of its subtrees,
        and every value is indented to show its depth.
        """
        if not self.is_empty():
            print(depth * '  ' + self.root)
            for subtree in self.subtrees:
                subtree.print_tree(depth + 1)

    # Mutating methods

    def delete_item(self, item):
        """ (Tree, object) -> bool
        Delete *one* occurrence of item from this tree.
        Return True if item was deleted, and False otherwise.
        """
        if self.is_empty():
            return False
        else:
            if self.root == item:
                self.delete_root()
                return True
            else:
                for subtree in self.subtrees:
                    # Try to delete item from current subtree
                    # If it works, return!
                    if delete_item(subtree):
                        return True
                return False

    def delete_root(self):
        """ (Tree) -> NoneType
        Remove the root item of this tree.
        """
        if self.subtrees == []:
            # Base case when empty or just one node
            self.root = EmptyValue
        else:
            # Note: this removes a whole subtree from
            # self.subtrees!
            temp = self.subtrees.pop()
            self.root = temp.root
            self.subtrees = self.subtrees + temp.subtrees

    # ------- Lab 7 methods -------
    def __contains__(self, item):
        """ (Tree, object) -> bool
        Return True if item is in this tree.
        """
        pass

    def get_branching_factor(self):
        """ (Tree) -> int
        Return the average branching factor of this tree.
        Return 0 if this tree is empty.

        As per the hint from the lab handout, you'll want to do
        most of your work in a recursive helper function.
        """
        pass



    # The following line of code imports the module random
    import random
    # Use the function randint as follows:
    # >>> random.randint(1, 3)
    # 2  # Returns a random number between 1 and 3

    def insert(self, item):
        """ (Tree, object) -> NoneType
        Insert item into this tree using the algorithm from the lab handout.
        """
        pass

    # ------- Exercise 7 -------

    def __eq__(self, other):
        """ (Tree, Tree) -> bool

        Return True if this tree and the other tree are equal trees.
        """
        #if self.subtrees == other.subtrees:
            #if self.subtrees == []:
                #return True
            #else:
                #return self.subtrees.__eq__(other.subtrees)
        #else:
            #return False

        if self.root == other.root:
            if self.root == EmptyValue:
                return True
            elif len(self.subtrees) != len(other.subtrees):
                return False
            else:
                return self.subtrees.__eq__(other.subtrees)
        else:
            return False