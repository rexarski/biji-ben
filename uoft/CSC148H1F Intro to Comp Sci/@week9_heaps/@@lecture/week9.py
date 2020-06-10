# next Wednesday midterm2
# cover up and until last week's material

# last week: BSTs, search, insert, delete

# a new ADT: Priority Queue
# example: insert some items with priority
# related methods: find max, extract max, insert, delete certain

# distinct from stack and queue

# implement priority queue with an ADT called Heaps (a twisted version of our old friend)

# binary trees with two invariants:
# 1. "complete"
# 2. Heap property
# though similar, but different from BST

# What does complete mean? "up and left"
#       4
#      / \
#     3   10
#     /     \
#    2       11
# this is not complete

#      3
#     / \
#    4   5
#   / \  /
#   1  2 9
# this one is!

# recall from last week's exercise, if we have a complete binary tree, we can always write it in a list representation, for the one above:
# [3, 4, 5, 1, 2, 9]
# why can we write it so easily? b/c there's no gap!
# and like we what did in exercise, we define the first item in such list has index 1, then etc. The index 0 is given to None.
# therefore, left = 2 * index, and right = 2 * index + 1

# HEAP PROPERTY
# node item >= all items in subtrees
#      20
#     / \
#    4   10
#   / \   / \
#  3   2  6   1

class Heap:
    
    def __init__(self):
        self.items = [None]
    
    def is_empty(self):
        return self.items == [None]
    
    # helper function
    def swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i] # multiple assignment feature of python
        
    def get_max(self):
        """ (Heap) -> object
        
        Return the largest item stored in self.
        """
        if self.is_empty():
            raise IndexError
        else:
            return self.items[1]
    
    # algorithm for extract the max:
    # 1. store the root item for returning later
    # 2. remove the last leaf, take the value stored there and store it in the root.
    # 3. this might not satisfy the heap property, so now recursively go down the tree, swapping the current value with the larger of its two children
    
    #       20
    #       / \
    #      4   10
    #     /\   /\
    #    3  2  7  9
    # take out the node 20, the final tree wil be like below (because it has to be complete):
    #       ?
    #       / \
    #      ?   ?
    #     /\   /
    #    ?  ?  ?
    # so try this:
    #       9
    #       / \
    #      4   10
    #     /\   /
    #    3  2  7   
    # then keep swapping 9 with (4, 10), in this case, which is 10 because it's larger, until we have the desired result.
    
    def extract_max(self):
        if self.is_empty():
            raise IndexError
        else:
            largest = self.items[1]
            self.items[1] = self.items.pop()
            # last leaf removed, and make it the new root
            self.bubble_down(1) # this step is gonna be recursive, keep swapping until the whole tree statisfies Heap property
    
    # so here comes the helper function:
    def bubble_down(self, index):
        """ (Heap, int) -> NoneType
        
        Restore heap property for the tree rooted at index.
        Note that when this is called, only the item as position index might not satisfy the heap property; all other nodes in the tree already do.
        """
        
        index_item = self.items[index]
        left = index * 2
        right = index * 2 + 1
        
        if right < len(self.items):
            # index node has two children
            left_item = self.items[left]
            right_item = self.items[right]
            if index_item < left_item < right_item:
                self.swap(index, right)
                self.bubble_down(right)
            elif index_item < right_item <= left_item:
                self.swap(index, left)
                self.bubble_down(left)
        elif left < len(self.items):
            # index node has just the left child
            left_item = self.items[left]
            if index_item < left.item:
                self.swap(index, left)
                self.bubble_down(left)
    
    
    # -------
    # Heap Insertion
    
    def insert(self, item):
        self.items.append(item)
        self.bubble_up(len(self.items) - 1)
    
    def bubble_up(self, index):
        """ (Heap, int):
        
        Move the item at position index up to its proper spot in the heap.
        Note: the only nodes where the heap property might fail to hold are the ancestors of index.
        """
        
        parent = index // 2
        if index == 1:
            # The current node is the root, so it has no ancestors
            # this means the heap property must be satisfied
            pass
        else:
            parent = index // 2
            if self.items[parent] < self.items[index]:
                self.swap(index, parent)
                self.bubble_up(parent)
            