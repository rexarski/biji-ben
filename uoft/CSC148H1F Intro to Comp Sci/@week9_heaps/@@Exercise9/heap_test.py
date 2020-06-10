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
from heap import Heap, heapsort


class TestIsHeap(unittest.TestCase):

    def test_simple_heap(self):
        heap = Heap()
        heap.items = [None, 3, 1, 2]
        self.assertTrue(heap.is_heap())

    def test_simple_not_heap(self):
        heap = Heap()
        heap.items = [None, 1, 2, 3]
        self.assertFalse(heap.is_heap())
    
    def test_complex_heap(self):
        heap = Heap()
        heap.items = [None, 10, 5, 8, 3, 5, 6, 7, 3, 0, 5, 3, 6, 6, 1, 1]
        self.assertTrue(heap.is_heap())
        self.assertTrue(heap.is_heap(4))
        self.assertTrue(heap.is_heap(3))
    
    def test_complex_not_heap(self):
        heap = Heap()
        heap.items = [None, 10, 5, 8, 3, 5, 6, 7, 3, 0, 5, 6, 6, 6, 1, 1]
        self.assertFalse(heap.is_heap())
        self.assertFalse(heap.is_heap(2))
        self.assertTrue(heap.is_heap(4))
        self.assertFalse(heap.is_heap(5))
        self.assertTrue(heap.is_heap(8))
    
    def test_complex_not_heap_long(self):
        heap = Heap()
        heap.items = [None, 10, 5, 8, 3, 5, 6, 7, 3, 0, 5, 3, 6, 6, 1, 1, 1, 9]
        self.assertFalse(heap.is_heap())
        self.assertFalse(heap.is_heap(2))
    
    def test1(self):
        heap = Heap()
        heap.items = [None, 6]
        self.assertTrue(heap.is_heap())
        
    def test2(self):
        heap = Heap()
        heap.items = [None, 6, 3]
        self.assertTrue(heap.is_heap())
        
    def test3(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5]
        self.assertTrue(heap.is_heap())  
        
    def test4(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 2]
        self.assertTrue(heap.is_heap())
        
    def test5(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 2, 1]
        self.assertTrue(heap.is_heap())        
    
    def test6(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 2, 1, 3]
        self.assertTrue(heap.is_heap())
        
    def test7(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 2, 1, 3, 4]
        self.assertTrue(heap.is_heap())         
    
    def test8(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 2, 1, 3, 4, 1]
        self.assertTrue(heap.is_heap())
        
    def test_long_not_heap(self):
        heap = Heap()
        heap.items = [None, 6, 3, 5, 3, 1, 3, 4, 1]
        self.assertTrue(heap.is_heap())
        self.assertTrue(heap.is_heap(2))
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
    
    def test_complex(self):
        self.assertEqual(heapsort([1, 2, 3, 4]), [4, 3, 2, 1])
    
    def test_complex2(self):
        self.assertEqual(heapsort([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])
        
    def test_complex3(self):
        self.assertEqual(heapsort([21, 21, 20, 9, 24, 30]), [30, 24, 21, 21, 20, 9])
        self.assertEqual(heapsort([5, 5, 3, 3, 11, 11]), [11, 11, 5, 5, 3, 3])
    
    def test_complex4(self):
        self.assertEqual(heapsort([1]), [1])
        self.assertEqual(heapsort([1, 1]), [1, 1])
        self.assertEqual(heapsort([1, 2]), [2, 1])
        self.assertEqual(heapsort([]), [])
        self.assertEqual(heapsort([1, 3, 3, 2, 9, 2, 4]), [9, 4, 3, 3, 2, 2, 1])

if __name__ == '__main__':
    unittest.main(exit=False)
