# last week
# arrays
# lookup = constant
# insert/delete = linear

# linked lists (cannot just jump, downside is need to .next, .next, .next..., but the good point is it's very efficient to get the first item)
# lookup = linear (but depends on which item you are looking up)
# insert/delete = (still need to loop through (index - 1) steps, that would take linear time as well, then why bother linked lists??????)

# imagine we have a long linked list, where index 4999 is very important, there would be many changes there. should have a more efficient way to update the info there, withouout looping items before 4999 every time we make changes around 4999.

# ---- till now, these are all we need to know before midterm 1

# [1, 2, 3, 4]
# |1| -> |2| -> |3| -> |4|

# THIS WEEK: not a new implementation of lists, but a higher level
# WHAT WE DO/THINK: 1 -> [2, 3, 4], i.e., the first item and the rest (a list)

# Recursive structure
# Break dwon an object into smaller part(s) with the same structure as original.
# for example, [2, 3, 4] is also a list like [1, 2, 3, 4]

# LinkedListRec
# first (object)
# rest (LinkedListRec)

# Thinking Recersively (important) is find the recursive structure. (though very hard)

class LinkedListReC:
    """Linked List with a recursive implementation.
    
    Note that there is no Node class any more.
    
    Attributes:
    - first (return the first item)
    - rest (return the memory address)
    """
    
    def __init__(self):
        if len(items) == 0:
            self.first = EmptyValue
            self.rest = None
        else:
            self.first = items[0]
            self.rest = LinkedListRec(items[1:])
        
    # Non-mutating methods
    
    def is_empty(self):
        # use a dummy class EmptyValue whose only use is to represent an empty list
        return self.first is EmptyValue
    
    def __len__(self):
        # thinking, how is the len([1, 2, 3, 4]) related with len([2, 3, 4])?
        # len([1, 2, 3, 4]) = 1 + len([2, 3, 4])
        # return 1 + self.rest.__len__()
        # or to say:
        # return 1 + len(self.rest)
        # but this is problematic if the list is empty!
        # so
        if self.is_empty():
            return 0
        else:
            # the length of self is 1 more than the length of the rest
            return 1 + self.rest.__len__()
    
    
    def __getitem__(self, index):
        if index == 0:
            return self.first
        else:
            # if I want the item at position index in self,
            # this is the *same* as the item at position (index-1) in self.rest
            return self.rest.__getitem__(index - 1)
            
    
    # Mutating methods
    
    def remove_first(self):
        pass