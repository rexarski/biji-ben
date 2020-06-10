import nose
from bricks import make_bricks

def test_first ():
  assert make_bricks (2, 2, 7), 'first'

def test_second():
  assert not make_bricks (2, 2, 8), 'second'

def test_third ():
  assert not make_bricks (0, 3, 9), 'third'
  
def test_fourth ():
  assert make_bricks (0, 3, 10), 'fourth'

def test_fifth ():
  assert not make_bricks (0, 3, 11), 'fifth'

def test_sixth ():
  assert make_bricks (3, 0, 2), 'sixth'

def test_seventh ():
  assert make_bricks (3, 0, 3), 'seventh'

def test_eighth ():
  assert not make_bricks (3, 0, 4), 'eighth'

def test_ninth ():
  assert make_bricks (4, 9, 12), 'ninth'
  
def test_tenth ():
  assert make_bricks (0, 0, 0), 'tenth'

def test_eleventh ():
  assert not make_bricks (0, 0, 2), 'eleventh'
  
if __name__ == '__main__':
  nose.runmodule()
  