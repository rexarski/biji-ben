# Exercise 2: Cars and Hover Cars
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your information below, in format
# <full name>, <utorid>
# <Rui Qiu>, <999292509>
# ---------------------------------------------
import math


class NotEnoughFuelError(Exception):
    
    def __init__(self):
        """(NotEnoughFuelError) -> NoneType
        Create a new NotEnoughFuelError with the given information about a car.
        """
        
        pass
    
    def __str__(self):
        """(NotEnoughFuelError) -> NoneType
        Return a string representation of the error.
        """
        
        return "You need to go to gas station!"

class Car:

    # Don't change this code!
    def __init__(self, fuel, efficiency):
        """ (Car, int, int) -> NoneType

        fuel is an int specifying the starting amount of fuel.
        efficiency is an int specifying how much fuel the car takes
        to travel 1 unit of distance.

        Initialize a new car with an amount of fuel and a fuel efficiency.
        The car's starting position is (0,0).
        """

        self.fuel = fuel
        self.efficiency = efficiency
        self.pos_x = 0
        self.pos_y = 0

    def move(self, new_x, new_y):
        """ (Car, int, int) -> NoneType

        Move the car from its old position to (new_x, new_y).
        Reduce the car's fuel depending on its efficiency and how far it
        travelled.

        If there isn't enough fuel to reach (new_x, new_y),
        do not change car's position or fuel level.
        Instead, raise NotEnoughFuelError.

        Remember that the car can only travel horizontally and vertically!
        """

        max_distance = int(self.fuel / self.efficiency)
        planned_distance = abs(new_x - self.pos_x) + abs(new_y - self.pos_y)
        if max_distance >= planned_distance:
            self.pos_x = new_x
            self.pos_y = new_y
            self.fuel -= planned_distance * self.efficiency
        else:
            raise NotEnoughFuelError

class HoverCar(Car):

    def __init__(self, fuel, efficiency, hover_fuel):
        """ (HoverCar, int, int, int) -> NoneType

        hover_fuel is an int specifying the starting amount of hover fuel.

        Initialize a new HoverCar.
        """
        Car.__init__(self, fuel, efficiency)
        self.hover_fuel = hover_fuel

    def move(self, new_x, new_y):
        """ (HoverCar, int, int)

        Move the hover car according to the description in the exercise.
        Remember that hover cars try using regular fuel first,
        and only use hover fuel if there isn't enough regular fuel.

        Be sure to follow the implementation guidelines for full marks!
        """
        
        planned_distance = abs(new_x - self.pos_x) + abs(new_y - self.pos_y)
        planned_diagonal_distance = math.sqrt(abs(new_x) ** 2 + abs(new_y) ** 2)
        fuel_distance = self.fuel / self.efficiency
        hover_distance = self.hover_fuel * 20
        try:
            Car.move(self, new_x, new_y)
        except:
            if planned_distance > fuel_distance:
                if planned_diagonal_distance > hover_distance:
                    raise NotEnoughFuelError
                else:
                    self.pos_x = new_x
                    self.pos_y = new_y
                    self.hover_fuel = math.floor(self.hover_fuel - planned_diagonal_distance / 20)