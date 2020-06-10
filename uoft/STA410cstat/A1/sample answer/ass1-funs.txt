# STA 410/2102, Fall 2015, Functions for Assignment #1.

source("bisect.r")
source("mvnewton.r")


# Compute the log likelihood for parameters p, given sample sizes n, m1, and m2,
# and observed counts x, x1, and x2.

log_likelihood <- function (p, n, m1, m2, x, x1, x2)
{
    dbinom (x, n, mean(p), log=TRUE) + 
      dbinom (x1, m1, p[1], log=TRUE) + 
      dbinom (x2, m2, p[2], log=TRUE)
}


# Compute the gradient of the log likelihood for parameters p, returning the
# vector of derivatives w.r.t. the two components of p.

log_likelihood_gradient <- function (p, n, m1, m2, x, x1, x2)
    c (x/mean(p)/2 - (n-x)/(1-mean(p))/2 + x1/p[1] - (m1-x1)/(1-p[1]),
       x/mean(p)/2 - (n-x)/(1-mean(p))/2 + x2/p[2] - (m2-x2)/(1-p[2])
    )


# Compute the two-by-two Hessian matrix of second derivatives of the log 
# likelihood, for parameters p.

log_likelihood_hessian <- function (p, n, m1, m2, x, x1, x2)
    matrix (c (- x/mean(p)^2/4 - (n-x)/(1-mean(p))^2/4
                  - x1/p[1]^2 - (m1-x1)/(1-p[1])^2,
               - x/mean(p)^2/4 - (n-x)/(1-mean(p))^2/4,
               - x/mean(p)^2/4 - (n-x)/(1-mean(p))^2/4,
               - x/mean(p)^2/4 - (n-x)/(1-mean(p))^2/4
                  - x2/p[2]^2 - (m2-x2)/(1-p[2])^2
            ), 2, 2)


# Compute the two-by-two Fisher information matrix for parameters p.

fisher_information <- function (p, n, m1, m2, x, x1, x2)
    matrix (c (n/mean(p)/4 + n/(1-mean(p))/4
                  + m1/p[1] + m1/(1-p[1]),
               n/mean(p)/4 + n/(1-mean(p))/4,
               n/mean(p)/4 + n/(1-mean(p))/4,
               n/mean(p)/4 + n/(1-mean(p))/4
                  + m2/p[2] + m2/(1-p[2])
            ), 2, 2)


# Find the maximum likelihood estimate of the parameter vector by alternating
# maximization, given sample sizes n, m1, and m2 and observed counts x, x1,
# and x2.  The last argument is the initial value of the parameters to use.
# Iterations continue until there is no change in the estimate.  The range for
# the parameters is taken to be 1e-10 to 1-1e-10 in order to avoid any possible
# problems with probabilities of exactly 0 or 1.

mle_alt <- function (n, m1, m2, x, x1, x2, initial)
{
    p <- initial

    i <- 1
    repeat {
        op <- p
        p[1] <- bisect2(function (p1) 
                         log_likelihood_gradient(c(p1,p[2]),n,m1,m2,x,x1,x2)[1],
                        1e-10, 1-1e-10)
        p[2] <- bisect2(function (p2)
                         log_likelihood_gradient(c(p[1],p2),n,m1,m2,x,x1,x2)[2],
                        1e-10, 1-1e-10)
        cat("i =",i,"p1 =",p[1],"  p2 =",p[2],"\n")
        if (all(p==op))
            break
        i <- i+1
    }

    p
}


# Find the maximum likeliihood estimate of the parameter vector by multivariate
# Newton iteration, given sample sizes n, m1, and m2 and observed counts x, x1,
# and x2.  The last arguments are the initial value of the parameters to use
# and the number of iterations to do.

mle_mvn <- function (n, m1, m2, x, x1, x2, initial, iters)
    mvnewton (function (p) log_likelihood_gradient(p,n,m1,m2,x,x1,x2), 
              function (p) log_likelihood_hessian(p,n,m1,m2,x,x1,x2), 
              initial, iters)


# Find the maximum likeliihood estimate of the parameter vector by the method
# of scoring, given sample sizes n, m1, and m2 and observed counts x, x1,and x2.
# The last arguments are the initial value of the parameters to use and the
# number of iterations to do.

mle_mos <- function (n, m1, m2, x, x1, x2, initial, iters)
    mvnewton (function (p) log_likelihood_gradient(p,n,m1,m2,x,x1,x2), 
              function (p) -fisher_information(p,n,m1,m2,x,x1,x2), 
              initial, iters)


# Find the maximum likeliihood estimate of the parameter vector by calling R's
# nlm function, with default parameter settings, given sample sizes n, m1, and 
# m2 and observed counts x, x1,and x2.  The last argument is the initial value
# of the parameters to use.

mle_nlm <- function (n, m1, m2, x, x1, x2, initial)
{
    nlm (function (p) -log_likelihood(p,n,m1,m2,x,x1,x2), initial) $ estimate
}
