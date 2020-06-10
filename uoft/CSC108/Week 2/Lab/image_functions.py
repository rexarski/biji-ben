import media

def get_picture():
	
    # Replace the line below with an appropriate body for this function.
    pass

def maximize_red(pic):

    new_pic = copy(pic)
	
    for pix in new_pic:
        media.set_red(pix, 255)

    return new_pic
