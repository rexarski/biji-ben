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

    