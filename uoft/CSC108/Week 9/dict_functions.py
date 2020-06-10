def increment_count(d, k):
    '''(dict, object) -> NoneType
    Increment the value associated with key k
    in d. If k is not a key in d, add it with value 1.'''
    
    if k in d:
        d[k] += 1
    else:
        d[k] = 1
        
def invert(table):
    '''(dict) -> dict
    Return a new dict that is dict table inverted.'''
    
    index = {}                         
    for key in table.keys():
        value = table[key]
        if not index.has_key(value):
            index[value] = []            
        index[value].append(key) 
    return index