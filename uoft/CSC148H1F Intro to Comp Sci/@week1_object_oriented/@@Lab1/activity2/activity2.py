""" Run Class """

import sys
from handler import Handler

def run_interaction():
    handler = Handler()
    
    while True:
        line = input()
        if line == 'exit':
            print('Goodbye! Thank you for using our program!')
            break
        elif not handler.process(line):
            print("Invalid command.")
            
if __name__ == '__main__':
    run_interaction()