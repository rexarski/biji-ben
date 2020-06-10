# WEEK 12 Efficiency

# observation 1: Running time (usually) depends on machine (and what else is running)

# observation 2: depends on implementation

# observation 3: depends on input size

def size(stack):
    count = 0
    temp = Stack()
    
    while not stack.is_empty():
        temp.push(stack.pop())
        count += 1
    
    while not temp.is_empty():
        stack.push(temp.pop())
        
    return count

# proportional to n = size of stack

# 'linear time'

# Big-Oh notation: O(_)

# ignore constants: 3n, n + 5, ...
# focus on aysmptotic behaviour
# O(log n), O(n), O(n log n), O(n^2), ...

def remove_kth(stack, k):
    count = 0
    temp = Stack()
    
    while count < k:
        temp.push(stack.pop())
        count += 1
        
    kth = temp.pop()
    
    while not temp.is_empty():
        stack.push(temp.pop())
    
    return kth # actually this does not depend on the size of stack, but the value of k

# worst case, k is n, O(n), linear tiem
# best case, k is 1, O(1), 'constant time', runtime doesn't depend on input size

# most list methods depend on legnth (and index)
# (search, insert, delete, etc.)


# most tree methods depend on size and/or height

#--------- wednesday

def num_common(lst1, lst2):
    count = 0
    for x in lst1:
        for y in lst2:
            if x == y:
                count += 1
    return count

# if lst1 has length n, lst2 has length m, then this will execute m*n times

# O(mn)

# recurse on ...

# one subtree(depends on the height)           multiple subtrees(depends on the size)
#     3*                           3*
#    /    \                      /     \
#   4*    10                   4*       10*
#  /  \   /                  /   \      /
#  6  7*  9                 6*   7*    9*
#     /\                         / \
#    1*  2                      1* 2*

# height
# worst case: n = h
# worst case                  best case
# O                              O
#  \                            / \
#   O                           O  O
#    \                         /\  / \
#     O                       O  O O  O
#      \                     /\  /\
#       O                   O  O O O
#
#   n = h                   n = 2 ** h, h = log2(n)

# MEMOERY MODEL

# 'data' is stored in two places (on computers):
# stack and heap (note: special terms! not the ones we learned in class before)

# call stack (keeping track of function calls)
# argument values
# local variables
# return address
# unqiue to each function call*

#def f(a):
    #b = 5
    #if a == 0:
        #print(b)
    #else:
        #f(a - 1)
        #print(b)

#def g(x):
    #b = 10
    #return x

# two functions, even they have the same local variables, don't mean that 

# heap (where data lives)

# heap: memory available to program not used by stack
# numbers, lists, dictionaries, objects, classes, functions
# variables store references to locations in the heap

# Morals
# x = __ changes a reference
# x = y does not make a copy