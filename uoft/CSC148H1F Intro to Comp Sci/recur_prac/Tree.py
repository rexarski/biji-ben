class EmptyValue:
    pass

class Tree:
    
    def __init__(self, root=EmptyValue):
        self.root = root
        self.subtrees = []
        
    def is_empty(self):
        return self.root is EmptyValue
    
    #1. Non-mutating
    
    #1.1 Find the size of the tree.
    def size(self):
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self.subtrees:
                size += subtree.size()
            return size
        
    #1.2 Count the number of leaves of the tree.
    def count_leaf(self):
        if self.subtrees == []:
            return 1
        else:
            count = 0
            for subtree in self.subtrees:
                if subtree.subtrees == []:
                    count += subtree.count_leaf()
            return count

    #1.3 Count the number of internal nodes of the tree.
    # use size - leaf - root
    
    #1.4 Count the number of nodes at depth d in the tree.
    # use size at depth d - size at depth (d-1)
    
    #1.5 Count the number of nodes at depth <= d in the tree.
    # just size at depth d
    
    #1.6 Count the number of nodes at depth >= d in the tree.
    
    #1.7 Find the number of times a given item occurs in the list.
    
    #1.8 Find the sum of all the items in the list.
    
    #1.9 Find out if there is a repeated item in the list.

    #1.10 Count the number of repeated items in the list.

    #1.11 Count the number of even items in the list.

    #1.12 Count the number of items two trees have in common.
    
    #2. Mutating
    

    #2.1 Remove the root of the tree.

    #2.2 Remove all of the nodes at depth 2 in the tree.

    #2.3 Remove all of the nodes at depth d in the tree.

    #2.4 Insert a new item at the root of the tree.

    #2.5 Insert a new item at depth d in the tree.

    #2.6 Insert a whole new tree into the tree.

    #2.7 Restructure the tree so that each node has at most 2 children (i.e., turn into a binary tree).
    
    #2.8 Restructure the tree so that each node has at most d children.

    #2.9 Restructure the tree so that each node has at most as many children as its parent does. (Root node can have any number of children.)

#       1
#     /  \
#     2   3
#    /|\  /\
#   4 5 6 7 8

t1 = Tree()
t2 = Tree()
t3 = Tree()
t4 = Tree()
t5 = Tree()
t6 = Tree()
t7 = Tree()
t8 = Tree()
t1.root = 1
t1.subtrees = [t2, t3]
t2.root = 2
t2.subtrees = [t4, t5, t6]
t3.root = 3
t3.subtrees = [t7, t8]
t4.root = 4
t5.root = 5
t6.root = 6
t7.root = 7
t8.root = 8    