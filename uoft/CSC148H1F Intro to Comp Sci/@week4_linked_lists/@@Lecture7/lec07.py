class Node:
    
    def __init__(self):
        self.item = item
        self.next = None # Initially pointing to nothing
        
class LinkedList:
    
    def __init__(self, items):
        """ (LinkedList, list) -> NoneType
        Create Node objects linked together in the order provided in items.
        Set the first node of the chain as the first item in items.
        """

        if len(items) == 0:  # No items, and an empty list!
            self.first = None
        else:
            self.first = Node(items[0])
            current_node = self.first # for every other item in the list, we need to point it to another one
            for item in items[1:]:
                current_node.next = Node(item)
                current_node = current_node.next
        
    # Non-mutating methods: these methods do not change the list
    def is_empty(self):
        """ (LinkedList) -> bool
        Return True if this list is empty.
        """
        
        return self.first is None
    
    def __len__(self): # List does not have a len() method, when we use double underscore, we are going to make a method where we can use like this len()
        """ (LinkedList) -> int
        Return the number of elements in this list.
        """
        
        count = 0
        curr = self.first
        while curr is not None:
            # 'doing somehting with curr'
            count += 1
            curr = curr.next
        return count
    
    def __getitem__(self, index):
        """ (LinkedList, int) -> object
        Return the item at position index in this list.
        Raise IndexError if index is >= the length of self.
        """
        if index > self.__len__ - 1:
            raise IndexError
        else:
            curr = self.first
            count = 0
            while count < index:
                count += 1
                curr = curr.next
            return curr.item    
        