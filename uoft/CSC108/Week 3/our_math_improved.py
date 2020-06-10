def add(x, y):
    '''(number, number) -> number
    Return the sum of x and y.'''
    
    return x + y

def square(x):
    '''(number) -> number
    Return x squared.'''
    
    return x ** 2

# If this is the very module being run, do the code
# below.  But if it's just being imported, don't!
# When calculations_improved imports our_math_improved, the code
# in the body of the if-statement is not executed.
if __name__ == '__main__':
    print square(add(34, 23.9))
    sum = add(23.5, 34)
    print square(sum / 3)