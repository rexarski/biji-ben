############################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 11 EXAMPLES (last update 10/1/2012)

############################################################################
### EXAMPLE 11.1-2 EASY DATA
############################################################################
# easy = observed data
# x    = observed predictor data
# y    = observed response data
# tma  = truncated neighborhood moving average (for k odd)
############################################################################

## INITIAL VALUES
easy = read.table(file.choose(),header=T)
x    = easy$X
y    = easy$Y

## FUNCTIONS
TMA = function(k,y){
      n = length(y)
      S = matrix(0,n,n)
      b = (k-1)/2
      if(k>1){
      for(i in 1:b){
            S[i,1:(b+i)] = 1/(k-b+i-1)
            S[n-i+1,(n-b-i+1):n] = 1/(k-b+i-1)
      }
      for(i in (b+1):(n-b)){
            S[i,(i-b):(i+b)] = 1/k
      }}
      if(k==1){S = diag(1,n)}
      out = S%*%y
      return(out)
}

## MAIN
s3  = TMA(3,y)
s13 = TMA(13,y)
s43 = TMA(43,y)

## OUTPUT PLOTS
s = function(x){(x^3) * sin((x+3.4)/2)}
x.plot = seq(min(x),max(x),length.out=1000)
y.plot = s(x.plot)
plot(x,y,xlab="Predictor",ylab="Response")
lines(x.plot,y.plot,lty=2)
lines(x,s3)
lines(x,s13,lty=3)
lines(x,s43,lty=5)
legend("bottomright",c("True relation","k=3","k=13","k=43"),
      lty=c(2,1,3,5))


############################################################################
### EXAMPLE 11.3 EASY DATA (CVRSS)
############################################################################
# easy  = observed data
# x     = observed predictor data
# y     = observed response data
# CVRSS = computes CVRSS for truncated neighborhood 
#         moving average (for k odd > 1)
############################################################################

## INITIAL VALUES
easy = read.table(file.choose(),header=T)
x    = easy$X
y    = easy$Y
k    = seq(3,51,by=2)

## FUNCTIONS
CVRSS = function(k,y){
      n = length(y)
      S = matrix(0,n,n)
      b = (k-1)/2
      if(k>1){
      for(i in 1:b){
            S[i,1:(b+i)] = 1/(k-b+i-1)
            S[n-i+1,(n-b-i+1):n] = 1/(k-b+i-1)
      }
      for(i in (b+1):(n-b)){
            S[i,(i-b):(i+b)] = 1/k
      }}
      if(k==1){S = diag(1,n)}
      s.hat = S%*%y
      out = sum(((y-s.hat)/(1-diag(S)))^2)
      return(out)
}

## MAIN
cvrss.val = rep(0,length(k))
for(i in 1:25){
      cvrss.val[i] = CVRSS(k[i],y)
}

## OUTPUT
cvrss.val      # CVRSS VALUES FOR k = 3,5,7,...,51

## OUTPUT PLOTS
plot(k,cvrss.val,type="b")


############################################################################
### EXAMPLE 11.4 EASY DATA (RUNNING-LINE SMOOTH)
############################################################################
# easy      = observed data
# x         = observed predictor data
# y         = observed response data
# k         = smoothing parameter
# RLSMOOTH1 = running-line smoother (for k odd > 1)
# RLSMOOTH2 = running-line smoother (for k odd > 1)
############################################################################
## NOTES
# The following has two implementations for the running-line smoother. 
# The first builds the hat matrix for each neighborhood while the second
# uses the sufficient statistics for regression to reduce computations.
############################################################################

## INITIAL VALUES
easy = read.table(file.choose(),header=T)
x    = easy$X
y    = easy$Y
k    = 23

