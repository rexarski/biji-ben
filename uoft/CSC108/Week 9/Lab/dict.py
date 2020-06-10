import urllib

def dict_to_str(d):
    '''(dict) -> str
    Return a str containing each key and value from d. Keys and
    values are separated by a space. Each key-value pair is separated by a
    comma.''' 
    
    s = ""
    for (k, v) in d.items():
        s = s + str(k) + " " + str(v) + ","
    return s

def dict_to_str_sorted(d):
    '''(dict) -> str
    Return a str containing each key and value from d. Keys and
    values are separated by a space. Each key-value pair is separated by a
    comma, and the pairs are sorted in ascending order by key.''' 
    
    s = ""
    L = d.keys()
    L.sort()
    for k in L:
        s = s + str(k) + " " + str(d(k)) + ","
    return s

def file_to_dict(f):
    '''(file) -> dict of {float : int}
    f contains exchange rate changes as floating point numbers separated by
    whitespace. Return a dict of how many times each rate change occurred, 
    with exchange rates as keys and the number of occurrences of the exchange
    rates as values.'''
    
    d = {}
    L = f.read().split()
    for rate_change in L:
        change = float(rate_change)
        if d.has_key(change):
            d(change) = d(change) + 1
        else:
            d(change) = 1
    return d
    
def count_data(d):
    '''(dict of {float : int}) -> int
    The keys in d are exchange rate changes and values are the number of 
    occurrences of each exchange rate change, return the total number of 
    exchange rate changes (including duplicates).'''
    
    total = 0
    for value in d.values():
        total = total + value
    return total

def most_common_rate_change(d):
    '''(dict of {float : int}) -> list of floats
    In d, keys are exchange rate changes and values are the number of 
    occurrences of each exchange rate.  Return a list of the exchange rate
    change(s) that occur the same number of times as the maximum number
    of occurrences of any rate change.'''  
    
    L = []
    max_num = max(d.values())
    for k in d.keys():
        if d(k) == max_num:
            L.append(k)
    return L
    
if __name__ == '__main__':
    
    filename = "http://www.stat.duke.edu/~mw/data-sets/ts_data/exchange-rates"
