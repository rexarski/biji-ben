def f():
    x = g()
    y = h()
    return x + y

def g():
    k()
    return 3

def h():
    return 5

def k():
    return 10