def all_keys_values (d):
  '''Return True if each key in d is also a value in d,
  and each value in d is also a key in d.
  For example, all_keys_values ({2:5, 4:4, 5:2}) returns True.'''

  all_good = True
  for k in d:
    if k not in d.values():
      all_good = False
  for v in d.values():
    if v not in d.keys():
      all_good = False
  return all_good