## FUNCTIONS
# USES HAT MATRIX
RLSMOOTH1 = function(k,y,x){
      n = length(y)
      s.hat = rep(0,n)
      b = (k-1)/2
      if(k>1){
      for(i in 1:(b+1)){
            xi = x[1:(b+i)]
            xi = cbind(rep(1,length(xi)),xi)
            hi = xi%*%solve(t(xi)%*%xi)%*%t(xi)
            s.hat[i] = y[1:(b+i)]%*%hi[i,]

            xi = x[(n-b-i+1):n]
            xi = cbind(rep(1,length(xi)),xi)
            hi = xi%*%solve(t(xi)%*%xi)%*%t(xi)
            s.hat[n-i+1] = y[(n-b-i+1):n]%*%hi[nrow(hi)-i+1,]
      }
      for(i in (b+2):(n-b-1)){
            xi = x[(i-b):(i+b)]
            xi = cbind(rep(1,length(xi)),xi)
            hi = xi%*%solve(t(xi)%*%xi)%*%t(xi)
            s.hat[i] = y[(i-b):(i+b)]%*%hi[b+1,]
      }}
      if(k==1){s.hat = y}
      return(s.hat)
}
# USES SUFFICIENT STATISTICS
RLSMOOTH2 = function(k,y,x){
      if(k>1){
      n = length(y)
      s.hat = rep(0,n)
      b = (k-1)/2
      x.bar = mean(x[1:(b+1)])
      y.bar = mean(y[1:(b+1)])
      xy.bar = mean(x[1:(b+1)]*y[1:(b+1)])
      x2.bar = mean(x[1:(b+1)]^2)
      beta1 = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
      s.hat[1] = y.bar + beta1*(x[1]-x.bar)
      for(i in 2:(b+1)){
            x.bar  = (x.bar*(i+b-1) + x[i+b])/(i+b)
            y.bar  = (y.bar*(i+b-1) + y[i+b])/(i+b)
            xy.bar = (xy.bar*(i+b-1) + x[i+b]*y[i+b])/(i+b)
            x2.bar = (x2.bar*(i+b-1) + (x[i+b]^2))/(i+b)
            beta1  = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
            s.hat[i] = y.bar + beta1*(x[i]-x.bar)
      }
      for(i in (b+2):(n-b)){
            x.bar = x.bar + (x[i+b] - x[i-b-1])/k
            y.bar = y.bar + (y[i+b] - y[i-b-1])/k
            xy.bar = xy.bar + (x[i+b]*y[i+b] - x[i-b-1]*y[i-b-1])/k
            x2.bar = x2.bar + ((x[i+b]^2)-(x[i-b-1]^2))/k
            beta1 = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
            s.hat[i] = y.bar + beta1*(x[i]-x.bar)
      }
      for(i in (n-b+1):n){
            x.bar  = (x.bar*(k-i+n-b+1) - x[i-b-1])/(k-i+n-b)
            y.bar  = (y.bar*(k-i+n-b+1) - y[i-b-1])/(k-i+n-b)
            xy.bar = (xy.bar*(k-i+n-b+1) - x[i-b-1]*y[i-b-1])/(k-i+n-b)
            x2.bar = (x2.bar*(k-i+n-b+1) - (x[i-b-1]^2))/(k-i+n-b)
            beta1  = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
            s.hat[i] = y.bar + beta1*(x[i]-x.bar)
      }
      }
      if(k==1){s.hat = y}
      return(s.hat)
}

## MAIN
rlsmooth1.val = RLSMOOTH1(k,y,x)
rlsmooth2.val = RLSMOOTH2(k,y,x)

## OUTPUT PLOTS
s = function(x){(x^3) * sin((x+3.4)/2)}
x.plot = seq(min(x),max(x),length.out=1000)
y.plot = s(x.plot)
plot(x,y,xlab="Predictor",ylab="Response")
lines(x.plot,y.plot,lty=2)
lines(x,rlsmooth2.val,type="l")


############################################################################
### EXAMPLE 11.5 EASY DATA (KERNEL SMOOTH)
############################################################################
# easy    = observed data
# x       = observed predictor data
# y       = observed response data
# h       = bandwidth
# fx.hat  = normal kernel density
# KSMOOTH = kernel smoother (for k odd > 1)
############################################################################

## INITIAL VALUES
easy = read.table(file.choose(),header=T)
x    = easy$X
y    = easy$Y
h    = 0.16

## FUNCTIONS
fx.hat = function(z,h){dnorm((z-x)/h)/h}
KSMOOTH = function(h,y,x){
      n = length(y)
      s.hat = rep(0,n)
      for(i in 1:n){
            a = fx.hat(x[i],h)
            s.hat[i] = sum(y * a/sum(a))
      }
      return(s.hat)
}

## MAIN
ksmooth.val = KSMOOTH(h,y,x)

## OUTPUT PLOTS
s = function(x){(x^3) * sin((x+3.4)/2)}
x.plot = seq(min(x),max(x),length.out=1000)
y.plot = s(x.plot)
plot(x,y,xlab="Predictor",ylab="Response")
lines(x.plot,y.plot,lty=2)
lines(x,ksmooth.val,type="l")


############################################################################
### EXAMPLE 11.6 EASY DATA (SPLINE SMOOTH)
############################################################################
# easy    = observed data
# x       = observed predictor data
# y       = observed response data
############################################################################
## NOTES
# The following uses the smooth.spline function in R which has a 
# different implementation of the smoothing parameter than S-PLUS,
# the programming language used originally for some of the examples
# in the first edition.  Thus the lambdas differ.
############################################################################

## INITIAL VALUES
easy = read.table(file.choose(),header=T)
x    = easy$X
y    = easy$Y

## MAIN
s.hat = smooth.spline(x=x,y=y)

## OUTPUT
s.hat      # SMOOTH.SPLINE OUTPUT

