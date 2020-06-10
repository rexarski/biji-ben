'''A cool program to generate fake text based on some training text.'''

def learn_occurrences(training_text):
    '''(file) -> dict
    Return a dictionary containing word occurrence information determined
    from open file training_text.'''
    
    pass

def generate_text(occurrence_dict, num_words):
    '''(dict) -> str
    Return the text generated based on the word occurrence info in 
    occurrence_dict.'''
    
    pass

if __name__ == '__main__':
    
    f = open(raw_input("Which training file? "))
    
    # Scan the training text and make a dictionary storing
    # word occurrence information.
    occurrence_dict = learn_occurrences(f)
    
    # Generate and print new text with the specificed number of words from that
    # dictionary.
    new_text = generate_text(occurrence_dict, 500)
    print new_text