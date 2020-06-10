def num_vowels(s):
    '''(str) -> int
    Return the number of vowels in s. Do not treat the
    letter "y" as a vowel.'''
    
    count_vowels = 0
    for char in s:
        if char in 'aeiouAEIOU':
            count_vowels += 1
    return count_vowels        

def reverse(s):
    '''(str) -> str
    Return a new string that is s in reverse.'''
    
    pass

def remove_spaces(s):
    '''(str) -> str
    Return a new string that is the same as s but with any blanks
    removed.'''

    pass

def num_matches(s1, s2):
    '''(str, str) -> int
    Return the number of characters in s1 that appear in s2.'''
   
    pass