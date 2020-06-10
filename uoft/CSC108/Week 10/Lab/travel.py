import media

def chromakey(person_pic, background_pic):
    '''(Picture, Picture) -> NoneType
    Replace the green pixels in person_pic with the corresponding
    pixels from background_pic.  The pictures must have the same
    dimensions.'''

    pass

if __name__ == '__main__':
    
    # Prompt the user to choose a picture of a person.
    pic1 = media.load_picture(media.choose_file())
    media.show(pic1)
    
    # Prompt the user to choose a background picture
    pic2 = media.load_picture(media.choose_file())
    media.show(pic2)
    
    # Display the picture of the person with the new background.
    chromakey(pic1, pic2)
    media.show(pic1)