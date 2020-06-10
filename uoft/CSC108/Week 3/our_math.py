def add(x, y):
    '''(number, number) -> number
    Return the sum of x and y.'''
    
    return x + y

def square(x):
    '''(number) -> number
    Return x squared.'''
    
    return x ** 2

# When calculations.py imports our_math, this code is executed!
print square(add(34, 23.9))
sum = add(23.5, 34)
print square(sum / 3)