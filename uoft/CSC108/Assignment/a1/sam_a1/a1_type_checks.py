'''This module should be used to test the parameter and return types of your
functions.  Run this on your a1.py and make sure there are no errors before
submitting.'''

import a1
import media

if __name__ == "__main__":
	
    # Type check a1.guess_captcha	
    result = a1.guess_captcha('hello', 'hello')
    
    assert isinstance(result, bool),\
    '''a1.guess_captcha('hello', 'hello') should return a bool, 
    but returned %s.''' % (type(result))
   
    # Type check a1.get_picture_width
    result = a1.get_picture_width('bye')
    expected = 30

    assert isinstance(result, int),\
    '''a1.get_picture_width('bye') should return an int, but returned
    %s.''' % (type(result))
    
    # Type check a1.word_to_pic
    result = a1.word_to_pic('today')
	
    assert isinstance(result, media.Picture), \
    '''a1.word_to_pic(\'today\') should return a Picture, but it returned
    %s.''' % (type(result))	
    
    # Type check a1.count_black
    pic = media.create_picture(2, 3)
    result = a1.count_black(pic)
    
    assert isinstance(result, int), \
    '''a1.count_black(pic) should return an int, but it returned 
    %s.''' % (type(result))
    
    # Type check a1.strikethrough
    pic = media.create_picture(30, 20)
    result = a1.strikethrough(pic)
    
    assert isinstance(result, media.Picture), \
    '''a1.strikethrough(pic) should return a Picture, but it returned 
    %s.''' % (type(result))
    
    # Type check a1.widen
    pic = media.create_picture(30, 20)
    result = a1.widen(pic)
	    
    assert isinstance(result, media.Picture), \
    '''a1.widen(pic) should return a Picture, but it returned
    %s.''' % (type(result))	
		
    # Type check a1.overlay_color	
    pic = media.create_picture(2, 3)
    pix1 = media.get_pixel(pic, 0, 0)
    pix2 = media.get_pixel(pic, 1, 1)
    media.set_color(pix1, media.orange)
    media.set_color(pix2, media.blue)
    result = a1.overlay_color(pix1, pix2)
    
    assert isinstance(result, media.Color), \
    '''a1.overlay_color(pix1, pix2) should return a Color, but it returned
    %s.''' % (type(result))
    
    # Type check a1.overlay_picture
    pic1 = media.create_picture(2, 3)
    pix1 = media.get_pixel(pic, 0, 0)
    pix2 = media.get_pixel(pic, 1, 1)
    r1, g1, b1 = 50, 100, 200
    r2, g2, b2 = 40, 150, 0
    media.set_color(pix1, media.create_color(r1, g1, b1))
    media.set_color(pix2, media.create_color(r2, g2, b2))
    pic2 = media.create_picture(2, 3)
    
    result = a1.overlay_picture(pic1, pic2)
    
    assert isinstance(result, media.Picture), \
    '''a1.overlay_picture(pic1, pic2) should return a Picture, but it returned
    %s.''' % (type(result))
    
    # Type check a1.flip
    pic = media.create_picture(2, 4)
    result = a1.flip(pic)
    
    assert isinstance(result, media.Picture), \
    '''a1.flip(pic) should return a Picture, but it returned 
    %s.''' % (type(result))