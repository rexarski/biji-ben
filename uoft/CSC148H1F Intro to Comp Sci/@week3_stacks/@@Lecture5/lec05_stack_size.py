from stack import Stack

def size(stack):
    """(Stack) -> int
    Return the number of items in stack.
    You can change the stack however you like.
    """
    count = 0
    while stack.is_empty() == False:
        stack.pop()
        count += 1
    return count
    #num = 0
    #while True:
        #try:
            #stack.pop()
            #num = num + 1
        #except ???:
            #pass
        #return num # you have to add errors for this!

def size2(stack):
    """(Stack) -> int
    Return the number of items in the stack.
    When the function finishes, stack must be unchanged.
    """
    #1. store items in a list
    #2. store items in a stack (we're gonna do this)
    #3. create a copy of the origianl stack (see below)
    
    num = 0
    temp_stack = Stack()
    while not stack.is_empty():
        x = stack.pop()
        temp_stack.push(x)
        num += 1
    
    # Restore original stack
    # While not temp_stack.is_empty()
    for i in range(num):
        x = temp_stack.pop()
        stack.push(x)
    return num

    #copy = stack
    #count = 0
    #while stack.is_empty() == False:
        #stack.pop()
        #count += 1
    #stack = copy
    #return count # this is method 3

