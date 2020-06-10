# week 10 - sorting

# going to talk about one specific data processing operation: sorting

# learned: bubble sort, selection sort, insertion sort (those are iterative, loops, basically size n -> n^2 steps)

# to learn: two faster sorting algorithms
# mergesort
# quicksort
# both divide-and-conquer algorithms: split up the input list into two parts, recursively sort each part, and then combine the two parts into a single sorted list. where they differ is in the splitting and combining: mergesort does the hard work in the combine step, and quicksort does the hard work in the divide step.

# MERGESORT
# split it up into two halves, then sort each half. then it should be the case that if we take two lists that are sorted, we can merge them efficiently into a single sorted list.

def mergesort(lst):
    """ (list) -> list
    
    Return a sorted list with the same elements as lst.
    Do *not* mutate lst.
    """
    
    if len(lst) <= 1:
        # return a copy of lst
        return lst[:]
    else:
        m = len(lst) // 2
        left_sorted = mergesort(lst[:m])
        right_sorted = mergesort(lst[m:])
        # 'merge' the two sorted halves (how?)
        return merge(left_sorted, right_sorted)

# how to merge?
# build up a sorted list from the two original lists, and the key idea is that if we're smart about which elements we compare against each other, after every comparison we can add an element to the sorted list.

def merge(left, right):
    """ (list, list) -> list
    
    Precondition: left and right are sorted
    
    Return a sorted list with the elements in left and right.
    """
    i = 0
    j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[i]:
            merged.append(left[i])
            i = i + 1
        else:
            merged.append(right[j])
            j = j + 1
    
    # now either i = len(left) or j = len(right)
    # the remaining elements of the other list can all be added to the end
    # note that at most ONE of left[i:] and list[j:]
    return merged + left[i:] + right[j:]

# QUICKSORT

# pick some arbitrary element in the list and call it the *pivot*, then split up the list into two parts:
# the elements less than (or equal to) the pivot, and those greater than the pivot.
# sort each part separately, then combine. (combination is easy)

def quicksort(lst):
    """ (list) -> list
    
    Return a sorted list with the same elements as lst.
    Do *not* mutate lst.
    """
    
    if len(lst) <= 1:
        return lst[:]
    else:
        # pick pivot to be first element
        pivot = lst[0]
        
        # partition rest of lists into two parts
        smaller, bigger = partition(lst[1:], pivot)
        
        # recurse on each partition
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)
        
        # Return! Notice the simple combining step
        return samller_sorted + [pivot] + bigger_sorted
    
# use loop to implement partition

def partition(lst, pivot):
    """ (list, object) -> (list, list)
    
    Return two lists, where the first is the items in lst
    that are <= pivot, and the second is the items in lst
    that are > pivot.
    """
    smaller = []
    bigger = []
    
    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)
            
    return smaller, bigger