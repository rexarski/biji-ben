# ------- from last lecture

class EmptyValue:
    pass

class EmptyBSTError:
    pass

class BinarySearchTree:
    
    # Attributes:
    # - root (object): the root value stored in the BST, or EmptyValue if the tree is empty
    # - left (BinarySearchTree): the left subtree, or None if the ENTIRE tree is empty
    # - right (BinarySearchTree): the right subtree, or None if the ENTIRE tree is empty
    
    def __init__(self, root=EmptyValue):
        self.root = root
        if self.is_empty():
            self.left = None
            self.right = None
        else:
            self.left = BinarySearchTree()
            self.right = BianrySearchTree()
    
    def is_empty(self):
        return self.root is EmptyValue
    
    def print_tree(self, depth=0):
        if not self.is_empty():
            print(depth * '   ' + str(self.root))
            self.left.print_tree(depth + 1)
            self.right.print_tree(depth + 1)
            
    def __contains__(self, item):
        # the fact that you only need to check one tree each time comes from the property of BST
        if self.is_empty():
            return False
        elif item == self.root:
            return True
        elif item < self.root:
            return self.left.__contains__(item)
        else:
            return self.right.__contains__(item) # or 'return item in self.right', because __contains__ is a special form of 'in'
        
    # ------- this lecture: Mutation (Insertion & Deletion)
    
    #          10
    #        /     \
    #       5       15
    #     / \       \
    #     4  7       20
    #    /\   \      / \
    #    1 5   9     17  30
    
    # now we want to insert 6.
    # In fact, there is only one place that 6 can go to, which is the left of 7.
        
    def insert(self, item):
        """ (BinarySearchTree, object) -> NoneType
        
        Insert item into this tree in the correct location.
        Do not change positions of any other nodes.
        """
        if self.is_empty():
            self.root = item
            self.left = BinarySearchTree()
            self.right = BinarySearchTree() #!!!
        elif self.root >= item:
            self.left.insert(item)
        #elif self.root > item:
            #self.left.insert(item)
        else:
            self.right.insert(item)
            
    
    #          10
    #        /     \
    #       5       15
    #     / \       \
    #     4  7       20
    #    /\   \      / \
    #    1 5   9     17  30    
    
    # say now we want to delete item.
    # the simplest case: delete the root 10
    # then we should: move all the left of 10 to left of 15
    # (take the whole left subtree tree to the left side of the whole right subtree)
    
    # if:
    #          10
    #        /     \
    #       5       15
    #     / \       /  \
    #     4  7     12  20
    #    /\   \        / \
    #    1 5   9     17  30
    
    # the only two solutions now are:
    # 1. to remove 10 and put 12 at the top. (smallest in right subtree) 
    # 2. to remove 10 and put 9 at the top. (largest in left subtree)
    #          12                              9
    #        /     \                          /   \ 
    #       5       15                      5      15
    #     / \         \                   /  \     / \
    #     4  7         20                4    7   12   20
    #    /\   \        / \              / \            /  \
    #    1 5   9     17  30            1  5           17   30
    
    def delete_item(self, item):
        """ (BinarySearchTree) -> NoneType
        Deletes item, if it's in the tree.
        """
        if self.is_empty():
            pass
        elif self.item == root:
            self.delete_root()
        elif self.root > root:
            self.left.delete_item(item)
        else:
            self.right.delete_item(item)
    
    def delete_root(self):
        """(BinarySearchTree) -> NoneType
        Removes the root item from this BST (and replaces it!).
        """
        if self.is_empty():
            raise EmptyBSTError
        else:
            self.root = self.left.extract_max()
    
    def extract_max(self):
        """(BinarySearchTree) -> object
        Remove and return the largest object contained in this tree.
        """
        # so we are going to do this in one way (leave the other!)
        if self.is_empty():
            raise EmptyBSTError
        elif self.right.is_empty():
            # this is the base case, where extract_max ends!
            temp = self.root
            # copy over the attributes of the left subtree into self
            self.root = self.left.root
            self.right = self.left.right
            self.left = self.left.left
            return temp # don't forget to return the result
        else:
            return self.right.extract_max() # without 'return', we will just delete but not return it
        