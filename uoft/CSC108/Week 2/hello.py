def say_hello():
    name = raw_input("What is your name? ")
    print "Hello " + name
    
def say_hello2():
    name = raw_input("What is your name? ")
    return "Hello " + name

say_hello()
say_hello2()