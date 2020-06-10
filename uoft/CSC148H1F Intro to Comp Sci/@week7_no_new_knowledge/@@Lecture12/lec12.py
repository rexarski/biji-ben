# Tree Deletion
# delete root? then we don't have that 'tree' any more.
# 1. General Strategies?
# 2. Special Cases?
# can use EmptyValue to represent the deleted root, we would remove the old value of the root, but this woudn't change the structure of the tree. and eventually we will end up with a tree full of empty nodes.

# INSTEAD: we are going to restructure the tree, replace the node with another value.

class EmptyValue:
    pass


class BinaryTree:
    """Binary Tree class.

    Attributes:
    - root (object): the item stored at the root, or EmptyValue
    - left (BinaryTree): the left subtree of this binary tree
    - right (BinaryTree): the right subtree of this binary tree
    """

    def __init__(self, root=EmptyValue):
        """ (BinaryTree, object) -> NoneType

        Create a new binary tree with a given root value,
        and no left or right subtrees.
        """
        self.root = root    # root value
        if self.is_empty():
            # Set left and right to nothing,
            # because this is an empty binary tree.
            self.left = None
            self.right = None
        else:
            # Set left and right to be new empty trees.
            # Note that this is different than setting them to None!
            self.left = BinaryTree()
            self.right = BinaryTree()

    def is_empty(self):
        """ (BinaryTree) -> bool
        Return True if self is empty.
        Note that only empty binary trees can have left and right
        attributes set to None.
        """
        return self.root is EmptyValue
    
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
    
    def delete_root(self):
        """ (BinarySearchTree) -> NoneType
        
        Delete root node of self.
        And replace it with one of the root of subtrees.
        """
        
        # actually this has two solutions for BinarySearchTree, pick left or pick right. We do LEFT here, and leave the rest to lab this week.
        if len(self.subtrees) == 0:
            # delete the root node, hence we have an empty tree!
            self.root = EmptyValue
        else:
            # set new root to be the root of the first subtree
            self.root = self.subtrees[0].root
            self.subtrees = self.subtrees[0].subtrees + self.subtrees[1:]
    
    def delete_item(self, item):
        """ (Tree, object) -> bool
        Delete *one* occurrence of item from this tree. 
        Return true if item was deleted, and False otherwise.
        """
        
        if self.is_empty():
            return False
        elif self.item == item:
            self.delete_root()
            return True
        else:
            for subtree in self.subtrees:
                # try to delete item from the subtree
                # subtree.delete_item(item) is problatic, since this would delte many many occurence, CANNOT STOP MYSELF!
                successful_deletetion = subtree.delete_item(item)
                if successful_deletion:
                    # once deleted anything, stop the loop and return True
                    if subtree.is_empty():
                        # note that we don't want an empty tree here!
                        self.subtrees.remove(subtree)
                    return True
            # looped through all subtrees, never returned True
            return False