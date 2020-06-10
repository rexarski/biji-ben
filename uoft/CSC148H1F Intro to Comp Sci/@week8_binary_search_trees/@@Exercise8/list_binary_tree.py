# ListBinaryTree class
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


class ListBinaryTree:
    def __init__(self, items):
        """ (ListBinaryTree, list) -> NoneType

        Create a complete binary tree in list form
        with the specified items.

        The [None] is used to start indexing items at 1
        instead of 0, which is easier.
        """

        self.items = [None] + items

    def is_empty(self):
        """ (ListBinaryTree) -> bool

        Return True if self is empty.
        """
        return len(self.items) == 1

    def root(self):
        """ (ListBinaryTree) -> object

        Return the root item of the tree.
        If the tree is empty, raise IndexError.
        """

        if self.is_empty():
            raise IndexError
        else:
            return self.items[1]

    def go_down_greedy(self, index=1):
        """ (ListBinaryTree) -> list

        Return a list of items starting at the node with position index
        and ending at a leaf, where at each level the child node
        with the smaller value is chosen to recurse on
        (in case of ties, choose the left child).

        By default, the list starts at the root of the tree.

        Note: you may use either the provided subtree methods,
        or do the index arithmetic yourself.
        For maximum learning, try both!
        """
        
        if self.is_empty():
            return []
        else:
            if index == None:
                i = 1
            else:
                i = index
            lst = [self.items[i]]
            while i <= len(self.items):
                if left(i) > len(self.items) - 1:
                    return lst
                elif left(i) <= len(self.items) - 1 < right(i):
                    lst.append(self.items[left(i)])
                    return lst
                elif right(i) <= len(self.items) - 1:
                    if self.items[left(i)] <= self.items[right(i)]:
                        lst.append(self.items[left(i)])
                        i = left(i)
                    else:
                        lst.append(self.items[right(i)])
                        i = right(i)
            return lst

# Index helper functions
def left(index):
    """ (int) -> int

    Return the index of the left child of the node as position index.
    """
    return 2 * index

def right(index):
    """ (int) -> int

    Return the index of the right child of the node as position index.
    """
    return 2 * index + 1
