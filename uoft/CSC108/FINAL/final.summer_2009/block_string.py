def block_string(s, c):
  '''s is a string, c is a one-character string. Return True exactly when 
  s consists entirely of increasing-length blocks of character c, 
  each followed by a space. For example, block_string ('a aa aaa ', 'a') 
  returns True, but block_string ('aa a aaa ', 'a') returns False.'''
  
  all_good = True
  block = 1
  i = 0
  while i < len(s) and all_good:
    chunk = s[i:i+block + 1]
    if chunk != c * block + ' ':
      all_good = False
    i = i + block + 1
    block = block + 1
  return all_good
