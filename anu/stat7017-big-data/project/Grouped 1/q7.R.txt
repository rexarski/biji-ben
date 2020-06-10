# q7

library(dplyr)
library(ggplot2)
library(mvtnorm)
library(reshape2)
library(readr)
library(ks)
library(vars)
library(portes)

set.seed(7017)

mts.gen.1 <- function(matrix.A, matrix.Sig, obs, method, viz=T, lag=0, add.S0=F, burnin=100, type="lag") {
    df <- data.frame()
    # epsilons <- NA
    if (method=="var") {
        epsilons <- rmvnorm((obs+burnin), c(0,0), matrix.Sig)
        Xt <- c(0,0)
        for (t in 1:(obs+burnin)) {
            Xt <- matrix.A%*%Xt + epsilons[t,]
            df <- rbind(df, c(Xt))
        }
        df <- df[(1+burnin):(obs+burnin),]
    } else if (method=="vma" || method=="ma") {
        epsilons <- rmvnorm(obs+burnin+1,c(0,0),matrix.Sig)
        for (t in 1:(obs+burnin)) {
            Xt <- epsilons[t+1,] + matrix.A%*%epsilons[t,]
            df <- rbind(df, c(Xt))
        }
        df <- df[(1+burnin):(obs+burnin),]
    }
    names(df) <- c("x1","x2")
    df$id <- (1+burnin):(obs+burnin)
    df2 <- melt(df, id.var = "id", variable.name = "x")
    if (viz) {
        print(ggplot(df2,aes(x=id,y=value)) + 
                  geom_line(aes(color=x)) + 
                  facet_grid(x ~ .) +
                  scale_colour_manual(values=c("#C83E45", "#5289B1")) +
                  theme_minimal())
    }
    if (lag>0) {
        if (type=="qm") {
            # if we conduct a portmanteau test on residuals, reassign the residual df to current variable df
            # mod=VAR(df,p=1,lag.max=20,ic="AIC")
            mod <- VAR(df,p=1,lag.max=20)
            df <- as.data.frame(cbind(mod$varresult$x1$residuals,mod$varresult$x2$residuals))
            names(df) <- c("x1","x2")
        }
        
        rho.tau <- list()
        X.bar <- c(mean(df$x1), mean(df$x2))
        # S0 <- 0
        # for (t in 1:obs) {
        #     S0 <- S0 + (c(df$x1[t], df$x2[t]) - X.bar) %*% t(c(df$x1[t], df$x2[t]) - X.bar)
        # }
        # S0 <- S0 / (obs-1)
        # S0 <- cov(df[1:obs,1:2])
        S0 <- cov(df[,1:2])
        D <- diag(1/sqrt(diag(S0)))
        
        # also record lag-0 autocovariance matrix, need to be used when doing portmanteau test
        if (add.S0) {
            # rho.tau[[lag+1]] <- D %*% S0 %*% D
            rho.tau[[lag+1]] <- cov2cor(S0)  # the same as D %*% S0 %*% D
        }
        
        for (tau in 1:lag) {
            Stau <- 0
            for (t in (tau+1):nrow(df)) {
                Stau <- Stau + (c(df$x1[t], df$x2[t]) - X.bar) %*% t(c(df$x1[t-tau],df$x2[t-tau]) - X.bar)
            }
            Stau <- Stau / (nrow(df)-1)
            print(dim(Stau))
            print(dim(D))
            print(dim(df))
            rho.tau[[tau]] <- D %*% Stau %*% D
        }
        
        # if (type=="lag") {
        #     return(rho.tau)
        # } else if (type=="qm") {
        #     return(epsilons)
        # }
        return(rho.tau)
    }
}

## (a) & (b) & (c) & (d)
A <- matrix(c(0.8,0.4,-0.3,0.6),byrow = T,ncol=2)
Sigma <- matrix(c(2,0.5,0.5,1),byrow = T,ncol=2)
mts.gen.1(A, Sigma, 300, "var", viz=T, lag=5, add.S0=F, burnin=100, type="lag")
mts.gen.1(A, Sigma, 300, "vma", viz=T, lag=2, add.S0=F, burnin=100, type="lag")

## (e)
A <- matrix(c(-.2, .3, -.6, 1.1), byrow = T, ncol=2)
B <- matrix(c(.4, .1, -1, .5), byrow = T, ncol=2)
C <- matrix(c(-1.5, 1.2, -.9, .5), byrow = T, ncol=2)
k <- 2 # 2 by 2 matrices
m <- 20
n <- 200
sim <- 1000

