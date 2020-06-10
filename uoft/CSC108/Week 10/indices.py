'''An example to use for practicing testing and debugging.'''

def get_indices(text, s):
    '''(str, str) -> list of ints
    Return a list containing the indices where s appears in text.'''
    
    index = 0
    indices = []
    while text.find(s, index) != -1:
        index = text.find(s, index)
        indices.append(text.find(s, index))
    return indices
