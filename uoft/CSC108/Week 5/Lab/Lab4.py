s = 'supercalifragilisticexpialidocious'
#for c in s:
    #print c

#for c in s:
    #print c,

#for c in s:
    #print c + ' ,',

#for c in s:
    #print c +',',

def longer(s1, s2):
    '''(str, str) -> int
    Given two strings, return the length of the longer string.'''

    return max(len(s1), len(s2))


def earlier(s1, s2):
    '''(str, str) -> str'''
    
    return min(s1, s2)


def count_letter(s1, s2):
    '''(str, str) -> int'''
    
    count = 0
    for char in s1:
        if char == s2:
            count += 1
    return count

def display_character(s1, s2):
    '''(str, str) -> str'''
    count = 0
    for char in s1:
        if char == s2:
            count += 1
    return s2 * count


def where(s1, s2):
    '''(str, str) -> int'''
    
    count = 0
    if s2 in s1:
        for char in s1:
            if char != s2:
                count += 1
            else:
                return count
    else:
        return -1

#s.endswith('h')


#s.isdigits()


#s.replace('l', '1')


#s.zill(6)


#s.islower()


#s.lstrip('0')



