def total_length(L):
    '''(list of strs) -> int
    Return the total length of all the strs in L.'''
    
    total = 0
    for item in L:
        total = total + len(item)
    return total

    # Another version (accumulate lengths in a list of ints):
    #str_lens = []
    #for item in L:
        #str_lens.append(len(item))
    #return sum(str_len)
    
def square_list(int_list):
    ''' (list of ints) -> list of ints
    Return a new list that contains the values
    from int_list squared.
    '''
    
    squared_list = []
    for item in int_list:
        squared_list.append(item ** 2)
    return squared_list


def to_upper_broken(str_list):
    '''(list of strs) -> NoneType
    Convert all strs in str_list to uppercase.'''
    
    # item refers to a single string that's in the list.
    # But strings are immutable, so we don't change it, we get a new one.
    # item refers to the new one, but the list doesn't!
    for item in str_list:
        item = item.upper()

def to_upper(str_list):
    '''(list of strs) -> NoneType
    Convert all strs in str_list to uppercase.'''
    
    for i in range(len(str_list)):

        # L still refers to the same list; it's the contents that are changing
        L[i] = L[i].upper()
        
def get_valid_response(p, valid_list):
    ''' (str, list of strs) -> str
    Use p to prompt for and return a string that is from 
    valid_list.'''

    response = raw_input(p)
    
    while response not in valid_list:
        print 'Valid responses are:', valid_list
        response = raw_input(p)
    
    return response

if __name__ == '__main__':
    
    print get_valid_response("Test today? ", ['yes', 'no'])
    print get_valid_response('What would you like to do?', ['Play Again', 'Save', 'Quit'])
                    