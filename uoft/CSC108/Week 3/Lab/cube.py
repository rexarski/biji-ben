def cube(x):
    '''(number) -> number
    Return the cube of x.'''
    
    return x * x * x

def print_cube(x):
    '''(number) -> NoneType
    Print the cube of x.'''
    
    print x * x * x
    
if __name__ == "__main__":
    print "Testing cube()"
    x_cubed = cube(3)
    print "The cube of 3 is", x_cubed
    
    print "Testing print_cube()"
    x_cubed = print_cube(3)
    print "The cube of 3 is", x_cubed