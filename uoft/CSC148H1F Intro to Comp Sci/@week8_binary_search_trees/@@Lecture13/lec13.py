#INVARIANTS

# an empty linked list always looks like (root=EmptyValue, rest=None)
# an non-empty linked list always looks like (root=<value>, rest=<LinkedList>)
# guarantees no 'NoneType' erros with recursive methods.


# Empty Trees: (root=EmptyValue, subtrees=[])
# No empty trees in subtrees!

# -------------------------------------

# searching for an item:
# In a list? [5, 4, 3, 10, -1, 0]
# In a tree?
#             5
#        /   \     \
#       4     -1    0
#      / \
#     3   10

# worst case: linear time
# but searching in a sorted list is more efficient in general (half!)

# what if we search in a 'sorted tree'?

#BINARY SEARCH TREE

# binary: each node has at most 2 subtrees (i.e. it could have 1 subtree only or none at all)

# class BinarySearchTree:
# - self.root (object)
# - self.left (BinarySearchTree)
# - self.right (BinarySearchTree)

# BST Property: each item is >= all items in left subtree, < all items in right subtree.

# Warning: this must be true for all items, not just the root! (Recursive)

#          10
#       /      \
#      3      20
#    /   \    /   \
#    1    4   15   30
#         / \       \
#         4  6      40
# this is a BST

class EmptyValue:
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
