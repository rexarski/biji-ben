import math

solnfile = open("quiz6soln.txt")
lines = solnfile.readlines()

TOL = .001
e = 10
testcases = (
  {'a':4.0, 'b':2.0, 'k':1.0},
  {'a':1.0, 'b':2.0, 'k':0.0},
  {'a':1.0, 'b':3.0, 'k':1.0}
)

def checklevelcosts(soln,a,b,k,case):
  allok = True
  for i in range(e+1):
    y = float(soln[i])
    if i == 0:
      if (abs(y - 1) > TOL):
        print("line {} is wrong".format(case*(e+1) + i + 1))
        allok = False
    else:
      if (abs((math.pow(y,1/(1.0*i)) * (b**k) ) / a - 1) > TOL):
        print("line {} is wrong".format(case*(e+1) + i + 1))
        allok = False
  if allok:
    print("Test case {} OK".format(case))

for j in range(len(testcases)):
  case = testcases[j]
  soln = lines[ j*(e+1) : (j+1)*(e+1) ]
  checklevelcosts(soln, case['a'], case['b'], case['k'], j)


