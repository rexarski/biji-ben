def rreverse(s):
    """ (String) -> String
    Return a string with reverse order.
    """
    if s == '':
        return s
    else:
        return rreverse(s[1:]) + s[0]

def count_length(lst):
    # this is a helper function to return the number length of a list of lists
    count = 0
    for i in lst:
        count += 1
    return count

def all_subsets(lst):
    """ (list) -> list of lists
    Return a list of all the subsets of given list.
    lst should not contain any repeated items.
    """
    
    # the subsets of [1, 2, 3] should be:
    # []
    # [1], [2], [3]
    # [1, 2], [2, 3], [1, 3]
    # [1, 2, 3]
    
    # and these can be subdivided into 2 groups: those with 1 in it and those without 1 in it,
    # Group1 -> [], [2], [3], [2, 3]
    # Group2 -> [1], [1, 2], [1, 3], [1, 2, 3]
    
    # recursively, we can divide Group1 into 2 parts: WITH and WITHOUT 2 in them.
    # so before that, we have [], [3] and another group is [2], [2, 3]
    # and long before that, we only have [], [3]
    
    # NOTE: the length of list of lists could not be ZERO!
    
    if count_length(lst) == 0:
        return [[]]
    else:
        result = []
        for subset in all_subsets(lst[1:]):
            result += [subset]
            result += [[lst[0]] + subset]
        return result
    
    