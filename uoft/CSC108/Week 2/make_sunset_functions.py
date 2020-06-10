import media

def get_picture():
    filename = media.choose_file()
    pic = media.load_picture(filename)
    return pic
    
def get_sunset_pic(picture):
    sunset_pic = media.copy(picture)
    
    for pixel in sunset_pic:
        value = media.get_green(pixel)
        new_green = int(value * 0.7)
        media.set_green(pixel, new_green)
        
        value = media.get_blue(pixel)
        new_blue = int(value * 0.7)
        media.set_blue(pixel, new_blue)
    return sunset_pic

pic = get_picture()
media.show(pic)
media.show(get_sunset_pic(pic))