# LinkedList class
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
        curr = self.first
        while curr is not None:
            if curr.item == item:
                return True
            curr = curr.next
        return False

    def __str__(self):
        """ (LinkedList) -> str

        Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.
        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        """
        curr = self.first
        ret_str = "["
        
        while curr is not None:
            ret_str += str(curr.item)
            if curr.next is not None:
                ret_str += " -> "
            curr = curr.next
            
        ret_str += "]"
        
        return ret_str
                

    def __setitem__(self, index, new_item):
        """ (LinkedList, int, object) -> NoneType

        Store item at position index in self.
        Raise IndexError if index is >= the length of self.
        >>> lst = LinkedList([1, 2, 3])
        >>> lst[1] = 100
        >>> str(lst)
        '[1 -> 100 -> 3]'
        """
        curr = self.first
        
        if len(self) <= index:
            raise IndexError
        
        while index > 0:
            curr = curr.next
            index -= 1
            
        curr.item = new_item
        
    def delete_item(self, item):
        """ (LinkedList, object) -> NoneType

        Remove the FIRST occurrence of item in self.
        Do nothing if self does not contain item.
        >>> lst = LinkedList([1, 2, 3])
        >>> lst.delete_item(2)
        >>> str(lst)
        '[1 -> 3]'
        """
        # if the item we need to delete is the first item in the list, we delete the arrow after it as well;
        # if the item we need to delete is the last item in the list, we delete the arrow before it as well;
        # if the item is middle item, we define to delete the arrow after it.
        
        # if the first item in the LinkedList is the item to delete
        if self.first.item == item:
            self.first = self.first.next
        
        # otherwise
        prev = self.first
        
        if prev is not None:
            curr = prev.next
            while curr is not None:
                if curr.item == item:
                    prev.next = curr.next
                    return
                else:
                    prev = curr
                    curr = curr.next
                
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
        if self.is_empty == True:
            return self
        
        curr = self.first
        lst = []
        while curr is not None:
            lst.append(f(curr.item))
            curr = curr.next
            
        ln = LinkedList(lst)
        
        return ln

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
        pass
