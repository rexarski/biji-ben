def remove(self, index):
    
    # we need to change the 'next' attribute of node (index - 1)
    # from pointing to node (index) to node (index + 1)
    

    # don't forget about empty list!
    
    if index == 0:
        #self.first = self.first.next
        tmp = self.first.next
        self.first = tmp
    else:
        # Go to node (index - 1)
        curr = self.first
        for i in range(index - 1):
            curr = curr.next
            
        tmp = curr.next.next
        curr.next = tmp
        
def insert(self, index, item):
    """ (LinkedList, int, object) -> NoneType
    
    Insert a new node containing item at position index.
    Raise IndexError if index is > the length of self.
    Note that adding to the end of a linked list is okay.
    
    >>> lst = LinkedList(['CSC', 'hi', 15, -3.14])
    >>> lst.insert(2, 42)
    >>> # lst contains 'CSC', 'hi', 42, 15, -3.14
    """
    
    # Create a new node
    new_code = Node(item)
    
    # Go to node (index - 1)
    curr = self.first
    for i in range(index - 1):
        curr = curr.next
    
    old_next_node = curr.next    
    # Update curr's next attribute
    curr.next = new_node
    
    # Update new node's next attribute
    new_node.next = old_next_node
    
    