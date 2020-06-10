import media


def guess_captcha(a, b):
    '''(str, str) -> bool
    Return True if the strS nare the same (including lettercase), and
    False othewise'''
    
    return a == b

def get_picture_width(s):
    '''(str) -> int
    Return the width(in pixels) of the picture that will be used to display
    the str.'''
    
    return 10*len(s)

def word_to_pic(s):
    '''(str) -> Picture
    Return a Picture that contains the str.'''
    
    pic = media.create_picture(get_picture_width(s), 20)
    media.add_text(pic, 0, 0, s, media.black)
    return pic

def count_black(pic):
    '''(Picture) -> int
    Return the quantity of pixels in pic that are black.'''
    
    n = 0
    for pixel in pic:
        if media.get_color(pixel) == media.black:
            n = n + 1
    return n

def strikethrough(pic):
    '''(Picture) -> Picture
    Return a copy of the picture with a black line added horizontally 
    through the middle of the picture.'''
    
    pic_c = media.copy(pic)
    h = media.get_height(pic)
    w = media.get_width(pic)
    y1 = int(0.45*h)
    y2 = int(0.55*h)
    for i in range(y1,y2+1):
        media.add_line(pic_c, 0, i, w-1, i,media.black)
    return pic_c

def widen(pic):
    '''(Picture) -> Picture
    Return a new picture that is twice as wide as the
    given picture.'''
    def widen(pic):
        w = media.get_width(pic)
        h = media.get_height(pic)
        new_pic = media.create_picture(2*w, h)
        for pix in new_pic:
            x = media.get_x(pix)
            y = media.get_y(pix)
            x_1 = x/2
            pixel_1 = media.get_pixel(pic, x_1, y)
            col = media.get_color(pixel_1)
            media.set_color(pix, col)
    return new_pic

def overlay_color(pix1, pix2):
    '''(Pixel, Pixel) -> Color
    Return a new color made up of 80% of the color 
    values of the first
    pixel and 20% of the color values of the second pixel.'''
    r_1 = media.get_red(pix1)
    g_1= media.get_green(pix1)
    b_1 = media.get_blue(pix1)
    r_2 = media.get_red(pix2)
    g_2= media.get_green(pix2)
    b_2 = media.get_blue(pix2)
    color = media.create_color\
          (0.8*r_1+0.2*r_2, 0.8*g_1+0.2*g_2, 0.8*b_1+0.2*b_2)
    
    return color
    
    
def overlay_picture(pic1, pic2):
    '''(Picture, Picture) -> Picture
    Return a new picture with each pixel's color values made up of 80% 
    of the color values of the corresponding pixel in the first picture
    and 20% of the color values of the correspongding pixel in the second 
    picture.'''
    w = media.get_width(pic1)
    h = media.get_height(pic1)
    new_pic = media.create_picture(w, h)
    
    for pix in new_pic:
        x1 = media.get_x(pix)
        y1 = media.get_y(pix)
        pixel_1 = media.get_pixel(pic1, x1, y1)
        pixel_2 = media.get_pixel(pic2, x1, y1)
        col = overlay_color(pixel_1, pixel_2)
        media.set_color(pix, col)
    return new_pic
    

def flip(pic):
    '''(Picture) -> Picture
    Return a new picture that contains the pixels of the original picture
    flipped across the vertical axis.'''
    w = media.get_width(pic)
    h = media.get_height(pic)
    new_picture = media.create_picture(w, h)
    for pix in new_picture:
        x = media.get_x(pix)
        y = media.get_y(pix)
        x_1 = w - 1 - x
        pixel_1 = media.get_pixel(pic, x_1, y)
        col = media.get_color(pixel_1)
        media.set_color(pix, col)
        
    return new_picture
