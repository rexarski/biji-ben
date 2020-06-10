import media

def prompt_and_open():
    '''() -> file
    Prompt the user to enter a file name, open the file
    for reading, and return the open file object.'''

    filename = media.choose_file()
    input_file = open(filename)
    return input_file

def print_starts_with(our_file, char):
    '''(file, str) -> NoneType
    Print the lines of our_file that start with the character char.'''

    for line in our_file:
        if line.lstrip().startswith(char):
            print line,

if __name__ == '__main__':
    input_file = prompt_and_open()
    print_starts_with(input_file, '#')