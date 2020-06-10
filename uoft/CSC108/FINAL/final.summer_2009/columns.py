def column_sums (f):
  '''Return the list of column sums from open file object f.'''
  
  sums = {}
  for line in f:
    vals = line.split()
    for pos, val in enumerate(vals):
      sums[pos] = sums.get(pos, 0) + int(val)
  cols = []
  for key in sorted(sums):
    cols.append (sums[key])
  return cols
  