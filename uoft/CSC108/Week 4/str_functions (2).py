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
    
    rev = ''
    for char in s:
        rev = char + rev
        
    return rev

def remove_spaces(s):
    '''(str) -> str
    Return a new string that is the same as s but with
    any blanks removed.'''

    new_str = ''   # accumulator
    
    for char in s:
        if char != ' ':
            new_str += char   # new_str = new_str + char
    return new_str

def num_matches(s1, s2):
    '''(str, str) -> int
    Return the number of characters in s1 that appear in s2.'''
   
    count = 0
    for char in s1:
        if char in s2:
            count += 1
    return count

if __name__ == '__main__':
    remove_spaces("Hi there")