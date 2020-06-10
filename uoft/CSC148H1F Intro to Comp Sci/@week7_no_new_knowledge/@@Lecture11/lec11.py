class EmptyValue:
    pass


class Tree:
    
    def __init__(self, root=EmptyValue):
        """ (Tree, object) -> NoneType
        """
        self.root = root
        self.subtrees = []
        
    def is_empty(self):
        """ (Tree) -> bool """
        return self.root is EmptyValue
    
    def add_subtree(self, subtree):
        if self.is_empty():
            raise ValueError
        else:
            self.subtrees.append(subtree)

    # basic tree structure is:
    # - A tree has a root node which stores a single item (Analogous to the head attribute of the linked list.)
    # - A tree has zero or more subtress, each of which is a tree. (This is where trees and lists differ. You can think of a list as a tree that only ever has zero or one subtrees.)
    
    # a tree is either empty or non-empty.
    # every non-empty tree has a root node (which is generally drawn at the top), connected to zero or more subtrees.
    # the size of a tree is the number of nodes in the tree.
    
    # a leaf is a node with no subtrees.
    
    # the height of a tree is the length of the longest path from its root to one of its leaves.
    
    # the children of a node are all nodes directly connected underneath that node.
    
    # the descendants of a node are its children, the children of its children, etc.
    
    # the parent of a node is the one immediately above and connected to it; each node has one parent, excepet the root, which has no parent.
    
    # the ancestors of a node are its parent, the parent of its parent, etc.
    
    def size(self):
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in subtrees:
                size += subtree.size()
            return size
    
    # traversing a tree
    
    # idea: print out the root, then recursively print out all of the subtrees. THE EASY WAY:
    
    def print_tree(self):
        if not self.is_empty():
            print (self.root)
            for subtree in self.subtrees:
                subtree.print_tree()
                
    # but this would be problematic because it's gonna be vague if we print out the following:
    # >>> t1 = Tree(1)
    # >>> t2 = Tree(2)
    # >>> t3 = Tree(3)
    # >>> t4 = Tree(4)
    # >>> t4.add_subtree(t1)
    # >>> t4.add_subtree(t2)
    # >>> t4.add_subtree(t3)
    # >>> t5 = Tree(5)
    # >>> t5.add_subtree(t4)
    # >>> t5.print_tree()
    # >>> 5
    # >>> 4
    # >>> 1
    # >>> 2
    # >>> 3
    
    # who is whose?
    
    # so the BETTER WAY IS:
    
    def print_tree_indent(self, depth=0):
        if not self.is_empty():
            print(depth * '  ' + self.root)
            for subtree in self.subtrees:
                subtree.print_tree(depth + 1)
                
    
    