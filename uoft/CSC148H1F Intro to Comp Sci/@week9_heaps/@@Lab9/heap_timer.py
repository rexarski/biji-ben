from heap import Heap, build_heap_1, build_heap_2
from timer import Timer
import random

if __name__ == '__main__':
    # 1. Create a very large list containing 10000000 numbers
    # (Use the functions range() and list() here)
    my_list = list(range(10000000))

    # 2. Use random.shuffle to randomly permute the list
    # (Check the documentation here:
    #    https://docs.python.org/3.4/library/random.html#examples-and-recipes)
    # random.shuffle(my_list)
    # my_list.reverse()

    # 3. Using Timer, check how long it takes to build a heap out of your
    # random permutation for the two different algorithms.
    # Remember that the syntax for using Timer is
    # with Timer('hello'):
    #    f()
    #    g()
    with Timer('Algorithm 1'):
        build_heap_1(my_list)
    my_list.insert(0, None)
    with Timer('Algorithm 2'):
        build_heap_2(my_list)


    # Repeat this experiment a few times with different random lists
    # (and try different sizes, too).

    # 4. When you're done, try replacing the random list with a sorted list in
    # descending order, and the one in ascending order.
    # (Warning: the latter will take a long time, why?)
