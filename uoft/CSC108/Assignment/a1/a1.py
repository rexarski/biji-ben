import media


def guess_captcha(s1, s2):
    '''(str, str) -> bool
    Return True if the strings are the same (including lettercase),\
    and False otherwise.'''

    return s1 == s2


def get_picture_width(s):
    '''(str) -> int
    Return the width (in pixels) of the picture that will be used to \
    display the str. Each character in the str requires a width of \
    10 pixels.'''

    width = len(s) * 10
    return width


def word_to_pic(s):
    '''(str) -> Picture
    Return a Picture that contains the str. The picture should have a white \
    background with black text, be 20 pixels high, \
    and be as wide as get_picture_width specifies for the str. \
    The text should be placed at position (0, 0).'''

    pic = media.create_picture(len(s) * 10, 20, media.white)
    media.add_text(pic, 0, 0, s, media.black)
    return pic


def count_black(pic):
    '''(Picture) -> int
    Return the quantity of pixels in pic that are black.'''

    count = 0
    for pixel in pic:
        if media.get_color(pixel) == media.black:
            count += 1
    return count


def strikethrough(pic):
    '''(Picture) -> Picture
    Return a copy of the picture with a black line added horizontally \
    through the middle of the picture. The line's thickness should \
    be 10% of the height of the picture.'''

    pic_strike = media.copy(pic)
    h = media.get_height(pic_strike) / 10
    w = media.get_width(pic_strike)
    x = 0
    y = media.get_height(pic_strike) / 2 - media.get_height(pic_strike) / 20
    media.add_rect_filled(pic_strike, x, y, w, h, media.black)
    return pic_strike


def widen(pic):
    '''(Picture) -> Picture
    Return a new picture that is twice as wide as the given picture. \
    For each pixel (x, y) in the original picture, the pixels (2 * x, y ) \
    and (2 * x + 1, y) in the new picture should \
    be set to the same color as it.'''

    w = media.get_width(pic)
    h = media.get_height(pic)
    pic2 = media.create_picture(2 * w, h, media.white)
    for pixel2 in pic2:
        x2 = media.get_x(pixel2)
        x = x2 / 2
        y = media.get_y(pixel2)
        pixel = media.get_pixel(pic, x, y)
        color = media.get_color(pixel)
        media.set_color(pixel2, color)
    return pic2


def overlay_color(Pixel1, Pixel2):
    '''(Pixel, Pixel) -> Color
    Return a new color made up of 80% of the color values \
    of the first pixel and 20% of the color values of the second pixel.'''

    red1 = media.get_red(Pixel1)
    red2 = media.get_red(Pixel2)
    green1 = media.get_green(Pixel1)
    green2 = media.get_green(Pixel2)
    blue1 = media.get_blue(Pixel1)
    blue2 = media.get_blue(Pixel2)
    new_red = int(red1 * 0.8) + int(red2 * 0.2)
    new_green = int(green1 * 0.8) + int(green2 * 0.2)
    new_blue = int(blue1 * 0.8) + int(blue2 * 0.2)
    new_color = media.create_color(new_red, new_green, new_blue)
    return new_color


def overlay_picture(Picture1, Picture2):
    '''(Picture, Picture) -> Picture
    Return a new picture with each pixel's color values made \
    up of 80% of the color values of the corresponding pixel \
    in the first picture and 20% of the color values of the \
    corresponding pixel in the second picture. \
    By "corresponding pixel", \
    we mean pixel at the same (x, y) coordinates. '''

    w1 = media.get_width(Picture1)
    h2 = media.get_height(Picture2)
    Picture3 = media.create_picture(w1, h2, media.white)
    for Pixel3 in Picture3:
        x = media.get_x(Pixel3)
        y = media.get_y(Pixel3)
        Pixel1 = media.get_pixel(Picture1, x, y)
        Pixel2 = media.get_pixel(Picture2, x, y)
        col = overlay_color(Pixel1, Pixel2)
        media.set_color(Pixel3, col)
    return Picture3


def flip(pic):
    '''(Picture) -> Picture
    Return a new picture that contains the pixels of \
    the original picture flipped across the vertical axis.'''

    w = media.get_width(pic)
    h = media.get_height(pic)
    new_pic = media.create_picture(w, h)
    for new_pix in new_pic:
        x = media.get_x(new_pix)
        y = media.get_y(new_pix)
        x_flip = (w - 1) - x
        pix_flip = media.get_pixel(pic, x_flip, y)
        media.set_color(new_pix, media.get_color(pix_flip))
    return new_pic
