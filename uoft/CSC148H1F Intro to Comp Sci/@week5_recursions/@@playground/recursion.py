class EmptyValue:
    
    pass

class LinkedListRec:

    def __init__(self, items):
        """ (LinkedListRec, list) -> NoneType
        
        Create a new linked list containing the elements in items.
        If items is empty, self.first initialized to EmptyValue. 
        """
        if len(items) == 0:
            self.first = None
            self.rest = None
        else:
            self.first = items[0]
            self.rest = LinkedListRec(items[1:])
            
    def is_empty(self):
        return self.first is EmptyValue
    
    def __getitem__(self, index):
        if self.is_empty():
            raise IndexError
        elif index == 0:
            return self.first
        else:
            return self.rest.__getitem__(index - 1)
        # Or equivalently, self.rest[index - 1]
        
    # Recursive Linked List Mutation (Deletion)

    def remove(self, index):
        """ (LinkedListRec, int) -> NoneType
        
        Remove item at position index from the list.
        Raise an IndexError if index is out of bounds.
        """

        if self.is_empty():
            raise IndexError
        elif index == 0:
            self.remove_first()
        else:
            self.rest.remove(index - 1)

    def remove_first(self):
        if self.is_empty():
            raise IndexError
        else:
            self.first = self.rest.first
            self.rest = self.rest.rest

# A Non-List Example: Binary Strings

def all_binary_strings(n):
    """ (int) -> list of str
    
    Return a list of all binary strings of length n.
    >>> all_binary_strings(0)
    [']
    >>> all_binary_strings(2)
    ['00', '01', '10', '11']
    """
    
    if n == 0:
        return ['']
    else:
        short_strings = all_binary_strings(n - 1)
        
        strings = []
        for s in short_strings:
            strings.append('0' + s)
        for s in short_strings:
            strings.append('1' + s)
            
        return strings