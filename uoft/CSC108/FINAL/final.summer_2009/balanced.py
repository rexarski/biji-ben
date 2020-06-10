def all_balanced (L):
  segs = []
  for i in range(len(L)):
    balance = 0
    for j in range (i, len(L)):
      if L[j] == 1:
        balance += 1
      else:
        balance -= 1
      if balance == 0:
        segs.append (L[i:j+1])
  return segs

def len_longest_balanced_segment (L):
  segs = all_balanced (L)
  if len(segs) > 0:
    return len(max (segs, key=len))
  else:
    return 0

