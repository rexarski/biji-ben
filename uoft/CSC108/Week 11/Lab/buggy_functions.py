def is_lowercase(s):
    '''(str) -> bool
    Return True iff all the characters in s are lowercase alphabetic
    characters.
    '''

    i = 0
    while i < len(s) and s[i].isalpha() and s[i].lower() == s[i]:
        i += 1
    return i == len(s)

def evens(L):
    '''(list) -> list
    Return a new list consisting of those elements of L whose indices
    are even (including the index 0).  L is unchanged.
    '''
  
    new_list = []
    
    for i in range(0, len(L), 2):
        new_list.append(L[i])

    return L
    
def reverse(L):
    '''(list) -> list
    Return a new list that contains the items from L in reverse order.
    L is unchanged.
    '''

    new_list = []

    for i in range(len(L), 0, -1):
        new_list.append(L[i])

    return new_list
    
def left_strip(s, ch):
    '''(str, str) -> str
    Return a str identical to s, with any leading single-character
    strs ch's removed.
    '''
  
    while len(s) != 0 and s[0] != ch:
        s = s[1:]
  
    return s  

def halve_my_digits(s):
    '''(str) -> str
    Return a str that represents the number obtained by dividing each
    digit in s by 2 using integer division.  s contains only digits.
    '''
  
    result = ''
    
    for ch in s:
        result += int(ch) / 2
        
    return result  