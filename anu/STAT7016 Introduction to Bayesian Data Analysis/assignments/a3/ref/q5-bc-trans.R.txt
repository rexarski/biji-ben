set.seed(123)
library(LearnBayes)
fun <- function(theta, y){
  lambda <- theta[1]
  mu <- theta[2]
  sigma <- exp(theta[3])
  r <- sum(dnorm((y^lambda - 1)/lambda, mu, sigma, log = T) +
          (lambda - 1) * log(y))
}
y <- c(13, 52, 6, 40, 10, 7, 66, 10, 10, 14, 16, 4, 
       65, 5, 11, 10, 15, 5, 76, 56, 88, 24, 51, 4, 
       40, 8, 18, 5, 16, 50, 40, 1, 36, 5, 10, 91, 
       18, 1, 18, 6, 1, 23, 15, 18, 12, 12, 17, 3)

fit <- laplace(fun, mode = c(0.1, 3, 0.5), y)


proposal <- list(var = fit$var, scale = 2)
r1 <- rwmetrop(fun, proposal, start = fit$mode, m = 10000, y)

proposal <- list(mu = fit$mode, var = fit$var)
proposal <- list(mu = fit$mode, var = diag(diag(fit$var)))
r2 <- indepmetrop(fun, proposal, start = fit$mode, m = 10000, y)

r3 <- gibbs(fun, start = fit$mode, m = 10000, 
                  scale = 2*diag(fit$var)^0.5, y)

canshu1 <- cbind(r1$par[, 1:2], exp(r1$par[, 3]))
canshu2 <- cbind(r2$par[, 1:2], exp(r2$par[, 3]))
canshu3 <- cbind(r3$par[, 1:2], exp(r3$par[, 3]))


apply(canshu1, 2, quantile, c(0.05, 0.95))
apply(canshu2, 2, quantile, c(0.05, 0.95))
apply(canshu3, 2, quantile, c(0.05, 0.95))


apply(canshu1, 2, mean)
apply(canshu2, 2, mean)
apply(canshu3, 2, mean)

xyplot(mcmc(r1$par))
xyplot(mcmc(r2$par))
xyplot(mcmc(r3$par))