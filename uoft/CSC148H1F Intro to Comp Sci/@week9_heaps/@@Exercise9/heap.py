# Heap class
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

        index_item = self.items[index]
        left = index * 2
        right = index * 2 + 1

        if right < len(self.items):
            # index node has two children
            left_item = self.items[left]
            right_item = self.items[right]
            if index_item < left_item < right_item:
                self.swap(index, right)
                self.bubble_down(right)
            elif index_item < right_item <= left_item:
                self.swap(index, left)
                self.bubble_down(left)
            elif index_item < left_item:
                self.swap(index, left)
                self.bubble_down(left)
            elif index_item < right_item:
                self.swap(index, right)
                self.bubble_down(right)
        elif left < len(self.items):
            # index node has just the left child
            if self.items[index] < self.items[left]:
                self.swap(index, left)
                self.bubble_down(left)

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
                self.swap(index, parent)
                self.bubble_up(parent)

    # Exercise 9 Part 1

    def is_heap(self, index=1):
        """ (Heap) -> bool
        Return True if the subtree of this heap rooted at
        position index satisfies the heap property.
        """
        if index > len(self.items) - 1:
            raise IndexError
        elif 2 * index > len(self.items) - 1:
            return True
        elif 2 * index <= len(self.items) - 1 and 2 * index + 1 > len(self.items) - 1:
            return self.items[index] >= self.items[2 * index]
        else:
            if self.items [index] < self.items[2 * index] or self.items[index] < self.items[2 * index + 1]:
                return False
            else:
                if self.is_heap(2 * index) == False:
                    return False
                elif self.is_heap(2 * index + 1) == False:
                    return False
                else:
                    return True


# Lab 9
def build_heap_1(lst):
    """ (list) -> Heap

    Build a heap out of the items in lst,
    using Algorithm 1 from the lab handout.
    """
    pass


def build_heap_2(lst):
    """ (list) -> Heap

    Build a heap out of the items in lst,
    using Algorithm 2 from the lab handout.
    """
    pass


# Exercise 9 Part 2

def heapsort(lst):
    """ (list) -> list
    Return a new list containing the items of lst
    sorted in decreasing order.
    Do not modify lst.

    Note: you *must* use heaps, and you may not use any
    sorting algorithms you've learned, or Python's
    sort method.
    """
    heap = Heap()
    if lst == []:
        return lst
    else:
        heap.items = [None]
        for item in lst:
            heap.insert(item)
            for i in range(len(heap.items) - 1, 1, -1):
                if heap.items[i] > heap.items[i - 1]:
                    heap.swap(i, i - 1)
        return heap.items[1:]

def get_first_child_index(length):
    """ With the given length of a list, transformed into a heap, then we return the first index of the youngest generation of children.
    E.g., we have a list [5, 4, 3, 2, 1], then we return the index of 2, which is 4 in the corresponding heap.
    """
    return 2 ** (length // 2)
