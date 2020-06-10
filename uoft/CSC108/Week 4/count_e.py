if __name__ == '__main__':
    
    sentence = raw_input('Enter a sentence: ')
    
    e_count = 0
    
    # This loop executes len(sentence) times.
    for char in sentence:
        if char == 'e':
            e_count += 1
            #e_count = e_count + 1
    
    #print "There were " + str(e_count) + ' e characters.'
    print "There were", str(e_count),'e characters.'
            