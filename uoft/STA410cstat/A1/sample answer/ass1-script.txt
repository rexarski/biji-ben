#+ setup,include=FALSE
source("http://utstat.utoronto.ca/~radford/knitr-options.r")
#+

#' STA 410/2102, Fall 2015, Script for Assignment #1.

source("ass1-funs.r")

options(digits=17)

#' Set the sample sizes and observed counts for the data in the assignment 
#' handout.

n <- 130
m1 <- 25
m2 <- 25

x  <- 75
x1 <- 20
x2 <-  6

#' Create a contour plot of the log likelihood function, for reference when 
#' discussing the results.

log_likelihood_contour <- function (n,m1,m2,x,x1,x2, ...)
{
    grid <- seq(0.01, 0.99, by=0.01)
    ll <- matrix(nrow=length(grid),ncol=length(grid))
    for (i in 1:length(grid))
        for (j in 1:length(grid))
            ll[i,j] <- log_likelihood(c(grid[i],grid[j]),n,m1,m2,x,x1,x2)
    contour (grid, grid, ll, ...)
}

log_likelihood_contour(n,m1,m2,x,x1,x2,nlevels=200)

#' Try the methods with various initial values, to see how sensitive they
#' are to initial values.  Does only a few iterations for Newton and
#' method of scoring, just to see if they are converging or diverging.

init_list <- list (c(x1/m1,x2/m2),
                   c(0.5,0.5),
                   c(0.1,0.1),
                   c(0.05,0.95))

for (init in init_list) {
    cat ("\nTRYING INITIAL VALUE",init,"\n\n")
    cat("\nAlternating maximization\n\n")
    p_alt <- mle_alt (n,m1,m2,x,x1,x2,init)
    cat("\nMultivariate Newton iteration\n")
    p_mvn <- mle_mvn (n,m1,m2,x,x1,x2,init,7)
    cat("\nMethod of scoring\n")
    p_mos <- mle_mos (n,m1,m2,x,x1,x2,init,7)
    cat("\nUsing nlm\n\n")
    p_nlm <- mle_nlm (n,m1,m2,x,x1,x2,init)
    print(p_nlm)
}

#' Use the run with the first initial value above to get precise estimates.

init <- init_list[[1]]
p_alt <- mle_alt (n,m1,m2,x,x1,x2,init)
p_mvn <- mle_mvn (n,m1,m2,x,x1,x2,init,7)
p_mos <- mle_mos (n,m1,m2,x,x1,x2,init,17)
p_nlm <- mle_nlm (n,m1,m2,x,x1,x2,init)

print (rbind (alt=p_alt,mvn=p_mvn,mos=p_mos,nlm=p_nlm))

print (rbind (alt_log_likilhood=log_likelihood(p_alt,n,m1,m2,x,x1,x2),
              mvn_log_likilhood=log_likelihood(p_mvn,n,m1,m2,x,x1,x2),
              mos_log_likilhood=log_likelihood(p_mos,n,m1,m2,x,x1,x2),
              nlm_log_likilhood=log_likelihood(p_nlm,n,m1,m2,x,x1,x2)))

#' Find standard errors using the observed and Fisher information.

print (observed_inf <- -log_likelihood_hessian(p_alt,n,m1,m2,x,x1,x2))
print (fisher_inf <- fisher_information(p_alt,n,m1,m2,x,x1,x2))

print (sqrt (diag (solve (observed_inf))))
print (sqrt (diag (solve (fisher_inf))))

#' Try another data set in which the difference in standard errors obtained
#' in these two ways might be bigger.

x <- 125
x1 <- 5
x2 <- 15

print (p_alt <- mle_alt (n,m1,m2,x,x1,x2,c(0.5,0.5)))

print (observed_inf <- -log_likelihood_hessian(p_alt,n,m1,m2,x,x1,x2))
print (fisher_inf <- fisher_information(p_alt,n,m1,m2,x,x1,x2))

print (sqrt (diag (solve (observed_inf))))
print (sqrt (diag (solve (fisher_inf))))

#' Finally, try a data set in which the difference in standard errors obtained
#' in these two ways should be zero.

x <- 52
x1 <- 5
x2 <- 15

print (p_alt <- mle_alt (n,m1,m2,x,x1,x2,c(0.5,0.5)))

print (observed_inf <- -log_likelihood_hessian(p_alt,n,m1,m2,x,x1,x2))
print (fisher_inf <- fisher_information(p_alt,n,m1,m2,x,x1,x2))

print (sqrt (diag (solve (observed_inf))))
print (sqrt (diag (solve (fisher_inf))))
