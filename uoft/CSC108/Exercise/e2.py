def get_upper_list(L):
    '''(list of strs) -> list of strs
    Return a new list of strs that contains the strs from the \
    original list converted to uppercase.'''

    index = 0
    L2 = []
    while index <= (len(L) - 1):
        new_string = L[index].upper()
        L2 += [str(new_string)]
        index += 1
    return L2
        


def convert_to_upper(L):
    '''(list of strs) -> NoneType
    Convert the strS in the given list to uppercase.'''
    
    for k in range(len(L)):
        L[k] = L[k].upper()


def get_str_list(big_list):
    '''(list of lists of strs) -> list of strs
    Return a list of strS, where each str is the concatenation of the \
    strS from the corresponding element of the given list.'''

    rlist = []
    for l in big_list:
        rstring = ''
        for s in l:
            rstring += s
        rlist.append(rstring)
    return rlist
