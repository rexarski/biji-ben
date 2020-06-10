# LinkedListRec class
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
"""LinkedListRec class.

This is the recursive implementation of a linked list
for Week 5 of the course.
Note the structural differences between this implementation
and the node-based implementation of Week 4. Even though
both classes have the same public interface, how they
implement their methods are quite different!

This contains all of the linked list methods from the week:
lecture material, labs, and the exercise.
"""


class EmptyValue:
    """Dummy class representing the "first" item
    of an empty list.

    This is created so that we can make linked lists
    that contain None.
    """
    pass


class LinkedListRec:
    """Linked List with a recursive implementation.
    Note that there is no "Node" class with this implementation.

    Attributes:
    - first (object): the first item stored in this list,
                      or EmptyValue if this list is empty
    - rest (LinkedListRec): a list containing the other items
                            in this list, or None if this list is empty
    """

    def __init__(self, items):
        """ (LinkedListRec, list) -> NoneType

        Create a new linked list containing the elements in items.
        If items is empty, self.first initialized to EmptyValue.
        """
        if len(items) == 0:
            self.first = EmptyValue
            self.rest = None
        else:
            self.first = items[0]
            self.rest = LinkedListRec(items[1:])

    # Non-mutating methods
    def is_empty(self):
        """ (LinkedListRec) -> bool
        Return True if this list is empty.
        """
        return self.first is EmptyValue

    def __len__(self):
        """ (LinkedListRec) -> int
        Return the number of items stored in this list.
        """
        if self.is_empty():
            return 0
        else:
            return 1 + self.rest.__len__()

    def __getitem__(self, index):
        """ (LinkedListRec, int) -> object

        Return the item at position index in this list.
        Raise IndexError if index is >= the length of this list.
        """
        if self.is_empty():
            raise IndexError
        elif index == 0:
            return self.first
        else:
            return self.rest.__getitem__(index - 1)
            # Or equivalently, self.rest[index - 1]

    def __contains__(self, item):
        """ (LinkedListRec, object) -> bool
        Return True if item is contained in this list.
        """
        pass

    # Mutating methods
    def remove(self, index):
        """ (LinkedListRec, int) -> NoneType

        Remove item at position index from self.
        Raise an IndexError if index is out of bounds.
        """
        if self.is_empty():
            raise IndexError
        elif index == 0:
            self.remove_first()
        else:
            self.rest.remove(index - 1)

    def remove_first(self):
        """ (LinkedListRec) -> NoneType

        Remove the first item in self.
        Raise an IndexError if self is empty.
        """
        if self.is_empty():
            raise IndexError
        else:
            self.first = self.rest.first
            self.rest = self.rest.rest

    def insert(self, index, item):
        """ (LinkedListRec, int, object) -> NoneType

        Insert item at position index in this list.
        Raise an IndexError if index > len(self).
        But note that it is possible to insert an item
        at the *end* of a list (when index == len(self)).
        """
        # Hint: take a look at remove and think about
        # what the base cases and recursive steps are.
        pass

    def insert_first(self, item):
        """ (LinkedListRec, object) -> NoneType

        Insert item at the front of the list.
        Note that this should work even if the list
        is empty!
        """
        pass
