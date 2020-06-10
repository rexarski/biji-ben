import media

def make_test_pic():
    '''() -> Picture
    Return a 2 x 2 test picture with red, black, white and blue pixels.'''
    
    pic = media.create_picture(2, 2)

    p = media.get_pixel(pic, 0, 0)
    media.set_color(p, media.red)

    p = media.get_pixel(pic, 0, 1)
    media.set_color(p, media.black)

    p = media.get_pixel(pic, 1, 1)
    media.set_color(p, media.blue)

    return pic

def reduce_red(pic):
    '''(Picture) -> Picture
    Return a new picture with that contains the  in which each pixel's red 
    component is set to zero if it is currently greater than 100.'''

	new_pic = media.copy(pic)

    for pix in new_pic:
        if media.get_red(pix) > 100:
            media.set_red(pix, 0)

    return new_pic