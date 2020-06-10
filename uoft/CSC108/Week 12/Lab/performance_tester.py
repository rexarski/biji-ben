import random
import time

def largest(L,i):
    n = i
    largest = L[i]
    ind_of_large = i
    while n != len(L) - 1:
        if L[n + 1] > largest:
            largest = L[n + 1]
            ind_of_large = n + 1
        n += 1
    return ind_of_large


def descending_selection_sort(L):
    for i in range(len(L)):
        L[largest(L,i)], L[i] = L[i], L[largest(L,i)]
    return L

def backwards_insertion_sort (L):
    i = len(L) - 1
    while i >= 0:
        help_insert(L,i)
        i -= 1
    return L
    
def help_insert(L, i):
    j = i + 1
    while j != len(L) and L[j] <= L[i]:
        j += 1
    value = L[i]
    del L[i]
    L.insert(j, value)
    
def gnome_sort(L):
    
    i = 0
    nxt_i = 1
    while i != len(L) - 1:
        if L[i] <= L[i + 1]:
            i = nxt_i
            nxt_i = nxt_i + 1
        else:
            L[i], L[i + 1] = L[i + 1], L[i]
            i -= 1
    return L

def generate_random_list(n, magnitude=1024):
    '''(int, int=1024) -> list of ints
    Return a list filled with n random numbers in the range
    (-magnitude, magnitude).'''

    random.seed()
    new_list = []
    for i in range(n):
        new_list.append(random.randrange(-magnitude, magnitude))
    return new_list

###############################################################
# Generate a list of specified size filled with random numbers
if __name__ == '__main__':
    myList = generate_random_list(2048)

    # Take the rough start time
    t1 = time.time()

    # Execute a sorting function
    gnome_sort(myList)
    # Take the rough end time
    t2 = time.time()

    # Provide an estimate of the execution time of the sorting function
    print 'Execution time:  %0.3f ms' % ((t2 - t1) * 1000.0)

###############################################################
