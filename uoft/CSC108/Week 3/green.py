import media

def total_green(pic):
    '''(Picture) -> int
    Return the total amount of green in pic.'''
    
    total = 0   # we call total an "accumulator"
    for pixel in pic:
        total = total + media.get_green(pixel)
    return total