# Exercise 9 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 9 TESTS.

Note: all tests provided here. In future weeks,
only a subset of the tests will be provided,
and you'll be encouraged to write your own.
"""
import unittest
from wuheap import Heap, heapsort


class TestIsHeap(unittest.TestCase):

    def test_simple_heap(self):
        heap = Heap()
        heap.items = [None, 3, 1, 2]
        self.assertTrue(heap.is_heap())

    def test_simple_not_heap(self):
        heap = Heap()
        heap.items = [None, 1, 2, 3]
        self.assertFalse(heap.is_heap())
    
    def test_long_heap(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 2, 1, 3, 4, 1]
        self.assertTrue(heap.is_heap())
        
    def test_long_not_heap(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 3, 1, 3, 4, 1]
        self.assertFalse(heap.is_heap())
        self.assertFalse(heap.is_heap(2))
        self.assertTrue(heap.is_heap(4))
    
    def test_complex_not_heap(self):
        heap = Heap()
        heap.items = [None, 10, 5, 8, 3, 5, 6, 7, 3, 0, 5, 6]
        self.assertFalse(heap.is_heap())
        self.assertFalse(heap.is_heap(2))
        #self.assertTrue(heap.is_heap(4)) yours not working here
        self.assertFalse(heap.is_heap(5))
        self.assertTrue(heap.is_heap(8))
        
    def test_complex_not_heap_long(self):
        heap = Heap()
        heap.items = [None, 10, 5, 8, 3, 5, 6, 7, 3, 0, 5, 3, 6, 6, 1, 1, 1, 9]
        self.assertFalse(heap.is_heap())
        self.assertFalse(heap.is_heap(2))


class TestHeapSort(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(heapsort([1, 3, 2]), [3, 2, 1])
    
    def test_sort_long(self):
        self.assertEqual(heapsort([1, 1, 2, 3, 3, 4, 5, 6]), [6, 5, 4, 3, 3, 2, 1, 1])


if __name__ == '__main__':
    unittest.main(exit=False)
