def our_max(num1, num2):
    '''(number, number) -> number
    Return the larger of the numbers num1 and num2.'''
    
    max = num1
    if num2 > num1:
        max = num2
    return num2

def same_string(str1, str2):
    '''(str, str) -> bool
    Return True if strings str1 and str2 have the same contents ignoring case,
    and return False otherwise.'''
    
    return str1.lower() == str2.lower()