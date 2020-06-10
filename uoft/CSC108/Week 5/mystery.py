def mystery(s):
    '''(str) -> int
    Return the index of the first digit in s, or the 
    length of s if there are no digits in s.
    '''
    
    i = 0
    while i < len(s) and s[i] not in "0123456789":
        i += 1   
    return i

if __name__ == '__main__':
    
    # first digit at front, at neither extreme, at end
    # string size 0, 1, bigger
    # no digit in the string
    
    
    print mystery('potato')
    print mystery('911')
    print mystery('a4b')
    print mystery('ab5')
    print mystery('a')
    print mystery('9')
    print mystery('')
            