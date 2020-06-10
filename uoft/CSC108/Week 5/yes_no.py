def yes_no_answer(prompt):
    '''(str) -> bool
    Ask the user for a yes/no answer using prompt. 
    Continue until they give a valid response. Return 
    True if the answer was "yes", and return False
    otherwise.'''
    
    answer = raw_input(prompt)
    
    while answer != 'yes' and answer != 'no':
        answer = raw_input(prompt)
        
    return answer == 'yes'

if __name__ == "__main__":
    
    if yes_no_answer("Are you having fun? "):
        print "Great! Me too!"
    else:
        print "That's a shame."