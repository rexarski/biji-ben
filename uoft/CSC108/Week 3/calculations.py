import our_math

def average(grade1, grade2):
    '''(number, number) -> float
    Return the average of grade1 and grade2.'''
    
    return our_math.add(grade1, grade2) / 2.0

avg = average(74.3, 85)
print "Your test average is: " + str(avg)