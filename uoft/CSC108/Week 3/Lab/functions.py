import media

def intensity(pix):
    '''(Pixel) -> int
    Return the intensity of pix.'''
    
    pass

def greyscale(pic):
    '''(Picture) -> Picture
    Return a new Picture that is a greyscale version of pic.'''
    
    pass
    
def avg_intensity(pic):
    '''(Picture) -> float
    Return the average intensity of pic.'''
    
    pass

def red_cross():
    '''() -> Picture
    Return a 100 by 100 centered picture of the red cross symbol, where the symbol's width is 30 pixels.'''
    
    pass

if __name__ == "__main__":
    test_pic = media.load_picture(media.choose_file())
    test_color = media.springgreen
