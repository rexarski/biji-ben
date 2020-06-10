# Lab 6 - More Recursion Practice
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu


# Task 1: Subsets revisited
def all_subsets(lst):
    """ (list) -> (list of lists)

    Precondition: lst contains no duplicates.
    Return a list of all of the subsets of lst; order does not matter.
    """
    
    if count_length(lst) == 0:
        return [[]]
    if count_length(lst) == 1:
        return [[], lst]
    else:
        result = []
        for subset in all_subsets(lst[1:]):
            result += [subset]
            result += [[lst[0]] + subset]
    return result

def count_length(lst):
    """ (list) -> (int)
    
    Return the number of lists in a list of lists.
    """
    count = 0
    for i in lst:
        count += 1
    return count 

# Task 2: Binary Search
def return_half(lst, side):
    """ (list, bool) -> list
    Precondition: len(lst) is a power of 2, including 1.
    If side is True, return a new list containing the items in the *left half*
    of lst; if side is False, return a new list containing the items
    in the *right half*. (Hint: use list slicing.)

    >>> nums = [10, 3, -4, 1]
    >>> return_half(nums, True)
    [10, 3]
    >>> return_half(nums, False)
    [-4, 1]
    """
    half = len(lst) // 2 # integer division!!!
    if side == True:
        lst = lst[:half]
        return lst[:half]
    else:
        lst = lst[-half:]
        return lst[-half:]

def mid_value(lst):
    """ (list) -> (float)
    
    Return the median of a sorted integer list.
    """
    if len(lst) % 2 == 0:
        half = len(lst) // 2
        return (lst[half - 1] + lst[half]) / 2
    else:
        return lst[(len(lst) - 1) // 2]

def binary_search(lst, item):
    """ (list, object) -> bool
    Precondition: lst is a sorted list.
    Return True if item is in lst.

    >>> nums = [10, 3, -4, 1]
    >>> binary_search(nums, 1)
    True
    >>> binary_search(nums, 40)
    False
    >>> binary_search([1], 1)
    True
    """
    # What is the base case?

    # Hint for the recursive implementation: check your indexes very carefully!
    if lst == []:
        return False
    elif len(lst) == 1:
        return lst == [item]
    else:         
        return binary_search(return_half(lst, mid_value(lst) >= item), item)

# Task 3: Indexed Binary Search
def print_left(lst, left=0, right=None):
    """ (list, int, int) -> NoneType
    Precondition: 0 <= left < right <= len(lst) (if left and right are given)

    If right is None, first set right = len(lst).
    Then, print all of the items in the left half of lst[left:right].
    For simplicity, assume that len(lst[left:right]) is even.

    >>> nums = [3, 10, 4, 15, -1, -1, 2, 16]
    >>> print_left(nums, 0, 4)
    3
    10
    None # in Wing only
    >>> print_left(nums, 3, 5)
    15
    None # in Wing only
    >>> print_left(nums)
    3
    10
    4
    15
    None # in Wing only
    """
    # This code handles the default value of right.
    
    # YOUR CODE GOES HERE
        # You may use a loop for this question.
        # Hint: the hard part of this question is actually calculating the
        # correct midpoint. Do the math carefully, because it's easy to
        # get an off-by-one error!    
    
    if right is None:
        right = len(lst)
    mid = (left + right + 1) // 2
    for item in lst[left:(mid)]:
        print(item)


def indexed_binary_search(lst, item, left=0, right=None):
    """ (list, object, int, int) -> bool
    Precondition: lst is a sorted list, 0 <= left <= right <= len(lst)
                  (if left and right are given)

    Return True if item is in lst[left:right].
    """
    if right is None:
        right = len(lst)
        
    if right == left:
        return False
    
    true_len = right - left
    mid_index = true_len // 2 + left
    mid_item = lst[mid_index]
    
    if mid_item == item:
        return True
    
    if item < mid_item:
        return indexed_binary_search(lst, item, left, mid_index)
    
    else:
        return indexed_binary_search(lst, item, mid_index + 1, right)

# YOUR CODE GOES HERE
    # Hint: your code will be very similar to binary_search;
    # just convert your base case and recursive calls to their index versions.