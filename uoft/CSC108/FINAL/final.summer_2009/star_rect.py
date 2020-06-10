def star_rect (f, h, w):
  '''Write a star rectangle of height h and width w to open file f.'''
  
  f.write ('*' * w + '\n')
  for i in range(h - 2):
    f.write ('*' + ' ' * (w - 2) + '*\n')
  f.write ('*' * w + '\n')
