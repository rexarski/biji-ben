############################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 10 EXAMPLES (last update 10/1/2012)

############################################################################
### EXAMPLE 10.1 BIMODAL DENSITY
############################################################################
# bimodal.dat = contains data
# y           = observed data
# h           = bandwiths
# x           = sequence of points for plotting
# d           = kernel density estimates
# f.hat       = kernel density estimator
############################################################################
## NOTES
# The base stats package and the R package {MASS} both contain a wide 
# variety of the techniques used in this chapter and are usually simpler 
# approaches than directly programming a method. See the ?density help 
# page for more information.
# If using the bandwidth selectors in MASS, please note that they are 
# scaled and will give values four times larger.
# i.e.:  bw.ucv(y) = ucv(y)/4 
############################################################################

## INITIAL VALUES
bimodal.dat = read.table(file.choose())
y = bimodal.dat$V1
h = c(0.3, 0.625, 1.875)
x = seq(min(y)-sd(y), max(y)+sd(y), length.out=1000)
d = matrix(0,length(x),length(h))

## FUNCTIONS
f.hat = function(x,h){mean(dnorm((x-y)/h))/h}

## MAIN
for(i in 1:3){d[,i] = mapply(f.hat,x,h[i])}

## OUTPUT PLOTS
hist(y,breaks=20,freq=FALSE, xlim=c(min(x),max(x)))
lines(x,d[,1])
lines(x,d[,2],lwd=2)
lines(x,d[,3],lty=2)


############################################################################
### EXAMPLE 10.2 WHALE MIGRATION
############################################################################
# whalemigration.dat = contains data
# y                  = observed data
# PL                 = pseudo-loglikelihood evaluated at h
############################################################################
## NOTES
# The base stats package and the R package {MASS} both contain a wide 
# variety of the techniques used in this chapter and are usually simpler 
# approachs than directly programming a method. See the ?density help 
# page for more information.
# If using the bandwidth selectors in MASS, please note that they are 
# scaled and will give values four times larger.
# i.e.:  bw.ucv(y) = ucv(y)/4 
############################################################################

## INITIAL VALUES
whalemigration.dat = read.table(file.choose())
y = whalemigration.dat$V1

## FUNCTIONS
PL = function(h){
      pseudo.lik = NULL
      for(i in 1:length(y)){
            pseudo.lik[i] = mean(dnorm((y[i]-y[-i])/h))/h
      }
return(sum(log(pseudo.lik)))
}

## MAIN
h.pl  = optimize(PL,interval=c(0,100),maximum=T)$max
h.ucv = bw.ucv(y)
h.bcv = bw.bcv(y)
d.pl  = density(y, bw=h.pl,  kernel="gaussian")
d.ucv = density(y, bw=h.ucv, kernel="gaussian")
d.bcv = density(y, bw=h.bcv, kernel="gaussian")

## OUTPUT
h.pl       # MAX PSEUDO-LIKELIHOOD BANDWIDTH
h.ucv      # MIN UNBIASED CROSS-VALIDATION BANDWIDTH
h.bcv      # MIN BIASED CROSS-VALIDATION BANDWIDTH 

## OUTPUT PLOTS
hist(y,breaks=20,freq=FALSE)
lines(d.pl,lty=2)
lines(d.ucv,lty=3)
lines(d.bcv)


############################################################################
### EXAMPLE 10.3-4 WHALE MIGRATION
############################################################################
# whalemigration.dat = contains data
# y = observed data
############################################################################
## NOTES
# The base stats package and the R package {MASS} both contain a wide 
# variety of the techniques used in this chapter and are usually simpler 
# approachs than directly programming a method. See the ?density help 
# page for more information.
# If using the bandwidth selectors in MASS, please note that they are 
# scaled and will give values four times larger.
# i.e.:  bw.ucv(y) = ucv(y)/4 
############################################################################
## INITIAL VALUES
whalemigration.dat = read.table(file.choose())
y = whalemigration.dat$V1


