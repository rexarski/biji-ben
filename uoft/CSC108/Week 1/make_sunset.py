import media

filename = media.choose_file()
pic = media.load_picture(filename)
media.show(pic)

sunset_pic = media.copy(pic)

for pixel in sunset_pic:
    value = media.get_green(pixel)  # Note: it should be pixel NOT sunset_pic!
    new_green = int(value * 0.7)
    media.set_green(pixel, new_green)
    
    value = media.get_blue(pixel)   # Note: it should be pixel NOT sunset_pic!
    new_blue = int(value * 0.7)
    media.set_blue(pixel, new_blue)
    
media.show(sunset_pic)