# LinkedList class
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
# Rui Qiu, 999292509
# ---------------------------------------------
"""LinkedList class.

This is the node-based implementation of a linked list
for Week 4 of the course.
Note that this class lends itself well to iteration,
but for recursion there is a simpler model.

This contains all of the linked list methods from the week:
lecture material, labs, and the exercise.
"""


class Node:
    """A node in a linked list.

    Attributes:
    - item (object): the data stored in this node
    - next (Node): the next Node in the list, or None if this
                   is the last Node
    """

    def __init__(self, item):
        """ (Node, object) -> NoneType
        Create a new node storing item, pointing to nothing.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.

    Attributes:
    - first (Node): the first node in the list, or
                    None if the list is empty
    """

    def __init__(self, items):
        """ (LinkedList, list) -> NoneType

        Create Node objects linked together in the order provided in items.
        Set the first node of the list as the first item in items.
        """

        if len(items) == 0:  # No items, and an empty list!
            self.first = None
        else:
            self.first = Node(items[0])
            current_node = self.first
            for item in items[1:]:
                current_node.next = Node(item)
                current_node = current_node.next

    # Non-mutating methods: these methods do not change the list
    def is_empty(self):
        """ (LinkedList) -> bool
        Return True if this list is empty.
        """
        return self.first is None

    def __len__(self):
        """ (LinkedList) -> int
        Return the number of elements in this list.
        """
        curr = self.first
        size = 0
        while curr is not None:
            size = size + 1
            curr = curr.next
        return size

    def __getitem__(self, index):
        """ (LinkedList, int) -> object

        Return the item at position index in this list.
        Raise IndexError if index is >= the length of self.
        """
        if len(self) <= index:
            raise IndexError

        curr = self.first
        # Iterate to (index)-th node
        for i in range(index):
            curr = curr.next
        return curr.item

    # Mutating methods - these methods modify the list
    def remove(self, index):
        """ (LinkedList, int) -> NoneType

        Remove node at position index.
        Raise IndexError if index is >= the length of self.
        """
        if len(self) <= index:
            raise IndexError

        if index == 0:
            self.first = self.first.next
        else:
            # Iterate to (index-1)-th node
            curr = self.first
            for i in range(index - 1):
                curr = curr.next

            # Update link to skip over i-th node
            curr.next = curr.next.next

    def insert(self, index, item):
        """ (LinkedList, int, object) -> NoneType

        Insert a new node containing item at position index.
        Raise IndexError if index is > the length of self.
        Note that adding to the end of a linked list is okay.
        """
        if index > len(self):
            raise IndexError

        # Create new node
        new_node = Node(item)

        if index == 0:
            new_node.next = self.first
            self.first = new_node
        else:
            # Iterate to (index-1)-th node
            curr = self.first
            for i in range(index - 1):
                curr = curr.next

            # Update links to insert new node
            new_node.next = curr.next
            curr.next = new_node

    # --- Lab exercises start here ---

    def __contains__(self, item):
        """ (LinkedList, object) -> bool

        Return True if item is in this list.
        >>> linked = LinkedList([1, 2, 3])
        >>> 1 in linked
        True
        >>> 4 in linked
        False
        """
        pass

    def __str__(self):
        """ (LinkedList) -> str

        Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.
        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        """
        pass

    def __setitem__(self, index, new_item):
        """ (LinkedList, int, object) -> NoneType

        Store item at position index in self.
        Raise IndexError if index is >= the length of self.
        >>> lst = LinkedList([1, 2, 3])
        >>> lst[1] = 100
        >>> str(lst)
        '[1 -> 100 -> 3]'
        """
        pass

    def delete_item(self, item):
        """ (LinkedList, object) -> NoneType

        Remove the FIRST occurrence of item in self.
        Do nothing if self does not contain item.
        >>> lst = LinkedList([1, 2, 3])
        >>> lst.delete_item(2)
        >>> str(lst)
        '[1 -> 3]'
        """
        pass

    def map(self, f):
        """ (LinkedList, function) -> LinkedList

        Return a new LinkedList whose nodes store items that are obtained by
        applying f to each item in this linked list.
        Note: does not change this linked list.

        >>> list = LinkedList(['Hello', 'Goodbye'])
        >>> str(list.map(upper))
        ['HELLO' -> 'GOODBYE']
        >>> str(list.map(len))
        [5 -> 7]
        """
        pass

    # --- Exercise 4 starts here ---
    def __eq__(self, other):
        """ (LinkedList, LinkedList) -> bool

        Return True if self and other contain the same items,
        in the same order.

        You may not use any other Linked List methods in your solution!
        Instead, access the "items" attribute of self and other directly.

        >>> lst1 = LinkedList([1, 2, 3])
        >>> lst2 = LinkedList([1, 2, 3])
        >>> lst3 = LinkedList([1, 2, 100])
        >>> lst1 == lst2
        True
        >>> lst1 == lst3
        False
        """
        
        c1 = self.first
        c2 = other.first
        size1 = 0
        size2 = 0
        while c1 is not None:
            size1 = size1 + 1
            c1 = c1.next
        while c2 is not None:
            size2 = size2 + 1
            c2 = c2.next
            
        if size1 != size2:
            return False
        elif size1 == size2 == 0:
            return True
        else:
            i = 0
            while i != size1:
                if self[i] != other[i]:
                    return False
                else:
                    i += 1
            return True            