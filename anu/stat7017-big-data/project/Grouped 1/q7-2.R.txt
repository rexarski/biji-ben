set.seed(7017)

fun1 <- function(matrix.A, matrix.Sig, obs, burnin=100) {
    df <- data.frame()
    epsilons.var <- rmvnorm((obs+burnin), c(0,0), matrix.Sig)
    Xt <- c(0,0)
    for (t in 1:(obs+burnin)) {
        Xt <- matrix.A%*%Xt + epsilons.var[t,]
        df <- rbind(df, c(Xt))
    }
    df <- df[(1+burnin):(obs+burnin),]
    names(df) <- c("x1","x2")
    return(df)
}

fun2 <- function(df,lag) {
    var=VAR(df,lag.max=1,ic="AIC")
    
    res <- as.data.frame(cbind(var$varresult$x1$residuals,var$varresult$x2$residuals))
    names(res) <- c("x1","x2")
    
    if (lag>0) {
        rho.tau <- list()
        # S.list <- list()
        
        X.bar <- c(mean(res$x1), mean(res$x2))
        S0 <- 0
        # rho0 <- matrix(rep(0,4),ncol=2)
        obs=nrow(res)
        for (t in 1:obs) {
            S0 <- S0 + (c(res$x1[t], res$x2[t]) - X.bar) %*% t(c(res$x1[t], res$x2[t]) - X.bar)
            # also record lag-0 autocorrelation matrix, need to be used when doing portmanteau test
            # rho0 <- rho0 + c(df$x1[t], df$x2[t]) %*% t(c(df$x1[t], df$x2[t])) * 2
        }
        
        S0 <- S0 / (obs-1)
        
        D <- diag(1/sqrt(diag(S0)))
        
        rho.tau[[lag+1]] <- D %*% S0 %*% D   
        
        for (tau in 1:lag) {
            Stau <- 0
            for (t in (tau+1):obs) {
                # correction:
                Stau <- Stau + (c(res$x1[t], res$x2[t]) - X.bar) %*% t(c(res$x1[t-tau],res$x2[t-tau]) - X.bar)
            }
            Stau <- Stau / (obs-1)
            # S.list[[tau]] <- Stau
            rho.tau[[tau]] <- D %*% Stau %*% D
        }
        
        # if (add.S0) {
        #     return(S.list)
        # } else {
        #     return(rho.tau)    
        # }
        return(rho.tau)
    }
}



A <- matrix(c(-.2, .3, -.6, 1.1), byrow = T, ncol=2)
B <- matrix(c(.4, .1, -1, .5), byrow = T, ncol=2)
C <- matrix(c(-1.5, 1.2, -.9, .5), byrow = T, ncol=2)

k <- 2 # 2 by 2 matrices?
m <- 20
n <- 200
sim <- 1000

alpha.vec <- c(.25, -.25, .5, -.5, .75, -.75)
# alpha.vec <- c(.25)

summary.table <- data.frame()

for (i in 1:sim) {
    for (alpha in alpha.vec) {
        delta.matrix <- Delta.matrix(alpha)
        df1 <- fun1(A, delta.matrix, n)
        df2 <- fun1(B, delta.matrix, n)
        df3 <- fun1(C, delta.matrix, n)
        rho1 = fun2(df1, m)
        rho2 = fun2(df2, m)
        rho3 = fun2(df3, m)
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
        A.Q20 = mean(QA),
        A.Q20.star = mean(QAs),
        B.Q20 = mean(QB),
        B.Q20.star = mean(QBs),
        C.Q20 = mean(QC),
        C.Q20.star = mean(QCs)
    )

