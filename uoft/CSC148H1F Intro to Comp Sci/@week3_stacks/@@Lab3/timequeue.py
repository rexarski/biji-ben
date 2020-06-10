"""Lab 3 - Timing experiments with Queue.

Authors: David Liu, September 2014
"""
from queue import Queue
from timer import Timer

class EmptyStackError(Exception):
    """Exception used when calling pop on empty stack."""
    pass


class Stack:

    def __init__(self):
        """ (Stack) -> NoneType """
        self.items = []

    def is_empty(self):
        """ (Stack) -> bool """
        return len(self.items) == 0

    def push(self, item):
        """ (Stack, object) -> NoneType """
        self.items.append(item)

    def pop(self):
        """ (Stack) -> object """
        try:
            return self.items.pop()
        except IndexError:
            raise EmptyStackError
    
def create_big_queue(n):
    """ (int) -> Queue

    Create a queue with n elements.
    """
    queue = Queue()
    for i in range(n):
        queue.enqueue(i)
    return queue

def create_big_stack(n):
    stack = Stack()
    for i in range(n):
        stack.push(i)
    return stack

def compare_time(n):
    
    with Timer('queue'):
        queue = create_big_queue(n)
    
    with Timer('dequeue'):   # time of processing this step is not linear. it's inefficient to add/remove items from the beginning, so we need to change to adding/removing items from the end.
        while not queue.is_empty():
            queue.dequeue()
    
    with Timer('stack'):
        stack = create_big_stack(n)
    
    with Timer('pop stack'):
        while not stack.is_empty():
            stack.pop()
    

#if __name__ == '__main__':
    ## Try creating queues of different sizes, and timing
    ## how long it takes to create them.
    ## for n in range(...): <- try multiples of 10000
    ##     create a queue of size n
    ## Then, try creating queues of different sizes, and time
    ## how long it takes to enqueue and dequeue ~100 items.
    
    ##compare_time(100000)
    ##Block "queue" took 0.06372 seconds
    ##Block "dequeue" took 1.95284 seconds
    ##Block "stack" took 0.0333 seconds
    ##Block "pop stack" took 0.06148 seconds
    ##compare_time(200000)
    ##Block "queue" took 0.1214 seconds
    ##Block "dequeue" took 7.96663 seconds
    ##Block "stack" took 0.06987 seconds
    ##Block "pop stack" took 0.12574 seconds
    ##compare_time(400000)
    ##Block "queue" took 0.2487 seconds
    ##Block "dequeue" took 32.27533 seconds
    ##Block "stack" took 0.13502 seconds
    ##Block "pop stack" took 0.24429 seconds 
    
    ##dequeue goes up at the rate of power of 2.
