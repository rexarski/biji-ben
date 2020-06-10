import media

filename = media.choose_file()
pic = media.load_picture(filename)
media.show(pic)
sunset_pic = media.copy(pic)
for pixel in sunset_pic:
    new_blue = int(0.5*media.get_blue(pixel))
    media.set_blue(pixel, new_blue)
    new_green = int(0.5*media.get_green(pixel))
    media.set_green(pixel, new_green)
media.show(sunset_pic)