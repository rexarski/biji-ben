import urllib

# Precondition for all functions in this module: Each line of the url
# file contains the average monthly temperatures for a year (separated
# by spaces) starting with January.  The file must also have 3 header
# lines.

# Instead of using the terms "url" or "file", we use the more general
# term "reader" to indicate an open file or webpage.

def open_temperature_file(url):
    '''(str) -> reader
    Open the URL url, read past the three-line header, and 
    return the open reader.'''

    f = urllib.urlopen(url)
    f.readline()
    f.readline()
    f.readline()
    return f

def avg_temp_march(r):
    ''' (reader) -> float
    Return the average temperature for the month of March for all years in r.'''
    
    total = 0
    for lines in r:
        months = lines.split()
        total = total + float(months[2])
    return total/12

def avg_temp(r, mo):
    '''(reader, int) -> float
    Return the average temperature for month mo for all years in r.
    mo is between 0 and 11, inclusive, representing January to December,
    respectively.'''
    
    total = 0
    for lines in r:
        months = lines.split()
        total = total + float(months[mo])
    return total/12
    
def higher_avg_temp(url, mo1, mo2):
    '''(str, int, int) -> int
    Return either mo1 or mo2 (they are values in the range 0 to 11), whichever 
    has the higher average temperature for all years in the webpage at url.  
    If the months have the same average temperature, then return -1.'''
    
    temp1 = avg_temp(r, mo1)
    temp2 = avg_temp(r, mo2)
    if temp1 == temp2:
        return -1
    elif temp1 > temp2:
        return mo1
    else:
        return mo2

def three_highest_temps(r):
    '''(reader) -> list of floats
    Return a list that contains the three highest temperatures, in descending
    order, for all months of all years in r.'''

    s = f.read()
    L = s.split()
    highest = []
    for num in L:
        num = float(num)
    L.sort().reverse()
    highest.append(L[0])
    highest.append(L[1])
    highest.append(L[2])
    return highest
    

def below_freezing(r):
    '''(reader) -> list of floats
    Return a list that contains the temperatures below freezing (32 degrees
    Fahrenheit), in ascending order, for all months in all years in r.'''

    L = f.read().split()
    below = []
    for num in L:
        num = float(num)
        if num < 32:
            below.append(num)
    below.sort()
    return below
