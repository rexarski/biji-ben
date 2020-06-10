# Lab 2 TESTS
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Lab 2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from pvd import Pokemon, Digimon


class TestPVD(unittest.TestCase):
    
    def setUp(self):
        self.charm = Pokemon('Charmander', 'fire')
        self.agumon = Digimon('Agumon')
        self.bulb = Pokemon('Bulbasaur', 'grass')
        
    def test_start_pokemon_health(self):
        self.assertEqual(self.charm.health, 50)

    def test_pokemon_attack_Digimon_once(self):
        self.charm.attack(self.agumon)
        # Note that this test makes use of the "health" attribute,
        # which was part of our design in the starter code.
        # You may or may not need to modify this, depending on your design!
        self.assertEqual(self.agumon.health, 20)
    
    def test_digimon_attack_Pokemon_once(self):
        self.agumon.attack(self.charm)
        self.assertEqual(self.charm.health, 35)
        
    def test_weakness_pokemon_attack(self):
        self.charm.attack(self.bulb)
        self.assertEqual(self.bulb.health, 10)
        # Because the attack should do 40 (50 - 40 = 10)
        
    def test_digimon_charge(self):
        self.agumon.charge()
        self.agumon.attack(self.agumon)
        self.assertEqual(self.agumon.health, 10)
        
    def test_dead_digimon(self):
        self.agumon.health = 1
        self.agumon.attack(self.agumon)
        #assumes self.agumon.dead is even a thing
        self.assertEqual(self.agumon.dead, True)

if __name__ == '__main__':
    unittest.main(exit=False)
