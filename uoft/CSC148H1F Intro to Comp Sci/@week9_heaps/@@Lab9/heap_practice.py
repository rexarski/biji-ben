# Heap class
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
"""Heap class.

This is the implementation of a heap data structure
from Week 9 of the course.

Note that this is not a recursive implementation:
there are no "left" and "right" attributes, even though
a heap is conceptually a binary tree.

This contains all of the Heap methods from the week:
lecture material, labs, and the exercise.
"""

class Heap:
    """Heap class.

    Attributes:
    - items (list): list of items contained in the heap, with an extra None
                    at the beginning, to make the index operations smoother.
    """

    def __init__(self):
        """ (Heap) -> NoneType
        Create an empty heap. The None pads the list to
        start indexing items at 1 instead of 0.
        """
        self.items = [None]

    def is_empty(self):
        """ (Heap) -> bool
        Return True if this heap is empty.
        """
        return self.items == [None]

    def get_max(self):
        """ (Heap) -> object

        Return the largest item stored in this heap.
        Raise IndexError if this heap is empty.
        """
        if self.is_empty():
            raise IndexError
        else:
            return self.items[1]

    # Mutating methods

    def extract_max(self):
        """ (Heap) -> object
        Return and remove the largest item stored in this heap.
        Raise IndexError if this heap is empty.
        """

        if self.is_empty():
            raise IndexError
        elif len(self.items) == 2:
            # It was correctly pointed out a few times that our strategy
            # of replacing the root item with the last leaf doesn't work
            # if there's only one leaf. So we handle that case separately!
            return self.items.pop()
        else:
            largest = self.items[1]
            last = self.items.pop()
            self.items[1] = last

            # Restore heap property
            self.bubble_down(1)

            return largest

    def bubble_down(self, index):
        """ (Heap, int) -> NoneType

        Restore heap property for the tree rooted at index.
        Note that when this is called, only the item
        at position index might not satisfy the heap property;
        all other nodes in the tree already do.
        """

        item = self.items[index]
        left = index * 2
        right = index * 2 + 1

        if left >= len(self.items):
            # What did we need to do here?
            pass
        elif right >= len(self.items):
            # What about here?
            if left < len(self.items):
                if self.items[left] > self.items[index]:
                    self.swap(left, index)
                    self.bubble_down(left)
        else:
            left_item = self.items[left]
            right_item = self.items[right]
            
            if item < left_item < right_item:
                # Go down right side
                self.swap(index, right)
                self.bubble_down(right)
                
            elif item < right_item <= left_item:
                # Go down left side
                self.swap(index, left)
                self.bubble_down(left)
            # Fill in other conditions!

    def swap(self, i, j):
        """ (Heap, int, int) -> NoneType
        Swap items as positions i and j in this heap.
        """
        # Note the use of simultaneous assignment here;
        # this is the "Pythonic" way of swapping variables
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def insert(self, item):
        """ (Heap, object) -> NoneType
        Insert item into this heap, preserving the heap property.
        """
        # Add item as new leaf
        self.items.append(item)
        # Restore heap property
        self.bubble_up(len(self.items) - 1)

    def bubble_up(self, index):
        """ (Heap, int) -> NoneType
        Move the item at position index up to its proper spot in the heap.

        Note: the only nodes where the heap property might fail to hold are
        the ancestors of index.
        """
        if index == 1:
            # The current node is the root, so it has no ancestors
            # This means the heap property must be satisfied
            pass
        else:
            parent = index // 2
            if self.items[parent] < self.items[index]:
                # Swap or stop?
                self.swap(parent, index)
                self.bubble_up(parent)
            else:
                # Swap or stop?
                pass

