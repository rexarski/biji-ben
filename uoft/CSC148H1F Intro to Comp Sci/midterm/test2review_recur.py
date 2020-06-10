# Recursive LinkedListRec class

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
        if self.is_empty():
            return False
        elif self.first == item:
            return True
        else:
            return self.rest.__contains__(item)
    
    # the recursive guarantee says that if:
    # 1. you've correctly identified all the base cases, and are handling them correctly, and
    # 2. you've done the correct recursive thinking and have translated that thinking into code, then your function is correct, no call stack required.
    # so, how to approach solving problems recursively:
    # identify your bases and handle them,
    # identify the recursive structure problem and write code to reflect it
    
    # the converse guarantee:
    # if code not working, it can only be because you've missed a base case, you're handling a base case incorrectly, or your recursive thinking/implementation is incorrect
    
    
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
        
        if index > len(self):
            raise IndexError
        elif index == 0:
            self.insert_first(item)
        else:
            self.rest.insert(index - 1, item)

    def insert_first(self, item):
        """ (LinkedListRec, object) -> NoneType

        Insert item at the front of the list.
        Note that this should work even if the list
        is empty!
        """
        temp = LinkedListRec([])
        temp.first = self.first
        temp.rest = self.rest
        self.first = item
        self.rest = temp        
            
    def map_f(linked_list, f):
        """ (LinkedListRec, function) -> LinkedListRec
    
        Return a new recursive linked list whose items
        are obtained by applying f to the items in linked_list.
    
        Your implementation should access the attributes
        of the LinkedListRec class directly, and may not use
        any LinkedListRec methods other than the constructor
        and is_empty.
        """
        new_list = LinkedListRec([])
        if linked_list.is_empty():
            return linked_list
        else:
            new_list.first = f(linked_list.first)
            new_list.rest = map_f(linked_list.rest, f)
            return new_list

def rreverse(s):
    """ (String) -> String
    Return a string with reverse order.
    """
    if s == '' or len(s) == 1:
        return s
    else:
        return rreverse(s[1:]) + s[0]

def count_length(lst):
    # this is a helper function to return the number length of a list of lists
    count = 0
    for i in lst:
        count += 1
    return count

def all_subsets(lst):
    """ (list) -> list of lists
    Return a list of all the subsets of given list.
    lst should not contain any repeated items.
    """
    
    # the subsets of [1, 2, 3] should be:
    # []
    # [1], [2], [3]
    # [1, 2], [2, 3], [1, 3]
    # [1, 2, 3]
    
    # and these can be subdivided into 2 groups: those with 1 in it and those without 1 in it,
    # Group1 -> [], [2], [3], [2, 3]
    # Group2 -> [1], [1, 2], [1, 3], [1, 2, 3]
    
    # recursively, we can divide Group1 into 2 parts: WITH and WITHOUT 2 in them.
    # so before that, we have [], [3] and another group is [2], [2, 3]
    # and long before that, we only have [], [3]
    
    # NOTE: the length of list of lists could not be ZERO!
    
    if count_length(lst) == 0:
        return [[]]
    else:
        result = []
        for subset in all_subsets(lst[1:]):
            result += [subset]
            result += [[lst[0]] + subset]
        return result