import random

'''A cool program to generate fake text based on some training text.'''

def add_new_pair(previous, current, occurrence_dict):
    '''(str, str, dict of [str: list of strs]) -> NoneType
    Update the word occurence dictionary occurrence_dict
    to reflect that current followed previous once / one more time.'''
    
    if previous in occurrence_dict:
        occurrence_dict[previous].append(current)
    else:
        occurrence_dict[previous] = [current]

def learn_occurrences(training_text):
    '''(file) -> dict
    Return a dictionary containing word occurrence information determined
    from open file training_text.'''
    
    occurrence_dict = {}
    word_list = training_text.read().split()

    previous = ''
    for word in word_list:
        #print '%s followed %s' % (word, previous)
        add_new_pair(previous, word, occurrence_dict)
        previous = word
    
    return occurrence_dict

def choose_random_element(L):
    '''(list) -> object
    Return a random element of L.'''
    
    random.shuffle(L)
    return L[0]


def choose_next_word(current, occurrence_dict):
    '''(str, dict of {str : list of strs} -> str
    Return a random word to follow word current, based
    on the occurrence patterns in word occurrence
    dictionary occurrence_dict.'''
    
    # Original version:
    #return choose_random_element(occurrence_dict[current])
    
    # Improved version:
    if current in occurrence_dict:
        return choose_random_element(occurrence_dict[current])
    else:
        return choose_random_element(occurrence_dict.keys())
                    

def generate_text(occurrence_dict, num_words):
    '''(dict of {str : list of strs}) -> str
    Return the text generated based on the word occurrence info in 
    occurrence_dict.'''
    
    # How to start?  First word?
    # - first word from training text
    # - pick a random first word
    # Desired number of words:
    #    pick a random next word, based on the latest
    #    word and following the occurrence patterns,
    #    and add it to the text
    
    # Original version of picking first word: 
    #current = ''
    #text = ''
          
    
    # Improved version of picking first word:
    current = choose_random_element(occurrence_dict.keys())
    text = current
    
    for i in range(num_words):
        next_word = choose_next_word(current, occurrence_dict)
        text = text + ' ' + next_word
        current = next_word
    
    return text

if __name__ == '__main__':
    
    f = open(raw_input("Which training file? "))
    
    # Scan the training text and make a dictionary storing
    # word occurrence information.
    occurrence_dict = learn_occurrences(f)
    #print occurrence_dict
    
    # Generate and print new text with the specificed number of words from that
    # dictionary.
    new_text = generate_text(occurrence_dict, 500)
    print new_text