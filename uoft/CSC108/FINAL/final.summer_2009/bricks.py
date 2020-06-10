def make_bricks (num_small, num_big, goal):
  return num_small >= goal - (min (goal / 5, num_big) * 5)
