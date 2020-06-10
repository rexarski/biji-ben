class Person:
    
    def  __init__(self, name, age, food):
        """(Person, string, int, string) -> NoneType
        Create new Person object with given, name, age, and favourite foood.
        """
        self.name = name
        self.age = age
        self.favourite_food = food
        self.mood = 'Happy'
    
    def eat(self, food):
        """Person, string) -> NoneType
        
        Make this person eat the food. Change the mood of this person if food
        is the same as this person's favourite food.
        """
        
        if self.favourite_food == food:
            self.mood = 'ecstatic'
            print('Ah, this is my favourite!')
            