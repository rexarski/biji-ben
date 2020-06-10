'''This module contains Python functions corresponding to the hints
given to the "poisonous potions" problem in CSC108/A08 booleans
lab.'''

def hint1(p1, p2, p3, p4):
    '''(bool, bool, bool, bool) -> bool
    Return True if at least one of p1, p2, p3, or p4 is True. Return False otherwise.'''

    return p1 or p2 or p3 or p4

def solution(p1, p2, p3, p4):
    '''(bool, bool, bool, bool) -> bool
    Return True if the values p1, p2, p3, and p4 are such that when they are passed to the hint functions in this module, all five functions return True. Return False otherwise.'''
    
    h1 = hint1(p1, p2, p3, p4)
    h2 = hint2(p2)
    h3 = hint3(p1, p3)
    h4 = hint4(p3, p4)
    h5 = hint5(p1, p3, p4)
    return h1 and h2 and h3 and h4 and h5

def make_bool(s):
    '''(str) -> bool
    Return the bool equivalent of s.  If s is not recognizable
    as a bool, return False.'''
    
    # make a lowercase version of s so there will be fewer comparisons to make.
    converted = s.lower()
    return converted == "true" or converted == "t"

if __name__ == "__main__":
    
    print "Tell me your hypothesis!"
    print "For each question, type true or false"
    guess1 = make_bool(raw_input("Is potion 1 poisonous? "))
    guess2 = make_bool(raw_input("Is potion 2 poisonous? "))
    guess3 = make_bool(raw_input("Is potion 3 poisonous? "))
    guess4 = make_bool(raw_input("Is potion 4 poisonous? "))
    if solution(guess1, guess2, guess3, guess4):
        print "You're right!"
    else:
        print "Sorry, your hypothesis is not correct."
