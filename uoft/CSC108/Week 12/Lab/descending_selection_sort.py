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
