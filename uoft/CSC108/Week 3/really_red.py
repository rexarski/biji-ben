def count_really_red(pic):
    '''(Picture) -> int
    Return the number of pixels in pic with red values
    greather than 200.'''
    
    count = 0
    for pixel in pic:
        if media.get_red(pixel) > 200:
            count = count + 1
    return count
