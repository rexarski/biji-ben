# Exercise 2, Tasks 1&2 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 2, Tasks 1&2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from vehicle import Car, HoverCar, NotEnoughFuelError


class TestCar(unittest.TestCase):

    def test_simple_car(self):
        car = Car(5, 1)
        car.move(3, 0)
        self.assertEqual(car.fuel, 2)
        self.assertEqual(car.pos_x, 3)
        self.assertEqual(car.pos_y, 0)
    
    def test_out_of_range(self):
        car = Car(5, 1)
        car.move(9999,9999)
        self.assertEqual(car.fuel, 5)
        self.assertEqual(car.pos_x, 0)
        self.assertEqual(car.pos_y, 0)
        self.assertRaises(NotEnoughFuelError, car.move(9999, 9999))

class TestHoverCar(unittest.TestCase):

    def test_simple_move_hover(self):
        hover_car = HoverCar(5, 1, 1)
        hover_car.move(10, 10)
        self.assertEqual(hover_car.fuel, 5)
        self.assertEqual(hover_car.hover_fuel, 0)  # NOTE: rounded down
        self.assertEqual(hover_car.pos_x, 10)
        self.assertEqual(hover_car.pos_y, 10)
    
    def test_hover_very_close(self):
        hover_car = HoverCar(5, 1, 1)
        hover_car.move(1, 1)
        self.assertEqual(hover_car.fuel, 3)
        self.assertEqual(hover_car.hover_fuel, 1)
        self.assertEqual(hover_car.pos_x, 1)
        self.assertEqual(hover_car.pos_y, 1)
    
    def test_too_far(self):
        hover_car = HoverCar(5, 1, 1)
        hover_car.move(1000, 1000)
        self.assertEqual(hover_car.fuel, 5)
        self.assertEqual(hover_car.hover_fuel, 1)
        self.assertEqual(hover_car.pos_x, 0)
        self.assertEqual(hover_car.pos_y, 0)
        self.assertRaises(NotEnoughFuelError, hover_car.move(1000, 1000)) # similar problem here
        
if __name__ == '__main__':
    unittest.main(exit=False)
