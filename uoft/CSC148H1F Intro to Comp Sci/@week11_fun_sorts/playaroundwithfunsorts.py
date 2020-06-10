#two fun sorts

# RADIX SORT

# key idea: we can sort a list of integers digit by digit, rather than comparing them all at one. 

# There are two variants of radix sort: most-significant digit and least-significant digit

import math

def msd_radix(lst, d=None):
    if len(lst) < 2:
        return lst
    else:
        if d is None:
            d = 0
            for num in lst:
                d = max(d, math.floor(math.log10(num))+1)
            
        buckets = [[], [], [], [], [], [], [], [], [], []]
        for num in lst:
            if d == 0:
                return lst
            else:
                digit = (num // 10 ** (d-1)) % 10
                buckets[digit].append(num)
            
        sorted_lst = []
        for bucket in buckets:
            sorted_lst = sorted_lst + msd_radix(bucket, d-1)
        
        lst[:] = sorted_lst
    return lst

# another implementation of radix sort

def radixsort(lst):
    radix = 10
    maxLength = False
    tmp, placement = -1, 1
    
    while not maxLength:
        maxLength = True
        # declare and initialize buckets
        buckets = [[], [], [], [], [], [], [], [], [], []]
        
        # split lst between lists
        for i in lst:
            tmp = i / placement
            buckets[math.floor(tmp % radix)].append(i)
            if maxLength and tmp > 0:
                maxLength = False
        
        # empty lists into lst array
        a = 0
        for b in range(radix):
            buck = buckets[b]
            for i in buck:
                lst[a] = i
                a += 1
        
        # move to next digit
        placement *= radix

# if the length of the list is much greater than d, this means that radix sort takes approximately linear time!

#BOGOSORT

import random

def bogosort(lst):
    """ (list) -> NoneType
    
    Sort lst using the bogosort algorithm.
    """
    
    while not is_sorted(lst):
        random.shuffle(lst)

def is_sorted(lst):
    """ (list) -> bool
    
    Return True if list is sorted.
    """
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True

#BOGOBOGOSORT

def bogobogosort(lst):
    """ (list) -> NoneType
    
    Sort lst using the bogobogosort algorithm.
    """
    if len(lst) < 2:
        pass
    else:
        while not is_sorted(lst):
            lst_copy = lst[:-1]
            bogobogosort(lst_copy)
            if lst_copy[-1] < lst[-1]:
                lst[:-1] = lst_copy[:]
                break
            else:
                random.shuffle(lst)