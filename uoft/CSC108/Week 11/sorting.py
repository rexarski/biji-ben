def bubble_sort(L):
    '''(list) -> list
    Sort the items in L into non-descending order and return the sorted list.'''
    
    for i in range(len(L)):
        for j in range(0, len(L) - 1 - i):
            if L[j] > L[j + 1]:
                L[j], L[j + 1] = L[j + 1], L[j]
    return L


def find_min(L, i):
    '''(list, int) -> int
    Return the index of the smallest item in L[i:].'''
    
    smallest = i
    for j in range(i + 1, len(L)):
        if L[j] < L[smallest]:
            smallest = j
    return smallest


def selection_sort(L):
    '''(list) -> list
    Sort the items in L into non-descending order and return the sorted list.'''
    
    i = 0
    
    # L[:i] is sorted
    while i != len(L):
        smallest = find_min(L, i)
        L[smallest], L[i] = L[i], L[smallest]
        i += 1
    return L


def selection_sort2(L):
    '''(list) -> list
    Sort the items in L into non-descending order and return the sorted list.'''
    
    for i in range(len(L)):
        smallest = find_min(L, i)
        L[smallest], L[i] = L[i], L[smallest]
    return L


def insert(L, i):
    '''(list, int) -> NoneType
    L[:i] is sorted.  Move L[i] to where it belongs in L[:i].'''

    # the value to be inserted into the sorted part of the list
    value = L[i]
    
    # find the spot, i, where value should go
    while i > 0 and L[i - 1] > value:
        L[i] = L[i - 1]
        i -= 1
    L[i] = value
    
    
def insertion_sort(L):
    '''(list) -> list
    Sort the items in L into non-descending order and return the sorted list.'''

    i = 0
    
    # L[:i] is sorted
    while i != len(L):
        insert(L, i)
        i += 1
    return L


def insertion_sort2(L):
    '''(list) -> list
    Sort the items in L into non-descending order and return the sorted list.'''

    for i in range(len(L)):
	insert(L, i)
    return L


def merge(left, right):
    '''(list, list) -> list
    Return the list made by merging sorted lists left and right.'''
    
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
	if left[i] <= right[j]:
	    result.append(left[i])
	    i = i + 1
	else:
	    result.append(right[j])
	    j = j + 1

    # One of the sublists has elements left over; the other is empty. Copying
    # both does no harm, since the empty one will add nothing.
    result += left[i:]
    result += right[j:]
    return result


def merge_sort(L):
    '''(list) -> list
    Sort the items in L into non-descending order and return the sorted list.'''

    if len(L) < 2:
	return L
    else:
	middle = len(L) / 2
	left = merge_sort(L[:middle])
	right = merge_sort(L[middle:])
	return merge(left, right)
