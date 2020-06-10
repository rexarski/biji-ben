import media

filename = media.choose_file()
pic = media.load_picture(filename)
media.show(pic)