## OUTPUT PLOTS
s = function(x){(x^3) * sin((x+3.4)/2)}
x.plot = seq(min(x),max(x),length.out=1000)
y.plot = s(x.plot)
plot(x,y,xlab="Predictor",ylab="Response")
lines(x.plot,y.plot,lty=2)
lines(s.hat)


############################################################################
### EXAMPLE 11.7 EASY DATA (LOESS)
############################################################################
# easy = observed data
# x    = observed predictor data
# y    = observed response data
# k    = smoothing parameter
############################################################################
## NOTES
# The following uses the lowess function. The loess function may also be
# used, however it does has a different implementation and defaults.
############################################################################

## INITIAL VALUES
easy = read.table(file.choose(),header=T)
x    = easy$X
y    = easy$Y
n    = length(y)
k    = 30

## MAIN
s.hat = lowess(x=x,y=y,f=k/n)

## OUTPUT
s.hat      # LOESS OUTPUT

## OUTPUT PLOTS
s = function(x){(x^3) * sin((x+3.4)/2)}
x.plot = seq(min(x),max(x),length.out=1000)
y.plot = s(x.plot)
plot(x,y,xlab="Predictor",ylab="Response")
lines(x.plot,y.plot,lty=2)
lines(s.hat)


############################################################################
### EXAMPLE 11.8 DIFFICULT DATA (SUPERSMOOTHER)
############################################################################
# tough       = observed data
# x           = observed predictor data
# y           = observed response data
# h           = smoothing parameters
# RLSMOOTH    = running-line smoother (for h odd > 1)
############################################################################
## NOTES
# This example uses the supersmoother implemented in R via the
# "supsmu" function. See the ?supsmu help page for more information.
############################################################################

## INITIAL VALUES
tough = read.table(file.choose(),header=T)
x     = tough$X
y     = tough$Y
n     = length(y)
h     = c(0.05*n, 0.2*n, 0.5*n)

## FUNCTION (running lines smoother).  The supersmoother is called
## using supsmu()

RLSMOOTH = function(k,y,x){
      if(k>1){
      n = length(y)
      s.hat = rep(0,n)
      b = (k-1)/2
      x.bar = mean(x[1:(b+1)])
      y.bar = mean(y[1:(b+1)])
      xy.bar = mean(x[1:(b+1)]*y[1:(b+1)])
      x2.bar = mean(x[1:(b+1)]^2)
      beta1 = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
      s.hat[1] = y.bar + beta1*(x[1]-x.bar)
      for(i in 2:(b+1)){
            x.bar  = (x.bar*(i+b-1) + x[i+b])/(i+b)
            y.bar  = (y.bar*(i+b-1) + y[i+b])/(i+b)
            xy.bar = (xy.bar*(i+b-1) + x[i+b]*y[i+b])/(i+b)
            x2.bar = (x2.bar*(i+b-1) + (x[i+b]^2))/(i+b)
            beta1  = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
            s.hat[i] = y.bar + beta1*(x[i]-x.bar)
      }
      for(i in (b+2):(n-b)){
            x.bar = x.bar + (x[i+b] - x[i-b-1])/k
            y.bar = y.bar + (y[i+b] - y[i-b-1])/k
            xy.bar = xy.bar + (x[i+b]*y[i+b] - x[i-b-1]*y[i-b-1])/k
            x2.bar = x2.bar + ((x[i+b]^2)-(x[i-b-1]^2))/k
            beta1 = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
            s.hat[i] = y.bar + beta1*(x[i]-x.bar)
      }
      for(i in (n-b+1):n){
            x.bar  = (x.bar*(k-i+n-b+1) - x[i-b-1])/(k-i+n-b)
            y.bar  = (y.bar*(k-i+n-b+1) - y[i-b-1])/(k-i+n-b)
            xy.bar = (xy.bar*(k-i+n-b+1) - x[i-b-1]*y[i-b-1])/(k-i+n-b)
            x2.bar = (x2.bar*(k-i+n-b+1) - (x[i-b-1]^2))/(k-i+n-b)
            beta1  = (xy.bar - x.bar*y.bar)/(x2.bar - x.bar^2)
            s.hat[i] = y.bar + beta1*(x[i]-x.bar)
      }
      }
      if(k==1){s.hat = y}
      return(s.hat)
}

## MAIN
ssmooth.val  = supsmu(x,y)
rlsmooth.val = mapply(RLSMOOTH,h+1,MoreArgs = list(y,x))

## OUTPUT PLOTS
par(mfrow=c(1,2))
plot(x,y,xlab="Predictor",ylab="Response",main="Running-line Smooths")
lines(x,rlsmooth.val[,1],type="l")
lines(x,rlsmooth.val[,2],type="l",lty=2)
lines(x,rlsmooth.val[,3],type="l",lty=3)
legend("bottomright",c("k=0.05n","k=0.2n","k=0.5n"),lty=1:3)

