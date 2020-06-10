def foo(x):
    y = x + 1
    z = y + x
    return z

def qStarter(word):
    return word.startswith('q') or word.startswith('Q')

def newQStarter(word):
    response.lower(word).startswith('q')

def TemperatureConverter(F):
    return '{:.2f}'.format((5 / 9) * (F - 32))

def SolTemperatureConverter():
    fahrenheit = float(input('Plesase enter the temperature you wanna convert (F): '))
    celsius = (5 / 9) * (fahrenheit - 32)
    print ('The temperature is {:.2f} C'.format(celsius))

def rangetrial(number):
    for i in range(number):
        print (i)
    
def TimesTable():
#    table = []
#    for i in range(n):
#        row = []
#        for j in range(n):
#            row.append(i * j)
#        table.append(row)
#    return (table)
# THIS SHOULD HAVE BEEN WORKING
    
    table = [[row * col for row in range(10)] for col in range(10)]
    return (table)

def dosomething(number):
    for index in range(number):
        if number == 2:
            break
        if number == 3:
            pass
        else:
            print(number)
        return None

def is_reverse_pair(s1, s2):
    for i in range(len(s1)):
        if s1[i-1] != s2[-i]:
            return False
    return True
    #return s1[::-1] == s2 ##a better version

def print_reverse_pairs(wordlist):
    for w1 in wordlist:
        for w2 in wordlist:
            if is_reverse_pair(w1, w2) == True:
                print (w1, w2)
                wordlist.remove(w1)
                wordlist.remove(w2)

with open('dog.txt', 'w') as open_file:
    print ('doggydog\nwoof', file=open_file)
import os
os.getcwd()
with open('dog.txt') as open_file:
    for line in open_file:
        print (line)

dic = {1234: 'Tony Stark', 1138: 'Steve Rogers'}

def print_record(dic):
    for key in dic:
        print (dic[key], '#' + str(key))

def count_occurrences(file):
    '''file -> dic'''
    counts = {}
    for line in file:
        for word in line.split:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts

def Guess():
    from random import randint
    answer = randint(0, 100)
    
    guess = 0
    while guess != answer:
          print ('Guess a number between 0 and 100: ')
          guess = int(input())
          if guess >= 0 and guess <= 100:
              if guess > answer:
                  print ('Too high.')
              elif guess < answer:
                  print ('Too low.')
              else:
                  print ('Correct! Thanks for playing!')

class Point:
    '''A new Point'''
    def __init__ (self, x = 0, y = 0):
        '''(Point, int, int) -> NoneType'''
        self.x = x
        self.y = y

position = Point(0, 0)
position.x += 5
position.y -= 2
print ((position.x, position.y))

def translate(self, dx, dy):
    '''(Point, int, int) -> NoneType'''
    self.x = dx
    self.y = dy

position = Point(0, 0)
position.translate(dy = -2, dx = 5)
print((position.x, position.y))

class Drinks:
    def __init__ (self, name, drink):
        self.name = name
        self.name = drink
    
class Fridge:
    def __init__ (self, drinkslist):
        self.drinkslist = drinkslist 
    
class DrinksTestCase(unittest.TestCase):
    def test_is_fridge_full(self):
        F = Fridge(sdafasdsf)
        Drink1 = Drink(hahaha)
        Drink2 = repeat
        Drink3 = repeat
        F.putin(Drink1)
        F.putin(Drink2)
        F.putin(Drink3)
        self.assertTrue(is_full(Fridge))
        
    def test_what_happens_if_we_take_one_out:
        F.takeout(pop)
        
    def test_is_there_three_drinks:
        
        