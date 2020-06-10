'''A function for which we'll design test cases.'''

def insert_after(L, n1, n2):
    '''(list of ints, int, int) -> NoneType
    After each occurrence of n1 in L, insert n2.'''
    
    i = 0
    while i < len(L):
        if L[i] == n1:
            # Original version:
            #L = L[:i+1] + [n2] + L[i+1:]
            
            # Fixed version (modify L):
            L.insert(i + 1, n2)
            
            # Fixed version (skip over n2):
            i += 1
        i += 1
        
if __name__ == '__main__':
    L = [1, 2, 3]
    insert_after(L, 2, 2)