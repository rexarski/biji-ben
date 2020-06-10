library(mvtnorm)
library(ggplot2)

set.seed(7017)

ps <- c(20,50)
ratios <- c(.5, 1)
taus <- c(0,1,2)

lag.sample.acf <- function(n, tau, X) {
    if (tau==0) {
        return(cov(X))
    } else {
        Ctau <- 0
        for (t in 1:(n-tau)) {
            Ctau <- Ctau + X[t,] %*% t(X[t+tau,]) + X[t+tau,] %*% t(X[t,])
        }
        Ctau <- Ctau/(2*n)
        return(Ctau)
    }
}

df <- data.frame()
for (ratio in ratios) {
    for (tau in taus){
        for (p in ps) {
            n <- p / ratio
            
            # draw the ESDs for iid
            Z <- rmvnorm(n,mean=rep(0,p),sigma=diag(p))
            # S <- cov(Z)
            S <- lag.sample.acf(n, tau, Z)
            ev <- eigen(S)$values

            F_ <- function(x) {
                total <- 0.
                for (i in 1:p) {
                    if (ev[i] <= x){
                        total <- total + 1
                    }
                }
                return(total/p)
            }
            empirical.cdf <- Vectorize(F_)

            df <- rbind(df, data.frame(p=rep(p,n),
                                       ratio=rep(ratio,n),
                                       tau=rep(tau, n),
                                       x=ev,
                                       Fvalue=empirical.cdf(ev),
                                       type=rep(paste("ESD.iid p =",p),n)))

            # draw the ESDs for MA(1)
            A1 <- diag(ncol(Z))
            Z.copy <- Z
            Z.copy <- cbind(rep(1,ncol(Z.copy)), Z.copy[,1:(ncol(Z.copy)-1)])
            X <- Z+Z.copy
            ev2 <- eigen(lag.sample.acf(n, tau, X))$values
            df <- rbind(df, data.frame(p=rep(p,n),
                                       ratio=rep(ratio,n),
                                       tau=rep(tau, n),
                                       x=ev2,
                                       Fvalue=empirical.cdf(ev2),
                                       type=rep(paste("ESD.MA(1) p =",p),n)))


            # draw the LSD for iid
            pp <- 500
            nn <- pp / ratio
            Zn <- rmvnorm(nn,mean=rep(0,pp),sigma=diag(pp))
            Sn <- lag.sample.acf(nn,tau,Zn)
            evn <- eigen(Sn)$values

            df <- rbind(df, data.frame(p=rep(pp,length(evn)),
                                       ratio=rep(ratio,length(evn)),
                                       tau=rep(tau,length(evn)),
                                       x=evn,
                                       Fvalue=empirical.cdf(evn),
                                       type=rep("LSD.iid",length(evn))))

            # draw the LSD for MA(1)
            A1n <- diag(ncol(Zn))
            Zn.copy <- Zn
            Zn.copy <- cbind(rep(1,ncol(Zn.copy)), Zn.copy[,1:(ncol(Zn.copy)-1)])
            Xn <- Zn+Zn.copy
            ev2n <- eigen(lag.sample.acf(length(evn), tau, Xn))$values
            df <- rbind(df, data.frame(p=rep(pp,length(ev2n)),
                                       ratio=rep(ratio,length(ev2n)),
                                       tau=rep(tau, length(ev2n)),
                                       x=ev2n,
                                       Fvalue=empirical.cdf(ev2n),
                                       type=rep("LSD.MA(1)",length(ev2n))))
        }
    }
}

# plotting 

df$para <- paste("tau = ", df$tau, "p/n = ", df$ratio)
ggplot(df, aes(x=x, y=Fvalue, color=type)) +
    stat_ecdf(geom = "step", size=.5, alpha=.8) +
    facet_wrap(para ~ ., nrow=3, strip.position = "bottom") +
    scale_x_continuous(limits = c(-3,6)) +
    scale_y_continuous(limits = c(0,1)) +
    scale_color_manual(values=c("LSD.iid" = "red", 
                                "LSD.MA(1)" = "black", 
                                "ESD.iid p = 20" = "blue",
                                "ESD.MA(1) p = 20" = "chartreuse", 
                                "ESD.iid p = 50" = "cadetblue",
                                "ESD.MA(1) p = 50" = "orange")) +
    theme_minimal()