alpha.vec <- c(.25, -.25, .5, -.5, .75, -.75)

Delta.matrix <- function(alpha.value) {
    return(matrix(c(1, alpha.value, alpha.value, 1), byrow = T, ncol=2))
}

# kronecker(), vec()

inside.Qm <- function(rhol,rho0) {
    temp <- t(vec(t(rhol))) %*% kronecker(solve(rho0), solve(rho0)) %*% vec(t(rhol))
    return(unlist(temp)[[1]])
}

summary.table <- data.frame()

timer <- Sys.time()

summary.table <- data.frame()

for (i in 1:sim) {
    for (alpha in alpha.vec) {
        delta.matrix <- Delta.matrix(alpha)
        rho1 <- mts.gen.1(A, delta.matrix, n, "var", viz=F, lag=m, add.S0=T, type="qm")
        rho2 <- mts.gen.1(B, delta.matrix, n, "var", viz=F, lag=m, add.S0=T, type="qm")
        rho3 <- mts.gen.1(C, delta.matrix, n, "var", viz=F, lag=m, add.S0=T, type="qm")
        QA <- 0
        QB <- 0
        QC <- 0
        for (j in 1:m) {
            QA <- QA + inside.Qm(rho1[[j]], rho1[[m+1]])
            QB <- QB + inside.Qm(rho2[[j]], rho2[[m+1]])
            QC <- QC + inside.Qm(rho3[[j]], rho3[[m+1]])
        }
        QA <- n * QA
        QAs <- QA + k**2*m*(m+1)/(2*n)
        QB <- n * QB
        QBs <- QB + k**2*m*(m+1)/(2*n)
        QC <- n * QC
        QCs <- QC + k**2*m*(m+1)/(2*n)
        summary.table <- rbind(summary.table,
                               c(alpha, QA, QAs, QB, QBs, QC, QCs))
    }
}
Sys.time() - timer

names(summary.table) <- c("alpha", "QA", "QAs", "QB", "QBs", "QC", "QCs")

critical <- qchisq(.05,76,lower.tail = F)  # k^2(m-p-q) = 4 * (20 - 1 - 0) = 76

summary.table %>%
    mutate(QA = QA>critical,
           QAs = QAs>critical,
           QB = QB>critical,
           QBs = QBs>critical,
           QC = QC>critical,
           QCs = QCs>critical) %>%
    group_by(alpha) %>%
    summarize(
        A.Q20 = sum(QA),
        A.Q20.star = sum(QAs),
        B.Q20 = sum(QB),
        B.Q20.star = sum(QBs),
        C.Q20 = sum(QC),
        C.Q20.star = sum(QCs)
    )

# # A tibble: 6 x 7
# alpha A.Q20 A.Q20.star B.Q20 B.Q20.star C.Q20 C.Q20.star
# <dbl> <int>      <int> <int>      <int> <int>      <int>
# 1 -0.75    29         51    35         53    27         54
# 2 -0.5     29         50    19         37    28         56
# 3 -0.25    29         65    25         44    24         50
# 4  0.25    23         47    28         38    31         50
# 5  0.5     20         52    23         45    27         48
# 6  0.75    31         55    21         42    28         54

# NOTE 1: the original table in paper (1981) might have a serious typo, where "per cent" should actually be "count". Consider a test with typo 1 error about 50%. Since the simulation run has a valeu of 1000 instead of 100, I guess this in fact is the "count", which also explains why Qm* is better in the perspective of "closer to 0.05".
# 
# NOTE 2: the difference between our simulation and the original table might originate from the fact that we discard 100 observations in the implented function as burnin, while the paper didn't specifies their approach or their particular parameter.

## (f)



debt <- read.table("q-fdebt.txt",header = T) %>%
    select(hbfin, hbfrbn) %>%
    mutate(hbfin = log(hbfin), hbfrbn = log(hbfrbn))
debt <- as.matrix(debt)
DiffData <- matrix(numeric(ncol(debt) * (nrow(debt)-1)), ncol = ncol(debt))
for (i in 1:ncol(debt)) DiffData[, i] <- diff(log(debt[, i]), lag = 1)
Fit <- ar.ols(DiffData, aic=F, order.max = 1)

LiMcLeod(Fit, lags=1:10)

# Monte Carlo version
portest(Fit, lags=1:10, test="LiMcLeod", ncores=4)
