# Lab 2 - Pokemon vs. Digimon
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Lab 2: Pokemon vs. Digimon.

This module contains stub classes for Pokemon and Digimon.
Make sure you understand the inheritance relationships
between the three classes, and then start implementing methods!
"""


class Creature:
    """Base creature class.

    This class is an abstract class, meaning it isn't meant to be
    used directly. It serves as a base class for both Pokemon and Digimon.
    
    Attributes:
    - name (str): the name of the Creature
    - health (int): the amount of health of the Creature. Cannot go below 0.
    """

    def __init__(self, name):
        """ (Creature, str, int) -> NoneType
        Create a new Creature with the given name and amount of health.
        """
        self.name = name
        self.health = 100

    def roar(self):
        """ (Creature) -> str
        Return a string representing this Creature's roar.
        """
        roar = 'I am a creature, fear my attack!'
        print (roar)

    def attack(self, enemy):
        self.roar()
        attack_damage = 10
        if self.health == 0:
            attack_damage = 0
        self.take_damage(enemy, attack_damage)

    def take_damage(self, damage):
        """ (Creature, int) -> NoneType
        Reduce this Creature's health by damage, to a minimum of 0.
        Call self.faint if health reaches 0.
        """
        self.health -= damage
        
        #It's dead
        if self.health <= 0:
            self.health = 0
            self.faint()
    
    def faint(self):
        """ (Creature) -> NoneType
        Make this Creature unable to take actions.
        Called when this Creature's health reaches 0.
        """
        self.dead = True
        print ('I\'m dying, that is sad')
        # How do we make this thing incapable of taking actions?

class Pokemon(Creature):
    """Pokemon class.
    
    Non-Inherited Attributes:
    - type (str): either 'grass', 'fire', or 'water', indicating Pokemon's type
    """
    def __init__(self, name, type_p):
        """ (Pokemon, str, str) -> NoneType
        Create a new Pokemon with the given name and type.
        """
        Creature.__init__(self, name)
        #pokemons have 50 health
        self.health = 50
        self.type_p = type_p

    # Overridden methods
    def roar(self):
        print(self.name + ' ' + self.name + '!')
        
    def weakness_manager(self, attack_type, defend_type):
        '''Grass is weak to water, water weak to grass, fire weak to water.'''
        if attack_type == 'grass':
            if defend_type == 'water':
                print ("Attack was super effective")
                return 40
        elif attack_type == 'fire':
            if defend_type == 'grass':
                print ("Attack was super effective")
                return 40
        elif attack_type == 'water':
            if defend_type == 'fire':
                print ("Attack was super effective")
                return 40
        return 20
    
    def attack(self, enemy):
        self.roar()
        if isinstance(enemy, Pokemon):
            attack_damage = self.weakness_manager(self.type_p, enemy.type_p)
        else:
            attack_damage = 20
        self.charging = False
        if self.health == 0:
            attack_damage = 0        
        enemy.take_damage(attack_damage)

class Digimon(Creature):
    """Digimon class.
    
    Non-Inherited Attributes:
    - charging (bool): whether this Digimon is charging for its next attack
    """    
    def __init__(self, name):
        """ (Digimon, str) -> NoneType
        Create a new Pokemon with the given name.
        """        
        Creature.__init__(self, name)
        self.health = 40
        self.charging = False

    # Overridden methods
    def roar(self):
        print('Digimon {} awaiting command!'.format(self.name))

    def attack(self, enemy):
        self.roar()
        if self.charging:
            attack_damage = 30
        else:
            attack_damage = 15
        
        if self.health == 0:
            attack_damage = 0        
        enemy.take_damage(attack_damage)
        
    # New method
    def charge(self):
        """ (Digimon) -> NoneType
        Save energy, making this Digimon's next attack deal double damage.
        """
        self.charging = True

class Hybridmon(Digimon, Pokemon):
    def __init__(self, name, type_p):
        Pokemon.__init__(self, name, type_p)
        Digimon.__init__(self, name)