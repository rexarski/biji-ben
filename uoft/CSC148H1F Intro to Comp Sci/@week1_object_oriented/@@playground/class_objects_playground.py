class Point:
    '''Point class represents and manipulates x,y coords. '''
    
    def __init__(self, x = 0, y = 0):
        '''Create a new point at the origin. '''
        self.x = x
        self.y = y
        
    def distance_from_origin(self):
        '''Compute my distance from the origin. '''
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5
    
    def to_string(self):
        return '{0}, {1}'.format(self.x, self.y)
    
    def __str__(self):  # All we have done is renamed the method
        return '({0}, {1})'.format(self.x, self.y)
    
    def midpoint(p1, p2):
        '''Return the midpoint of points p1 and p2. '''
        mx = (p1.x + p2.x) / 2
        my = (p1.y + p2.y) / 2
        return Point(mx, my)
    
    def halway(self, target):
        '''Return the halfway point between myself and the target. '''
        mx = (self.x + target.x) / 2
        my = (self.y + target.y) / 2
        return Point(mx, my)
    
    # print_time(current_time)
    # is like saying: 'Hey, print_time! Here's an object for you to print.'
    # current_time.print_time()
    # is more like saying: 'Hey current_time! Please print yourself!'
    

class Rectangle:
    '''A class to manufacture rectangle objects.'''
    
    def __init__(self, posn, w, h):
        '''Initialize rectangle at posn, with width w, height h.'''
        self.corner = posn
        self.width = w
        self.height = h
        
    def __str__(self):
        return '({0}, {1}, {2})'.format(self.corner, self.width, self.height)
    
    def grow(self, delta_width, delta_height):
        '''Grow (or shrink) this object by the deltas.'''
        self.width += delta_width
        self.height += delta_height
        
    def move(self, dx, dy):
        '''Move this object by the deltas.'''
        self.corner.x += dx
        self.corner.y += dy
    
    def same_coordinates(p1, p2):
        return (p1.x == p2.x) and (p1.y == p2.y)
    
# box = Rectangle(Point(0, 0), 100, 200)
# bomb = Rectangle(Point(100, 80), 5, 10)
# print('box: ', box)
# print('bomb: ', bomb)

