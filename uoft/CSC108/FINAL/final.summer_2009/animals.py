class Animal(object):

  def __init__ (self, name):
    '''Create a new animal named name.'''
      
    self.name = name
    
  def __str__ (self):
    '''Return a string representation of this animal.'''
    
    return 'Animal: (' + self.name + ')'
    
class Dog(Animal):
    
  def speak(self):
    '''Make a doggie noise.'''
    
    print 'Woof woof!'
    