plot(x,y,xlab="Predictor",ylab="Response",main="Supersmooth")
lines(ssmooth.val)

############################################################################
### EXAMPLE 11.9 - 11.11 CONFIDENCE REGIONS
############################################################################
# smoothdat.x, smoothdat.y = data for smoothing
# S = smoothing matrix
# yhat = original smooth estimate
# boot.yhat = bootstrap smooths
############################################################################
## NOTES
# Edition 1 did not include the data for this example.  They are
# below.
############################################################################

##INITIAL VALUES
cbsmooth=read.table(file.choose(),header=T)
smoothdat.y = cbsmooth$y
smoothdat.x = cbsmooth$x

##CONSTRUCT RUNNING-LINE SMOOTHING MATRIX	
##Span of 15 chosen by cross-validation of scatter.smooth()
s = 7  #span = 2*s+1
S = matrix(0,50,50)
for (i in 1:50) {
     lo=max(1,i-s) ; hi=min(50,i+s)
     design.mat=cbind(1,smoothdat.x[lo:hi])
     h=design.mat%*%solve(t(design.mat)%*%design.mat)%*%t(design.mat)
     where=ifelse(i<26-s-1,dim(h)[2]-s,s+1)
     S[i,lo:hi]=h[where,] 
}
yhat = S%*%cbind(smoothdat.y)
resids = smoothdat.y-yhat

#Note: qr(S%*%t(S))$rank is 47 so watch out for inverting

##BOOTSTRAP
boot.yhat=matrix(0,nrow=50,ncol=1000) 
for (i in 1:1000) {
     newfit=yhat+sample(resids,50,replace=T)
     boot.yhat[,i]=S%*%cbind(newfit)
}
pointwise.lower=apply(boot.yhat,1,quantile,.025)
pointwise.upper=apply(boot.yhat,1,quantile,.975)

##INFLATION METHOD
#Used bisection to search for correct omega. Result below. 
omega=1.61   
Lhat=yhat-pointwise.lower
Uhat=pointwise.upper-yhat
adj.pointwise.lower=yhat-omega*Lhat
adj.pointwise.upper=yhat+omega*Uhat
is.completely.within=function(yhat,lo,up) {
  all(yhat>=lo & yhat<=up) 
}
number.within=apply(boot.yhat,2,is.completely.within,
     lo=adj.pointwise.lower,up=adj.pointwise.upper)
sum(number.within)/1000

##SUPERIMPOSITION METHOD
##Using same span as above
s.hat.star=matrix(0,nrow=50,ncol=1000) 
v.star=rep(0,1000)
eigen.decomp=eigen(S%*%t(S))
SST.inv=eigen.decomp$vectors%*%diag(1/eigen.decomp$values)%*%
           t(eigen.decomp$vectors)
denom=50-2*sum(diag(S))+sum(diag(S%*%t(S)))

for (i in 1:1000) {
     ystar=yhat+sample(resids,50,replace=T)
     s.hat.star[,i]=S%*%cbind(ystar)
     sigma2.hat=sum((s.hat.star[,i]-ystar)^2)/denom 
     v.star[i]=t(cbind(s.hat.star[,i]-ystar))%*%SST.inv%*%
               rbind(s.hat.star[,i]-ystar)/sigma2.hat
}

sorting=(1:1000)[order(v.star)]
s.hat.star=s.hat.star[,sorting]
v.star=sort(v.star)

###OUTPUT GRAPHS
plot(smoothdat.x,smoothdat.y)
lines(smoothdat.x,yhat,lwd=2)
polygon(c(smoothdat.x,rev(smoothdat.x)),c(pointwise.lower,rev(pointwise.upper)),
     density=-1,col=grey(.7),border=NA)
lines(c(min(smoothdat.x),max(smoothdat.x)),-c(.00,.00),lty=2)
points(smoothdat.x,smoothdat.y,pch=16)
lines(smoothdat.x,adj.pointwise.upper,lty=2)
lines(smoothdat.x,adj.pointwise.lower,lty=2)

plot(smoothdat.x,smoothdat.y)
lines(smoothdat.x,yhat,lwd=2)
polygon(c(smoothdat.x,rev(smoothdat.x)),c(pointwise.lower,rev(pointwise.upper)),
     density=-1,col=grey(.7),border=NA)
lines(c(min(smoothdat.x),max(smoothdat.x)),-c(.00,.00),lty=2)
points(smoothdat.x,smoothdat.y,pch=16)
for (i in seq(25,975,by=50)) {
     lines(smoothdat.x,s.hat.star[,i]) }



############################################################################
### END OF FILE
