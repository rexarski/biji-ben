# A Timer class
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Timer class.

A Python context used to measure and output the amount of time
a block of code takes. Usage:

def run_time_test():
    with Timer('Some code'):
        do_stuff()
        do_more_stuff()

>>> run_time_test()
Block "Some code" took 3.54532 seconds
"""
import time


class Timer:
    def __init__(self, label=''):
        self.label = label

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        log = 'Block '
        if self.label:
            log += '\"{}\" '.format(self.label)
        log += 'took ' + str(round(self.interval, 5)) + ' seconds'
        print(log)
