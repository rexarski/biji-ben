def get_report(temp):
    '''(number) -> str
    Return a message describing temp.'''

    message = ''
    
    if temp < 0:
        message = "Brrr, it's freezing!"
    
    return message
        
def get_report2(temp):
    '''(number) -> str
    Return a message describing temp.'''

    message = ''
    
    if temp < 0:
        message =  "Brrr, it's freezing!"
    elif temp > 0:
        message = "Yippee!"
    
    return message

def get_report3(temp):
    '''(number) -> str
    Return a message describing temp.'''

    message = ''
    
    if temp < 0:
        message =  "Brrr, it's freezing!"
    elif temp > 0:
        message = "Yippee!"
    else:
        message = "At freezing."
    
    return message


if __name__ == '__main__':
    print get_report3(0)