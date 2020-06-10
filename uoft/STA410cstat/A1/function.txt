options(digits=17)

# since we cannot comment out the call of the cat function online, so I used the modified version locally
# source("http://utstat.utoronto.ca/~radford/sta410/bisect.r") 
source("~/Dropbox/1516/STA410cstat/codes/week2/bisect.r")
source("http://utstat.utoronto.ca/~radford/sta410/mvnewton.r")

# First we need to implement these helper functions:

log_likelihood <- function (p, n, m1, m2, x, x1, x2) {
  
  p1 <- p[1]
  p2 <- p[2]
  if(any(p<=0)) {
    -Inf
  }
  if(p1+p2>=2) {
    -Inf
  }
  if(any(p>=1)) {
    -Inf
  }
  else {(log(choose(n, x))+log(choose(m1, x1))+log(choose(m2,x2)) 
        +x*log((p1+p2)/2)+(n-x)*log(1-(p1+p2)/2)
        +x1*log(p1)+(m1-x1)*log(1-p1) 
        +x2*log(p2)+(m2-x2)*log(1-p2))
  }
}
  
log_likelihood_gradient <- function (p, n ,m1, m2, x, x1, x2) {
  
  p1 <- p[1]
  p2 <- p[2]
  dp1 <- x/(p1+p2)+(n-x)/(p1+p2 - 2)+x1/p1+(m1-x1)/(p1-1)
  dp2 <- x/(p1+p2)+(n-x)/(p1+p2 - 2)+x2/p2+(m2-x2)/(p2-1)
  c (dp1, dp2)
}
  
log_likelihood_hessian <- function (p, n, m1, m2, x, x1, x2) {
  
  p1 <- p[1]
  p2 <- p[2]
  matrix (c (-x*(p1+p2)^(-2)-(n-x)*(p1+p2-2)^(-2)-x1*p1^(-2)-(m1-x1)*(p1-1)^(-2), 
             -x*(p1+p2)^(-2)-(n-x)*(p1+p2-2)^(-2),
             -x*(p1+p2)^(-2)-(n-x)*(p1+p2-2)^(-2),
             -x*(p1+p2)^(-2)-(n-x)*(p1+p2-2)^(-2)-x2*p2^(-2)-(m2-x2)*(p2-1)^(-2)),
          2, 2)
}

fisher_information <- function (p, n, m1, m2, x, x1, x2) {

  p1 <- p[1]
  p2 <- p[2]
  matrix (- c (n/2*(p1+p2)^(-1)+n/2*(2-p1-p2)^(-1)+m1/p1+m1*(1-p1)^(-1), n/2*(p1+p2)^(-1)+n/2*(2-p1-p2)^(-1), 
             n/2*(p1+p2)^(-1)+n/2*(2-p1-p2)^(-1), n/2*(p1+p2)^(-1)+n/2*(2-p1-p2)^(-1)+m2/p2+m2*(1-p2)^(-1)), 
          2, 2)
}

# Method 1: Alternating maximization (non-linear Gauss-Siedel iteration)

mle_alt <- function (n, m1, m2, x, x1, x2, initial) {
  
  origin <- initial
  temp <- c (2, 2) # impossible values by definition
  i <- 1 # iteration counter
  
  while (origin[1] != temp[1] || origin[2] != temp[2]) {
    if (i != 1) {
      origin <- temp
    }
    
    # to iterative alternatively, we need to fix one parameter at a time
    
    # fixed p2
    f <- function(p) { 
      x/(p+origin[2])+(n-x)/(p+origin[2]-2)+x1/p+(m1-x1)/(p-1)    
    }
    # fixed p1
    g <- function(p) {
      x/(origin[1]+p)+(n-x)/(origin[1]+p - 2)+x2/p+(m2-x2)/(p-1)
    }
    
    temp <- c(bisect2(f, 0.001, 0.999), bisect2(g, 0.001, 0.999))
    cat("i =", i, "p1 =", temp[1], "p2 =", temp[2], "\n")
    i <- i+1
  }
}

# Method 2: Multivariate Newton iteration

mle_mvn <- function (n, m1, m2, x, x1, x2, initial, iters) {

  mvnewton (function (p) log_likelihood_gradient(p, n, m1, m2, x, x1, x2), 
            function (p) log_likelihood_hessian(p, n, m1, m2, x, x1, x2) , initial, iters)
}
  
# Method 3: Multivariate method of scoring

mle_mos <- function (n, m1, m2, x, x1, x2, initial, iters) {
  
  mvnewton (function (p) log_likelihood_gradient(p, n, m1, m2, x, x1, x2), 
            function (p) fisher_information(p, n, m1, m2, x, x1, x2), initial, iters) 
}

# Method 4: R’s built-in nlm function

mle_nlm <- function (n,m1,m2,x,x1,x2,initial) {
  
  nlm(function (p) -log_likelihood(p, n, m1, m2, x, x1, x2), initial, hessian=TRUE)
}
