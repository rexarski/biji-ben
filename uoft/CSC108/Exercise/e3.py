def load_words(filename):
    '''(file) -> dict of {str: list of strs}
    The open file contains one lowercase word per line.
    Return a dictionary in which each key is a single lowercase
    letter and each value is a list of the words
    from the file that start with that letter.
    Only letters that one or more words from the file
    start with appear as keys in the dictionary.'''
    
    d = {}
    for line in filename:
        if line[0] not in d.keys():
            d[line[0]] = [line.strip()]
        else:
            d[line[0]].append(line.strip())        
    return d

def get_letter_counts(d):
    '''(dict of {str: list of strs}) -> dict of {str: int}
    In the given dictionary, each key is a single lowercase letter and
    each value is a list of lowercase words that start with that
    letter. Based on the given dictionary, return a new dictionary in
    which each key is a single lowercase letter and each value is the
    number of lowercase words that start with that letter.'''
    
    d2 = d
    i = 0
    while i != len(d.items()):
        d2[d2.keys()[i]] = len(d2.values()[i])
        i += 1
    return d2

def get_letter_percentage(d2, s):
    '''(dict of {str: int}, str) -> float
    In the given dictionary, each key is a single lowercase letter
    and each value is the number of lowercase words that start with
    that letter. The str parameter is a single lowercase letter. Based
    on the values in the dictionary, retrun the percentage of words
    that start with that letter. Note: use floating-point division.'''
    
    i = 0
    total = 0
    while i != len(d2.values()):
        total += int(d2.values()[i])
        i += 1
    if s in d2.keys():
        percentage = float(d2[s]) / total * 100
    else:
        percentage = float(0)
    return percentage

if __name__ == "__main__":
    
    filename = open('single_word_test.txt', 'w')
    filename.write('apple')
    filename.close()
    filename = open('single_word_test.txt', 'r')
    if load_words(filename) == {'a': ['apple']}:
        print 'First function passes in single word test.'
    else:
        print 'Error in single word test of the first function.'
    
    filename = open('two_same_words.txt', 'w')
    filename.write('apple')
    filename.write('\n')
    filename.write('apple')
    filename.close()
    filename = open('two_same_words.txt', 'r')
    if load_words(filename) == {'a': ['apple', 'apple']}:
        print 'First function passes in two same words test.'
    else:
        print 'Error in two same words test of the first function.'
    
    filename = open('two_diff_words.txt', 'w')
    filename.write('apple')
    filename.write('\n')
    filename.write('bike')
    filename.close()
    filename = open('two_diff_words.txt', 'r')
    if load_words(filename) == {'a': ['apple'], 'b': ['bike']}:
        print 'First function passes in two different words test.'
    else:
        print 'Error in two different words test of the first function.'
        
    filename = open('same_first_letter.txt', 'w')
    filename.write('apple')
    filename.write('\n')
    filename.write('april')
    filename.close()
    filename = open('same_first_letter.txt', 'r')
    if load_words(filename) == {'a': ['apple', 'april']}:
        print 'First function passes in two diff words started with same letter test.'
    else:
        print 'Error in two diff words started with same letter test of the first function.'
    
    filename = open('big_test.txt', 'w')
    filename.write('apple')
    filename.write('\n')
    filename.write('bike')
    filename.write('\n')
    filename.write('cat')
    filename.write('\n')
    filename.write('dog')
    filename.write('\n')
    filename.write('april')
    filename.write('\n')
    filename.write('biscuit')
    filename.write('\n')
    filename.write('cream')
    filename.write('\n')
    filename.write('dream')
    filename.close()
    filename = open('big_test.txt', 'r')
    if load_words(filename) == {'a': ['apple', 'april'], 'b': ['bike', 'biscuit'], 'c': ['cat', 'cream'], 'd': ['dog', 'dream']}:
        print 'First function passes in big test.'
    else:
        print 'Error in big test of the first function.'
        
    d = {'a': ['apple']}
    if get_letter_counts(d) == {'a': 1}:
        print 'Second function passes one-key-one-value test.'
    else:
        print 'Error in one-key-one-value test.'
    
    d = {'a': ['apple', 'april']}
    if get_letter_counts(d) == {'a': 2}:
        print 'Second function passes one-key-multi-value test.'
    else:
        print 'Error in one-key-multi-value test.'
    
    d = {'a': ['apple'], 'b': ['bike']}
    if get_letter_counts(d) == {'a': 1, 'b': 1}:
        print 'Second function passes multi-key-one-value test.'
    else:
        print 'Error in multi-key-one-value test.'
        
    d = {'a': ['apple', 'april'], 'b': ['bike', 'biscuit']}
    if get_letter_counts(d) == {'a': 2, 'b': 2}:
        print 'Second function passes multi-key-multi-value test.'
    else:
        print 'Error in multi-key-multi-value test.'
        
    d = {'a': []}
    if get_letter_counts(d) == {'a': 0}:
        print 'Second function passes one-key-none-value test.'
    else:
        print 'Error in one-key-none-value test.'
        
    d = {'a': [], 'b': []}
    if get_letter_counts(d) == {'a': 0, 'b': 0}:
        print 'Second function passes multi-key-none-value test.'
    else:
        print 'Error in multi-key-none-value test.'
        
    d = {'a': [], 'b': ['bike', 'biscuit']}
    if get_letter_counts(d) == {'a': 0, 'b': 2}:
        print 'Second function passes multi-key-mix-value test.'
    else:
        print 'Error in multi-key-mix-value test.'
        
    d2 = {'a': 2, 'b': 2}
    if get_letter_percentage(d2, 'a') == 50.0:
        print 'Third function passes str-in-dict test.'
    else:
        print 'Error in str-in-dict test.'
    
    d2 = {'a': 2, 'b': 2}
    if get_letter_percentage(d2, 'c') == 0.0:
        print 'Third function passes str-not-in-dict test.'
    else:
        print 'Error in str-not-in-dict test.'