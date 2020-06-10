# a node in a binary tree has the binary search tree property if its value is greater than or equal to all node values in its left subtree, and less than all node values in its right subtree.

# a binary tree is a binary search tree if every node in the tree satisfies the binary search tree property (note that it's possible in general for some nodes to satisfy this but not others)

class EmptyTreeError:
    pass

class BinarySearchTree:
    def __init__(self, root=EmptyValue):
        self.root = root # root value
        if self.is_empty():
            # set left and right to nothing
            # because this is an empty binary tree
            self.left = None
            self.right = None
        else:
            # set left and right to be new empty trees.
            # note that this is different than setting them to None!
            self.left = BinarySearchTree()
            self.right = BinarySearchTree()
            
    def is_empty(self):
        return self.root is EmptyValue
    
    # general tree: standard search algorithm is to compare the item against the root, and then search in each of its subtrees until either the item is found, or all the subtrees have been searched. WORST CASE: everything is searched once but the item is not in the tree.
    
    # but for BST is different:
    
    def __contains__(self, item):
        if self.is_empty():
            return False
        elif item == self.root:
            return True
        elif item < self.root:
            return self.left.__contains__(item)
        else:
            return self.right.__contains__(item)
        
    # IDEA CASE: the BST is balanced, then we need up to log_2^n trials to find the item at most; problem is, if the tree is very unbalanced, then the worst case would still end up checking every node!
    
    # it's common that the amount of time an algorithm takes depends on the height of the tree rather than simply the number of nodes.
    
    # the efficiency, not only in searching, but in adding/removing nodes
    
    # INSERTION
    
    # basic idea: to avoid changing the contents of the tree too much, we will recurse down the tree until we reach an empty spot to insert the new leaf into.
    
    # however, different from general tree where we did this randomly, here we need th PRESERVE the BINARY SEARCH TREE PROPERTY.
    
    def insert(self, item):
        if self.is_empty():
            # make new leaf node
            self.root = item
            self.left = BinarySearchTree()
            self.right = BinarySearchTree()
            
        elif item <= self.root:
            self.left.insert(item)
        else:
            self.right.insert(item)
            
    # if balance, efficient; unbalanced, inefficient!
    
    def extract_max(self):
        """ (BinarySearchTree) -> object
        
        Remove and return the maximum value in self.
        """
        
        if self.is_empty():
            raise EmptyTreeError
        elif self.right_is_empty():
            temp = self.root
            # copy left subtree to self, because root node is removed.
            self.root = self.left.root
            self.right = self.left.right
            new_left = self.left.left
            self.left = new_left
            return temp
        else:
            return extract_max(self.right)
        
    # so far, the idea of deleteing the roots is pretty straightforward:
    # 0. if the tree is empty, raise an error
    # 1. extract the maximum from the left subtree
    # 2. set the root value equal to the extracted value
    
    def delete_root(self):
        if self.is_empty():
            raise EmptyTreeError
        else:
            self.root = self.left.extract_max()

    ## equivalently, we can define extract_min then, here for delete_root(self), we can redefine self.root = self.right.extract_min()
    
    # therefore:
    
    def delete(self, item):
        if not self.is_empty():
            if self.root == item:
                self.delete_root()
            elif item < self.root:
                self.left.delete(item)
            else:
                self.right.delete(item)
    
    # still, this is problematic, and need to be fixed in lab.