library(mvtnorm)
library(ggplot2)
library(readr)
library(dplyr)
library(heplots)


set.seed(7017)

n <- 500
p.vec <- c(5, 10, 50, 100, 300, 375)
N <- n - 1
sim <- 200

table <- data.frame()

timer <- Sys.time()

for (i in 1:length(p.vec)) {
    p <- p.vec[i]
    mu <- rep(0, p)
    Sigma <- diag(p)
    Sigma2 <- diag(.05,p)
    Sigma2[1,1] <- 1
    
    for (s in 1:sim) {
        X <- rmvnorm(n, mu, Sigma)
        S <- cov(X)
        
        rho <- 1-(2*p**2+3*p-1)/(6*(n-1)*(p+1))
        ts <- -2*rho*(0.5*p*N + (0.5*N) * 
                          (unlist(determinant(S,logarithm=T))[[1]]-sum(diag(S))))
        
        X2 <- rmvnorm(n, mu, Sigma2)
        S2 <- cov(X2)
        ts2 <- -2*rho*(0.5*p*N + (0.5*N) * 
                           (unlist(determinant(S2,logarithm=T))[[1]]-sum(diag(S2))))
        
        table <- rbind(table,c(p,ts,1))
        table <- rbind(table,c(p,ts2,2))
    }
}

Sys.time()-timer

names(table) <- c("p","ts","type")

large.summary <- data.frame()
for (pv in p.vec) {
    table.size <- table %>%
        filter(p==pv,type==1)
    table.power <- table %>%
        filter(p==pv,type==2)
    
    f <- 0.5*pv*(pv+1)
    gamma2 <- pv*(2*pv**4+6*pv**3+pv**2-12*pv-13)/(288*(pv+1))
    rho <- 1-(2*pv**2+3*pv-1)/(6*(n-1)*(pv+1))
    
    pv.size <- mean(table.size$ts>(
        qchisq(.95,f)+gamma2/rho**2/N**2*(qchisq(.95,f+4)-qchisq(.95,f))))
    pv.power <- mean(table.power$ts>(
        qchisq(.95,f)+gamma2/rho**2/N**2*(qchisq(.95,f+4)-qchisq(.95,f))))
    large.summary <- rbind(large.summary, c(pv, pv.size, pv.power))
}
names(large.summary) <- c("p", "size", "power")

large.summary

# p  size power
# 1   5 0.040     1
# 2  10 0.060     1
# 3  50 0.060     1
# 4 100 0.045     1
# 5 300 0.280     1
# 6 375 0.970     1