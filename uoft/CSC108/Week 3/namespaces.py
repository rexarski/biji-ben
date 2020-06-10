def f(x):
    x = 7
    return x ** 2

def g(x):
    return x * (x + 1) /2

# The program has three different x's: f's, g's x and the global x.
# Trace code with debugger and see how Python keeps track of them 
# in namespaces (Stack Data tab).
x = 13
y = f(x)
z = g(x)
print x, y, z