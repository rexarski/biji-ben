import media

def same_dimensions(pic_1, pic_2):
        for pixel in pic_1:
                width_1 = media.get_width(pic_1)
                height_1 = media.get_height(pic_1)
        for pixel in pic_2:
                width_2 = media.get_width(pic_2)
                height_2 = media.get_height(pic_2)
        
        if width_1 == width_2 and height_1 == height_2:
                return True
        else:
                return False

def copyright():
        pic_3 = media.create_picture(20, 20)
        black = media.black
        media.add_oval(pic_3, 0, 0, 16, 16, black)
        media.add_text(pic_3, 6, 3, 'C', black)
        return pic_3

def moderate_blue(picture):
        pic_4 = media.copy(picture)
        for pixel in pic_4:
                red = media.get_red(pixel)
                green = media.get_green(pixel)
                new_blue = int((red + green) / 2)
                media.set_blue(pixel, new_blue)
        return pic_4