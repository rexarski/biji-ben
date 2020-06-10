class NegativeAgeError(Exception):
    pass

class Person:
    def __init__(self, name, age):
        '''(Person, str, int) -> NoneType
        Create a new person with the given name and age.
        Age should be a non-negative integer!'''
        
#        One way which is not very great, write:
#        if age < 0:
#            self.age = None
#        else:
#            self.age = age
        self.name = name
        if age == -4:
            1 / 0
        if age < 0:
            raise NegativeAgeError
        else:
            self. age = age
        
def make_person(age):
    try:
        p = Person('david', age)
    except NegativeAgeError:
        print ('Invalid age:(')
        p = None
    except ZeroDivisionError:   #you can have multiple except, just like multiple if
        print('divided by 0 :(')
        p = None
        
    return p