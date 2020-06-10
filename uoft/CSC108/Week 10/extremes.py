def print_min_max(L):
    '''(list) -> NoneType
    Print the minimum and maximum values in list L.'''
    
    # Original version:
    #  - when list contains all negatives, max reported as 0
    #  - when list contains positives (non-zero), min reported as 0
    #min = 0
    #max = 0

    # Fixed version:
    min = L[0]  
    max = L[0]  
    
    # What about empty list? Would result in an error.
    # Should state how to handle empty lists in docstring and code should
    # match that specification.
    
    for value in L:
        if value > max:
            max = value
        if value < min:
            min = value
    print 'The minimum value is %s' % min
    print 'The maximum value is %s' % max
    
# list size: 0, 1, bigger
# values: positive? negative?
# position of min: front, back, "middle"
# position of max: front, back, "middle"
# min == max