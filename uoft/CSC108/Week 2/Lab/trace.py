import media
import random

# make a new 100 by 100 picture
pic = media.create_picture(100, 100)

# get 2 random numbers between 0 and 99 to use as coordinates
x = random.randint(0, 99)
y = random.randint(0, 99)

# get the pixel at this x,y coordinate
pix = media.get_pixel(pic, x, y)

# get the red, blue and green values of this pixel   
red = media.get_red(pix)
green = media.get_green(pix)
blue = media.get_blue(pix)

# introduce a new colour
new_color = media.orange

# make a 10 x 10 rectangle of the new colour inside our 
# picture, starting with our x and y as the upper 
# left corner. (In this case, it doesn't matter if some
# of the rectangle is outside the picture, as long as 
# the x,y corner is inside.)
media.add_rect_filled(pic, x, y, 10, 10, new_color)

# display the picture
media.show(pic)

# the colours should have changed in our pixel
red = media.get_red(pix)
green = media.get_green(pix)
blue = media.get_blue(pix)
