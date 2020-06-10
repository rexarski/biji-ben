class BinarySearchTree:
    
    def __init__(self, root=EmptyValue):
        self.root = root
        if self.is_empty():
            self.left = None
            self.right = None
        else:
            self.left = BinarySearchTree()
            self.right = BinarySearchTree()
    
    def is_empty(self):
        return self.root is EmptyValue
    
    #Non-mutating
    
    #Find the size.
    #Find the number of leaves.
    #Find the number of internal nodes.
    #Find the sum of the items.
    #Find how many times a given item appears.
    #Find the number of duplicates.
    #Find the number of even items.
    #Count the number of nodes at depth d.
    #Find the maximum item.
    #Find the minimum item.
    #Find the k-th smallest item.
    #Find the k-th largest item.
    #Return a list containing the items <= 10.
    #Return a list containing the items >= 10.
    #Mutating
    
    #Remove the root.
    #Remove the smallest item.
    #Remove a single occurrence of 10.
    #Remove all occurrences of 10.
    #Remove all numbers <= 10.
    #Remove all even numbers.
    #Insert a given item.
    #Insert a list of given items.
    #(BST only) Pick a different item to be the root, and restructure the tree accordingly.   