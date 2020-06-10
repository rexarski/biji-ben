# Tree class
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
#  Antong Wu    wuantong
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

# The following line of code imports the module random
import random


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
            print(depth * '  ' + str(self.root))
            for subtree in self.subtrees:
                subtree.print_tree_indent(depth + 1)

    # Mutating methods
    def delete_root(self):
        """ (Tree) -> NoneType
        Remove the root item of this tree.
        """
        if len(self.subtrees) == 0:
            # Base case when empty or just one node
            self.root = EmptyValue
        else:
            # Note: this removes a whole subtree from
            # self.subtrees!
            temp = self.subtrees.pop()
            self.root = temp.root
            self.subtrees = self.subtrees + temp.subtrees

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
                    if subtree.delete_item(item):
                        # If the subtree is now empty, remove it!
                        if subtree.is_empty():
                            self.subtrees.remove(subtree)
                        return True
                return False

    # ------- Lab 7 methods -------
    def __contains__(self, item):
        """ (Tree, object) -> bool
        Return True if item is in this tree.
        """
        if self.is_empty():
            return False
        else:
            if self.root == item:
                return True
            else:
                for subtree in self.subtrees:
                    if subtree.__contains__(item):
                        return True
                return False
                        

    def get_branching_factor(self):
        """ (Tree) -> int
        Return the average branching factor of this tree.
        Remember to ignore all 0's coming from leaves in
        this calculation.
        Return 0 if this tree is empty or consists of just
        a single root node.
        """
        table = self.get_branching_factor_helper()
        x = table[0]
        y = table[1]
        if y is 0:
            return 0
        return y/x

    def get_branching_factor_helper(self):
        """ (Tree) -> (int, int)
        Return a tuple (x,y) where
        x is the total branching factor of all non-leaf nodes in this tree, and
        y is the total number of non-leaf nodes in this tree.
        """
        if self.is_empty():
            return (0, 0)
        else:
            x = 0
            y = 0
            if len(self.subtrees) is not 0:
                x = x + 1
                y = y + len(self.subtrees)
            for subtree in self.subtrees:
                table=subtree.get_branching_factor_helper()
                x+=table[0]
                y+=table[1]
            return (x,y)
                


    # Lab Task 2 - Insertion
    # Use the function randint as follows:
    # >>> random.randint(1, 3)
    # 2  # Returns a random number between 1 and 3

    def insert(self, item):
        """ (Tree, object) -> NoneType
        Insert item into this tree using the algorithm from the lab handout.
        """
        if self.is_empty():
            self.root = item
        elif len(self.subtrees) is 0:
            self.subtrees.append(Tree(item))
        else:
            x = random.randint(1, 3)
            if x is 3:
                self.subtrees.append(Tree(item))
            else:
                random.choice(self.subtrees).insert(item)

    # ------- Exercise 7 -------

    def __eq__(self, other):
        """ (Tree, Tree) -> bool

        Return True if this tree and the other tree are equal trees.
        """
        if self.is_empty():
            return other.is_empty()
        else:
            if self.root == other.root:
                return self.subtrees == other.subtrees
                
