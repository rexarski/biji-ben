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
        y <- p/n
        YN <- p/N
        d1 <- 1+(1-YN)/YN*log(1-YN)
        
        X <- rmvnorm(n, mu, Sigma)
        S <- cov(X)
        T1 <- sum(diag(S))-unlist(determinant(S,logarithm=T))[[1]]-p
        
        ts <- T1-p*d1
        
        X2 <- rmvnorm(n, mu, Sigma2)
        S2 <- cov(X2)
        T1.2 <- sum(diag(S2))-unlist(determinant(S2,logarithm=T))[[1]]-p
        
        ts.2 <- T1.2-p*d1
        
        table <- rbind(table,c(p,ts,1))
        table <- rbind(table,c(p,ts.2,2))
    }
}

Sys.time()-timer

names(table) <- c("p","ts","type")

large.summary <- data.frame()

for (pv in p.vec) {
    y <- pv/n
    mu1 <- -0.5*log(1-y)
    sigma1 <- sqrt(-2*log(1-y)-2*y)
    
    table.size <- table %>%
        filter(p==pv,type==1)
    table.power <- table %>%
        filter(p==pv,type==2)
    
    pv.size <- mean(table.size$ts>qnorm(.95,mu1,sigma1))
    pv.power <- mean(table.power$ts>qnorm(.95,mu1,sigma1))
    large.summary <- rbind(large.summary, c(pv, pv.size, pv.power))
}
names(large.summary) <- c("p", "size", "power")

large.summary