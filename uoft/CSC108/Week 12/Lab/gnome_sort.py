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