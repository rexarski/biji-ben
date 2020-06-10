class NegativeAgeError(Exception):
    def __init__(self, age):
        """(NegativeAgeError, int) -> NoneType
        Create a new NegativeAgeError with the given (bad) age.
        """
        
        self.age = age
       
    def __str__(self):
        """(NegativeAgeError) - str
        Return a string representation of the error.
        """
        
        return 'Tried to create a Person with negative age {0}'.format(self.age)
    
class Person:
    def __init__(self, name, age):
        if age < 0:
            raise NegativeAgeError(age) #why this does not work?
        else:
            self.name = name
            self.age = age

#class NegativeAgeError(Exception):
    #pass

#class Person:
    #def __init__(self, name, age):
        #if age < 0:
            #raise NegativeAgeError(Exception)
        #else:
            #self.name = name
            #self.age = age
    
    #def safe_neg_person(n):
        #try:
            #x = Person('Janus', n)
            #print('Successfully created a Person!')
        #except NegativeAgeError:
            #print('You tried to create a negative-age Person. Shame on you!')
        #except TypeError:
            #print ('You need to pass in a numeric argument.')
        #else:
            #print('Successfully created a Person with age ' + n)
        #finally:
            #print('This always prints, even if an unexpected error occurs.')
        
        #print('Program continues safely, even if a NegativeAgeError was raised.')
        
        