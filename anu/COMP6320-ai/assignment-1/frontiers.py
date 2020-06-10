# frontiers.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course.

""" This file contains data structures useful for representing search frontiers
    for your depth-first, breadth-first, and a-star search algorithms (Q1-3).

    You do not have to use these, but it is strongly recommended.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import collections
import heapq


class Stack(object):
    """ A container with a last-in-first-out (LIFO) queuing policy."""

    def __init__(self):
        """ Make a new empty Stack.
            (Stack) -> None
        """
        self.contents = []

    def push(self, item):
        """ Push item onto the stack.
            (Stack, object) -> None
        """
        self.contents.append(item)

    def pop(self):
        """ Pop and return the most recently pushed item from the stack.
            (Stack) -> object
        """
        return self.contents.pop()

    def peek(self):
        """ Return the most recently pushed item from the stack.
            (Stack) -> object
        """
        return self.contents[-1]

    def is_empty(self):
        """ Returns True if the stack is empty and False otherwise.
            (Stack) -> bool
        """
        return not self.contents

    def find(self, f):
        """ Returns some item n from the queue such that f(n) == True and None
            if there is no such item.
            (Stack, (object) -> object/None) -> object
        """
        for elem in self.contents:
            if f(elem):
                return elem
        return None

    def __str__(self):
        """ Return a string representation of the Stack.
            (Stack) -> str
        """
        return str(self.contents)


class Queue(object):
    """ A container with a first-in-first-out (FIFO) queuing policy.

        Its contents are stored in a collections.deque. This allows constant
        time insertion and removal of elements at both ends -- whereas a list
        is constant time to add or remove elements at the end, but linear
        time at the head.
    """

    def __init__(self):
        """ Make a new empty Queue.
            (Queue) -> None
        """
        self.contents = collections.deque()

    def push(self, item):
        """ Enqueue the item into the queue
            (Queue, object) -> None
        """
        self.contents.append(item)

    def pop(self):
        """ Dequeue and return the earliest enqueued item still in the queue.
            (Queue) -> object
        """
        return self.contents.popleft()

    def peek(self):
        """ Return the earliest enqueued item still in the queue.
            (Queue) -> object
        """
        return self.contents[0]

    def is_empty(self):
        """ Returns True if the queue is empty and False otherwise.
            (Queue) -> bool
        """
        return not self.contents

    def find(self, f):
        """ Returns some item n from the queue such that f(n) == True and None
            if there is no such item.
            (Queue, (object) -> object/None) -> object
        """
        for elem in self.contents:
            if f(elem):
                return elem
        return None

    def __str__(self):
        """ Return a string representation of the queue.
            (Queue) -> str
        """
        return str(list(self.contents))


class PriorityQueue(object):
    """ This class implements a priority queue data structure. Each inserted item
        has a priority associated with it and we are usually interested in quick
        retrieval of the lowest-priority item in the queue. This data structure
        allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        """ Make a new empty priority queue.
            (PriorityQueue) -> None
        """
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        """ Enqueue an item to the priority queue with a given priority.
            (PriorityQueue, object, number) -> None
        """
        heapq.heappush(self.heap, (priority, self.count, item))
        self.count += 1

    def pop(self):
        """ Dequeue and return the item with the lowest priority, breaking ties
            in a FIFO order.
            (PriorityQueue) -> object
        """
        return heapq.heappop(self.heap)[2]

    def peek(self):
        """ Return the item with the lowest priority, breaking ties in a FIFO order.
            (PriorityQueue) -> object
        """
        return self.heap[0][2]

    def is_empty(self):
        """ Returns True if the queue is empty and False otherwise.
            (PriorityQueue) -> bool
        """
        return not self.heap

    def find(self, f):
        """ Returns some item n from the queue such that f(n) == True and None
            if there is no such item. Note that the parameter `f` is a function.

            (PriorityQueue, (object) -> object/None) -> object
        """
        for elem in self.heap:
            if f(elem[2]):
                return elem[2]
        return None

    def change_priority(self, item, priority):
        """ Change the priority of the given item to the specified value. If
            the item is not in the queue, a ValueError is raised.
            (PriorityQueue, object, int) -> None
        """
        for eid, elem in enumerate(self.heap):
            if elem[2] == item:
                self.heap[eid] = (priority, self.count, item)
                self.count += 1
                heapq.heapify(self.heap)
                return
        raise ValueError("Error: " + str(item) +
                         " is not in the PriorityQueue.")

    def __str__(self):
        """ Return a string representation of the queue. This will not be in
            order.
            (PriorityQueue) -> str
        """
        return str([x[2] for x in self.heap])


class PriorityQueueWithFunction(PriorityQueue):
    """ Implements a priority queue with the same push/pop signature of the
        Queue and the Stack classes. This is designed for drop-in replacement for
        those two classes. The caller has to provide a priority function, which
        extracts each item's priority.
    """

    def __init__(self, priority_function):
        """ Make a new priority queue with the given priority function.
            (PriorityQueueWithFunction, (object) -> number) -> None
        """
        super(PriorityQueueWithFunction, self).__init__()
        self.priority_function = priority_function

    def push(self, item):
        """" Adds an item to the queue with priority from the priority function.
            (PriorityQueueWithFunction, object) -> None
        """
        heapq.heappush(
            self.heap, (self.priority_function(item), self.count, item))
        self.count += 1
