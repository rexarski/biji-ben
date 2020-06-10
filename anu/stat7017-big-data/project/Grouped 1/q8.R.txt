library(dplyr)
library(ggplot2)
library(ggfortify)
library(forecast)
library(vars)

# remove zoo

set.seed(7017)

# (a)

dat <- read.table("m-cpitb3m.txt",header = T) %>%
    dplyr::select(tb=tb3m, cpi=cpiaucsl) %>%
    mutate(cpi=100*log(cpi))

dat <- diff(ts(dat,frequency = 12,start = c(1947,1)))

autoplot(dat) +
    scale_colour_manual(values=c("#C83E45", "#5289B1")) +
    theme_minimal()

# (b)

# library(MTS)
# MTS::VARorder(dat,maxp=10)


VARorder2 <- function (x, P = 10) {
    x1 <- as.matrix(x)
    T <- nrow(x1)
    k <- ncol(x1)
    if (P < 1) {P = 1}
    obs = T - P
    y = x1[(P + 1):T, , drop = FALSE]
    ist = P + 1
    xmtx = cbind(rep(1, obs), x1[P:(T - 1), ])
    if (P > 1) {
        for (i in 2:P) {
            xmtx = cbind(xmtx, x1[(ist - i):(T - i), ])
        }
    }
    chidet = rep(0, (P + 1))
    s = cov(y) * (obs - 1)/obs
    chidet[1] = log(det(s))
    y = as.matrix(y)
    for (l in 1:P) {
        idm = k * l + 1
        xm = xmtx[, 1:idm]
        xm = as.matrix(xm)
        xpx <- crossprod(xm, xm)
        xpy <- crossprod(xm, y)
        beta <- solve(xpx, xpy)
        yhat <- xm %*% beta
        resi <- y - yhat
        sse <- crossprod(resi, resi)/obs
        d1 = log(det(sse))
        chidet[l + 1] = d1
    }
    Mstat = rep(0, P)
    pv = rep(0, P)
    for (j in 1:P) {
        Mstat[j] = (T - P - k * j - 1.5) * (chidet[j] - chidet[j + 1])
        pv[j] = 1 - pchisq(Mstat[j], k ** 2)
    }
    
    output = cbind(c(0:P), c(0, Mstat), c(0, pv))
    colnames(output) <- c("l", "M(l)", "p-value")
    
    # which m? i.e. starting from this l=m, the p-value of following models
    # should all be greater than 0.05
    
    m.output <- 1
    
    for (m in 1:nrow(output)) {
        if (all(output[m:nrow(output),3] >= 0.05)) {
            m.output <- m
            break()
        }
    }
    print(round(output, 3))
    cat("Select VAR (", m.output-1, ")")
}

VARorder2(dat, 50)

# (c)

library(tsDyn)

# B1<-matrix(c(0.7, 0.2, 0.2, 0.7), 2)
# var1 <- VAR.sim(B=B1, n=100, include="none")
# # ts.plot(var1, type="l", col=c(1,2))
# VARorder2(var1, P=30)

increase.dim <- function(data, p) {
    dat.p <- dat
    # dim 3 to p
    for (dim.p in 3:p) {
        dat.p <- cbind(dat.p, sample(dat[,sample(1:2, 1, prob=c(0.5,0.5))],
                                     nrow(dat), replace=T))
    }
    dim(dat.p)
    mod <- lineVar(dat.p, lag=1)
    new.mod <- VAR.boot(mod, "resample")
    VARorder2(new.mod, P=20)
}

increase.dim(dat, 10)
increase.dim(dat, 20)
increase.dim(dat, 30)
increase.dim(dat, 40)  # computationally singular
increase.dim(dat, 50)  # computationally singular