## MAIN
h.s  = sd(y)*(4/(3*length(y)))^.2
h.SJ = bw.SJ(y)
h.t  = 3*sd(y)*((1/(2*sqrt(pi)))/(35*length(y)))^.2
d.s  = density(y, bw=h.s,  kernel="gaussian")
d.SJ = density(y, bw=h.SJ, kernel="gaussian")
d.t  = density(y, bw=h.t,  kernel="gaussian")


## OUTPUT
h.s       # SILVERMAN'S BANDWIDTH
h.SJ      # SHEATHER-JONES BANDWIDTH (Slight variation in MASS package)
h.t       # TERRELL'S MAXIMAL SMOOTHING BANDWIDTH


## OUTPUT PLOTS
hist(y,breaks=20,freq=FALSE)
lines(d.s,lty=2)
lines(d.SJ)
lines(d.t,lty=3)



############################################################################
### EXAMPLE 10.5 BIMODAL DENSITY
############################################################################
# bimodal.dat = contains data
# y           = observed data
# x           = sequence of points for plotting
# d           = kernel density estimates
# K.triw      = triweight kernel
# f.hat.triw  = kernel density estimator for triweight kernel
############################################################################
## NOTES
# The base stats package and the R package {MASS} both contain a wide 
# variety of the techniques used in this chapter and are usually simpler 
# approachs than directly programming a method. See the ?density help 
# page for more information.
# If using the bandwidth selectors in MASS, please note that they are 
# scaled and will give values four times larger.
# i.e.:  bw.ucv(y) = ucv(y)/4 
############################################################################
## INITIAL VALUES
bimodal.dat = read.table(file.choose())
y = bimodal.dat$V1
x = seq(min(y)-sd(y), max(y)+sd(y), length.out=1000)


## FUNCTIONS
K.unif     = function(z){ifelse(abs(z)<1,0.5,0)}
f.hat.unif = function(x,h){mean(K.unif((x-y)/h))/h}

K.triw     = function(z){ifelse(abs(z)<1,(35/32)*(1-z^2)^3,0)}
f.hat.triw = function(x,h){mean(K.triw((x-y)/h))/h}


## MAIN
h.SJ       = bw.SJ(y)
delta.unif = (9/2)^.2
delta.n    = (1/(2*sqrt(pi)))^.2
delta.triw = (9450/143)^.2
h.unif     = h.SJ*delta.unif/delta.n
h.triw     = h.SJ*delta.triw/delta.n


d1 = mapply(f.hat.unif, x, h.unif)
d2 = density(y, bw=h.SJ, kernel="epanechnikov")
d3 = density(y, bw=h.SJ, kernel="triangular")
d4 = density(y, bw=h.SJ, kernel="gaussian")
d5 = density(y, bw=h.SJ, kernel="biweight")
d6 = mapply(f.hat.triw, x, h.triw)


## OUTPUT
h.SJ      # SHEATHER-JONES BANDWIDTH FOR NORMAL KERNEL


## OUTPUT PLOTS
par(mfrow=c(2,3))
plot(d1,axes=F,frame.plot=T,xlab="",ylab="",main="Uniform",type="l")
plot(d2,axes=F,frame.plot=T,xlab="",ylab="",main="Epanechnikov")
plot(d3,axes=F,frame.plot=T,xlab="",ylab="",main="Triangular")
plot(d4,axes=F,frame.plot=T,xlab="",ylab="",main="Normal")
plot(d5,axes=F,frame.plot=T,xlab="",ylab="",main="Biweight")
plot(d6,axes=F,frame.plot=T,xlab="",ylab="",main="Triweight",type="l")



############################################################################
### EXAMPLE 10.6 WHALE MIGRATION (LOGSPLINE)
############################################################################
# whalemigration.dat = contains data
# y = observed data
############################################################################
## NOTES
# The following example uses the {polspline} package. See the ?logspline 
# help page for more information. 
############################################################################
## INITIAL VALUES
whalemigration.dat = read.table(file.choose())
y = whalemigration.dat$V1

