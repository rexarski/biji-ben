source("~/Dropbox/1516/STA410cstat/A1/function.r")

options(digits=17)

n <- 130
m1 <- 25
m2 <- 25
x <- 75
x1 <- 20
x2 <- 6
iters <- 10
initial <- c (0, 0)

i <- 1

while (i < 4) {
  set.seed(i)
  initial[1] <- runif(1, 0.5, 1) # we tend to set our initial guess suitable, as the observed p1 = 0.8
  initial[2] <- runif(1, 0, 0.5) # similarly since observed p2 = 0.24
  
  cat("\nAlternating Maximization with initial guess p1 =", initial[1], "and p2=", initial[2], "\n")
  print( a <- mle_alt(n, m1, m2, x, x1, x2, initial))
  cat("\nMultivariate Newton Iteration with initial guess p1 =", initial[1], "and p2=", initial[2], "\n")
  print( b <- mle_mvn(n, m1, m2, x, x1, x2, initial, iters))
  cat("\nMultivariate Method of Scoring with initial guess p1 =", initial[1], "and p2=", initial[2], "\n")
  print( c <- mle_mos(n, m1, m2, x, x1, x2, initial, iters))
  cat("\nBuilt-in nlm Function with initial guess p1 =", initial[1], "and p2=", initial[2], "\n")
  print( d <- mle_nlm(n, m1, m2, x, x1, x2, initial))
  i <- i + 1
}

# increase number of iterations for mvn and mos

# these are results of previous random number generation.

data1 <- c (0.63275433157104999, 0.18606194981839508)
data2 <- c (0.59244112996384501, 0.35118701797910035)
data3 <- c (0.58402076316997409, 0.40375819953624159)

print(mle_mos(130, 25, 25, 75, 20, 6, data1, 20))

print(mle_mos(130, 25, 25, 75, 20, 6, data2, 20))

print(mle_mos(130, 25, 25, 75, 20, 6, data3, 20))