# Lab 3 - Queues
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------


class EmptyQueueError(Exception):
    """Error raised when trying to dequeue from an empty queue."""
    pass


class Queue:
    """Queue class.
    A class implementing the Queue ADT, using a list.

    Attributes:
    - ???
    """

    def __init__(self):
        """ (Queue) -> NoneType
        Create an empty queue.
        """
        self.items =[]

    def is_empty(self):
        """ (Queue) -> bool
        Return True if the queue is empty.
        """
        return len(self.items) == 0

    def enqueue(self, item):
        """ (Queue, object) -> NoneType
        Add item to the back of the queue.
        """
        self.items.insert(len(self.items), item)

    def dequeue(self):
        """ (Queue) -> object
        Remove and return the front item, if there is one.
        Raise EmptyQueueError if the list is empty.
        """
        if self.is_empty():
            raise EmptyQueueError
        else:
            a = self.items[0]
            self.items.remove(self.items[0])
            return a

def product(queue):
    """ (Queue of number) -> number

    Return the product of all numbers in queue.
    Return 1 if queue is empty.
    You may change queue (and in particular, remove all its items).

    Although as a bonus, try *not* changing the queue!
    """
    product = 1
    temp = Queue()
    
    while not queue.is_empty():
        temp.enqueue(queue.dequeue())
        
    while not temp.is_empty():
        element = temp.dequeue()
        queue.enqueue(element)
        product *= element
        
    return product