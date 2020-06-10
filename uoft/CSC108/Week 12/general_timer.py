import time

# A bunch of nonsense functions whose run-times we can compare.

def one_loop(L):
    for i in range(len(L)):
        L[i] = L[i] + 1     
        
def two_loops(L):
    for i in range(len(L)):
        L[i] = L[i] + 1
        
    for i in range(len(L)):
        L[i] = L[i] + 1   
    
def nested_loop(L):
    for i in range(len(L)):
        for j in range(len(L)):
            L[i] = L[j] + 1
            
def nested_loop2(L):
    for i in range(len(L)):
        for j in range(30):
            L[i] = L[i] + j

def big_loop(L):
    sum = 0
    for i in range(10000):
        sum += L[0]
    return sum

def interesting(L):
    sum = 0
    i = len(L) - 1
    while i > 1:
        sum += L[i]
        i = i / 2
    return sum
    
def time_something(f):
    '''f is a function that takes a list as its only parameter.
    Call f on a series of progressively bigger lists and print how long
    it takes to run on each of them.'''
    
    num_sizes = 10
    increment = 1000
    for size in range(increment, (num_sizes + 1) * increment, increment):
        long_list = range(size)
        t1 = time.time()
        f(long_list)
        t2 = time.time()
        print "Size = %d and elapsed time = %.6f" % (size, t2 - t1)      
        
if __name__ == "__main__":
    
    functions = [one_loop, two_loops, nested_loop, nested_loop2, big_loop,
                 interesting]
    for f in functions:
        print "=== %s ===" % str(f)
        time_something(f)