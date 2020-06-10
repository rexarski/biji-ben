# Lab 11 - Timsort!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------


def mergesort(lst, i=0, j=None):
    """ (list, int, int) -> NoneType

    Sort the items in lst[i:j] in non-decreasing order.
    Note: this mutates the list.
    """

    if j is None:
        j = len(lst)

    if i < j - 1:
        m = (i + j) // 2
        mergesort(lst, i, m)
        mergesort(lst, m, j)
        merge(lst, i, m, j)


def merge(lst, i, mid, j):
    """ (list, int, int, int) -> NoneType

    Precondition: lst[i:mid] and lst[mid:j] are sorted.

    Change lst so that lst[i:j] is sorted.
    """

    result = []
    left = i
    right = mid
    while left < mid and right < j:
        if lst[left] < lst[right]:
            result.append(lst[left])
            left = left + 1
        else:
            result.append(lst[right])
            right = right + 1

    lst[i:j] = result + lst[left:mid] + lst[right:j]


def find_runs(lst):
    """ (list) -> list of (int, int)
    Precondition: lst is non-empty
    Return a list of tuples indexing the runs of lst.

    >>> find_runs([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 7), (7, 8)]
    >>> find_runs([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs([10, 4, -2, 1])
    [(0, 1), (1, 2), (2, 4)]
    """
    runs = []

    # Variables to keep track of the start and end points
    # of a run
    run_start = 0
    run_end = 1
    while run_start < len(lst):
        # How can you tell if a run should continue?
        i = run_start
        if run_end >= len(lst):
            runs.append((run_start, run_end))
            break
        while lst[run_end] >= lst[i]:
            run_end += 1
            i += 1
            if run_end >= len(lst):
                break
        # How can you tell if a run is over?
        runs.append((run_start, run_end))
        run_start = run_end
        run_end += 1

    return runs

def timsort(lst):
    """ (list) -> NoneType
    Sort lst (mutating function).
    """
    runs = find_runs(lst)
    while len(runs) > 1:
        runs.pop()
        b = runs.pop()
        left = b[0]
        new_sorted_lst = mergesort(lst, left, len(lst))
        # we made a mistake here, just change len(lst-1) to len(lst)
        runs.append((left, len(lst) - 1))
        # append the new run representing the sorted list
        
    # Treat runs as a stack and repeatedly merge the top two runs
    # When the loop ends, the only run should be the whole list.
    # HINT: you should be able to use the "merge" function provided
    # in this file.


def find_runs2(lst):
    """ (list) -> list of (int, int)
    Return a list of tuples indexing the runs of lst.
    Now, a run can be either ascending or descending!

    >>> find_runs2([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 8)]
    >>> find_runs2([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs2([10, 4, -2, 1])
    [(0, 3), (3, 4)]
    """
    # Hint: this is similar to find_runs, except
    # you'll need to keep track of whether the "current run"
    # is ascending or descending.
    runs = []

    # Variables to keep track of the start and end points
    # of a run
    
    run_start = 0
    run_end = 1
    while run_start < len(lst):
        i = run_start
        if run_end >= len(lst):
            if lst[-1] >= lst[-2]:
                runs.append((run_start, run_end))
                break
            else:
                runs[-1][1] = len(lst)
                break
        if lst [run_end] >= lst[i]:
            while lst[run_end] >= lst[i]:
                run_end += 1
                i += 1
                if run_end >= len(lst):
                    break
        else:
            while lst[run_end] < lst[i]:
                run_end += 1
                i += 1
                if run_end >= len(lst):
                    break
        lst[run_start:run_end] = lst[run_start:run_end][::-1]
        runs.append((run_start, run_end))
        run_start = run_end
        run_end += 1

    return runs


def find_runs3(lst):
    """ (list) -> list of (int, int)
    Same as find_runs2, but each run (except the last one)
    must be of length >= 32.
    """
    pass


# Insertion sort
def insertion_sort(lst, left, right):
    """ (list) -> NoneType
    Sort the items in lst[left:right] in non-decreasing order.
    """
    for i in range(left + 1, right):
        # Find where lst[i] belongs in lst[left:i], but don't swap!
        j = i - 1
        while j >= left and lst[j] > lst[j+1]:
            lst[j], lst[j+1] = lst[j+1], lst[j]
            j -= 1


def merge2(lst, i, mid, j):
    """ (list, int, int, int) -> NoneType
    Precondition: lst[i:mid] and lst[mid:j] are sorted.

    Change lst so that lst[i:j] is sorted.
    Only use temporary storage of size (mid - i).
    """
    pass


def timsort2(lst):
    """ (list) -> NoneType
    Sort lst using the version of timsort from Task 6.
    """
    pass