library(polspline) #you may need to install this package

## MAIN
fit1 = oldlogspline(y)
fit1 = oldlogspline.to.logspline(fit1,y)
fit2 = oldlogspline(y,nknots=6,delete=F)
fit2 = oldlogspline.to.logspline(fit2,y)
fit3 = oldlogspline(y,nknots=11,delete=F)
fit3 = oldlogspline.to.logspline(fit3,y)

## OUTPUT
fit1      # OPTIMAL FIT BASED ON BIC

## PLOTS
hist(y,breaks=20,freq=FALSE)
plot(fit1,add=T)
plot(fit2,add=T,lty=2)
plot(fit3,add=T,lty=3)

points(fit2$knots,rep(0,6),pch=21,cex=2,bg="white")
points(fit1$knots,rep(0,7),pch=21,cex=2,bg="black")




############################################################################
### EXAMPLE 10.7 BIVARIATE T DISTRIBUTION
############################################################################
# n         = sample size
# df        = degrees of freedom
# alpha     = sensitivity parameter
# epsilon   = tolerance
# y         = observed data
# x         = sequence of points for plotting
# X         = matrix of points for plotting (second coordinate set at 0)
# h         = bandwidths
# f.tilda   = pilot estimator values
# hs        = adapted bandwidths
# f.hatp    = nonadaptive estimator
# f.hat.adp = adaptive estimator
############################################################################
# Note: results differ slightly from the book because of the random
# number seed.
############################################################################

## INITIAL VALUES
n       = 500
p       = 2
df      = 3
alpha   = 0.5
epsilon = 0.005

set.seed(0)

y  = matrix(rnorm(n*p), nrow=n)/
      sqrt(matrix(rchisq(n,df),nrow=n,ncol=p)/df)
x  = seq(min(y)-max(sd(y)), max(y)+max(sd(y)), length.out=1000)
X  = cbind(x,rep(0,length(x)))
h1 = bw.SJ(y[,1])
h2 = bw.SJ(y[,2])
h  = c(h1,h2)
f.tilda = rep(1,n)
hs = rep(1,n)


## FUNCTIONS
f.hatp = function(x){
      m   = length(x[,1])
      out = rep(0,m)
      for(i in 1:m){
            out[i] = mean(dnorm((x[i,1]-y[,1])/h[1])/h[1] * 
                      dnorm((x[i,2]-y[,2])/h[2])/h[2])
      }
      return(out)
}

f.hat.adp = function(x,h){
      m   = length(x[,1])
      out = rep(0,m)
      for(i in 1:m){
            out[i] = mean(dnorm(x[i,1],mean=y[,1],sd=h) * 
                      dnorm(x[i,2],mean=y[,2],sd=h))
      }
      return(out)
}

## MAIN
d = f.hatp(X)

for(i in 1:n){
      f.tilda[i] = mean(dnorm((y[i,1]-y[,1])/h[1])/h[1] * 
                    dnorm((y[i,2]-y[,2])/h[2])/h[2])
}
f.tilda[f.tilda < epsilon] = epsilon
g.mean = exp(mean(log(f.tilda)))
hs     = mean(h)/((f.tilda/g.mean)^alpha)
d.adp  = f.hat.adp(X,hs)

## OUTPUT PLOTS
par(mfrow=c(1,2))
plot(x,d,type="l",main="Nonadaptive approach",
      ylab="Estimated density",xlab="x1")
plot(x,d.adp,type="l",main="Adaptive approach",
      ylab="Estimated density",xlab="x1")


############################################################################
### EXAMPLE 10.8 BIVARIATE ROTATION
############################################################################

# Omitted. It's nasty.  The figures illustrate the key points.  The data 
# are available for you to play with.  (2drotation.dat)


############################################################################
### END OF FILE
