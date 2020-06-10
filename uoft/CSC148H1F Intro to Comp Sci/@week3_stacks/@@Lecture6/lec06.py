class EmptyStackError(Exception):
    """Exception used when calling pop on empty stack."""
    pass

class Stack:
    """Stack implementation using a list, where the 'top' of the stack is the END of the list.
    """
    
    def __init__(self):
        """ (Stack) -> NoneType """
        self.items = []

    def is_empty(self):
        """ (Stack) -> bool """ # return true if ... else false if ...
        #return not self.items # can convert a list to Boolean, for example, not [] == True, not [1, 2, 3] == False.
        #return self.items == []
        return len(self.items) == 0
    
    def push(self, item):
        """ (Stack, object) -> NoneType """
        self.items.append(item) # it turns out that list in python has its own method 'list.pop()'
    
    def pop(self):
        """ (Stack) -> object """
        try:
            return self.items.pop()
        except IndexError:
            raise EmptyStackError
        
class Stack2:
    """Stack implementation using a list, where the 'top' of the stack is the FRONT of the list.
    """
    
    def __init__(self):
        """ (Stack) -> NoneType """
        self.items = [] # same
    
    def is_empty(self):
        """ (Stack) -> bool """ # return true if ... else false if ...
        return len(self.items) == 0 # same
    
    def push(self, item):
        """(Stack, object) -> NoneType
        Add a new element to the top of this stack.
        """
        self.items.insert(0, item) # note that this does not return anything!
        # this doesn't work before it overwrite the first item! if items list has something at the beginning!
        #self.items[0] = item
        #self.items[0:0] = item
    
    def pop(self):
        """(Stack) -> object
        Remove and return the element at the top of this stack.
        Raise EmptyStackError if trying to pop from an empty list.
        """
        try:
            item = self.items[0]
            self.items = self.items[1:]
            return item
        except IndexError:
            raise EmptyStackError        

    #after time comparison, Stack1 looks more efficient!
    
