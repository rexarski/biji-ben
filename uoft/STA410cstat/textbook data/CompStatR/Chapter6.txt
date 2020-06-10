#########################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 6 EXAMPLES (last update 10/1/2012)
#########################################################################


#########################################################################
### EXAMPLE 6.1 GAMMA DEVIATES
#########################################################################
# r = gamma dist shape parameter (r >= 1)
# n = sample size
# g = function for generating gamma(r,1) draw
# x = random draws from gamma(r,1) dist
#########################################################################

## INITIAL VALUES
r = 4
n = 1000
z = rnorm(n)
u = runif(n)

## FUNCTIONS
g = function(y,r){
     a = r - (1/3)
     b = 1/sqrt(9*a)
     out = a*(1+b*y)^3
     return(out)
}
g = Vectorize(g)

## MAIN
a = r - (1/3)
v = g(z,r)
z = z[(v > 0)]
u = u[(v > 0)]
v = v[(v > 0)]
f = exp(((z^2)/2) + a*log(v/a) - v + a)
keep = (u <= f) * (1:length(v))

## OUTPUT
x = v[keep]	 # DRAWS FROM GAMMA(r,1)
length(x)/n 	 # PERCENT OF DRAWS ACCEPTED

## PLOTS
z = sort(z)
# PLOT OF ENVELOPE
plot(z,exp(-(z^2)/2),type="l")
# PLOT OF DENSITY PROPORTIONAL TO TARGET IGNORING NORMALIZING CONSTANT
points(z,exp(a*log(g(z,r)/a) - g(z,r) + a),type="l")


#########################################################################
### EXAMPLE 6.2 SAMPLING A BAYESIAN POSTERIOR
#########################################################################
# x = observed data
# n = sample size
# d = prior draws
# u = uniform draws
#########################################################################

## INITIAL VALUES
x = c(8,3,4,3,1,7,2,6,2,7)
n = 1000
d = exp(rnorm(n,log(4),0.5))
u = runif(n)
x.bar = mean(x)

# MAIN
check = sapply(d,
           function(d){sum(dpois(x,d,log=T))-sum(dpois(x,x.bar,log=T))})
check = exp(check)
keep = (1:n)[u < check]

## OUTPUT
y = d[keep] # DRAWS FROM POSTERIOR
length(y)/n # PERCENT OF DRAWS ACCEPTED

## PLOTS
lambda=seq(0,20,length.out=1000)

y1=dlnorm(lambda,log(4),.5)*prod(dpois(x,x.bar))
plot(lambda,y1,type="l")

y2=dlnorm(lambda,log(4),.5)*sapply(lambda,function(d){prod(dpois(x,d))})
lines(lambda,y2,lty=2)


#########################################################################
### EXAMPLE 6.3 SLASH DISTRIBUTION
#########################################################################
# m = sample size
# n = resample size
# y = sample candidates from a standard normal dist
# v = sample candidates from a slash dist
# w = computes standardized importance weights (slash target density)
# w2 = computes standardized importance weights (normal target density)
# x = resample (approximate draws from slash dist)
# u = resample (approximate draws from standard normal dist)
#########################################################################
## NOTES
# This example uses the {VGAM} package for its implementation of the
# slash distribution.
#########################################################################

library(VGAM)

## INITIAL VALUES
m = 100000
n = 5000
y = rnorm(m)
v = rslash(m)

## FUNCTIONS
w = function(x){
     out = dslash(x)/dnorm(x)
     out = out/sum(out)
     return(out)
}
w2 = function(x){
     out = dnorm(x)/dslash(x)
     out = out/sum(out)
     return(out)
}

## CALCULATE WEIGHTS AND RESAMPLE
weights = w(y)
x = sample(y, n, replace=TRUE, prob=weights)
weights2 = w2(v)
u = sample(v, n, replace=TRUE, prob=weights2)

## OUTPUT
par(mfrow=c(1,2))
hist(x,freq=FALSE,breaks=seq(-7,7,by=.25),main="Histogram of draws",
  ylab="Slash density")
points(seq(-10,10,by=.01),dslash(seq(-10,10,by=.01)),type="l")

hist(u,freq=FALSE,breaks=seq(-7,7,by=.25),main="Histogram of draws",
  ylab="Normal density")
points(seq(-10,10,by=.01),dnorm(seq(-10,10,by=.01)),type="l")



#########################################################################
### EXAMPLE 6.5 SIMPLE MARKOV PROCESS
#########################################################################
# tmax = limit on t index
# n = number of Monte Carlo samples
# rejuvs = number of rejuvenations used
# ess = effective sample size
# w = importance weights
# X = samples
# Xt = current sample of X_t | X_(t-1)
# sds = sequence of estimates of sigma
#########################################################################
##INITIAL VALUES
tmax=100
n=100000
X=matrix(0,n,tmax+1)
w=matrix(0,n,tmax+1)
w[,1]=rep(1/n,n)
ess=rep(0,tmax)
rejuvs=0

##MAIN LOOP
set.seed(919191)
for (i in 1:tmax) {
     Xt=rnorm(n,X[,i],rep(1.5,n))
     u=abs(cos(Xt-X[,i]))*exp(-.25*abs(Xt-X[,i])^2)/
       (dnorm(Xt,X[,i],rep(1.5,n)))
     w[,i+1]=w[,i]*u
     w[,i+1]=w[,i+1]/sum(w[,i+1])
     ess[i]=1/sum(w[,i+1]^2)
     if (ess[i]<.33*n) {
          Xt=sample(Xt,n,prob=w[,i+1],replace=T)
          rejuvs=rejuvs+1 
          w[,i+1]=rep(1/n,n) 
     }
     X[,i+1]=Xt 
}

##CALCULATE SIGMA FOR EACH T
sds=rep(0,tmax+1)      
for (i in 1:(1+tmax)) {
     denom=1/(1-sum(w[,i]^2))
     muhatt=sum(w[,i]*X[,i])/sum(w[,i])
     sumofsq=sum(w[,i]*(X[,i]-muhatt)^2)
     sds[i]=sqrt(denom*sumofsq) 
}

##OUTPUT
sds[101]   #SigmaHat_100


#########################################################################
### EXAMPLE 6.6 HIGH DIMENSIONAL DISTRIBUTION
#########################################################################
# p = number of dimensions
# n = number of points sampled
# N.eff = effective sample size
# X = sample
# w = importance weights
# rejuvs = number of rejuvenations
# normal.draw = sample from the standard normal envelope.
# ftxt = f_x(x_1:t) in book notation
# ft1xt1= f_t-1(x_1:t-1)
# Note: f_t(x_t|x_1:t-1) = ftxt/ft1xt1
#########################################################################

##INITIAL VALUES
p=50
n=5000
X=matrix(NA,nrow=n,ncol=p)
w=rep(1,n)/n
N.eff=rep(NA,p+1)
N.eff[1]=n
ft1xt1=w
rejuvs=0

##FUNCTION
dens.fun=function(x) {
  temp=function(x) {   exp(-(abs(sqrt(sum(x^2)))^3)/3) }
  c(apply(x,1,temp)) }

##MAIN LOOP
set.seed(4567)
for (i in 1:p) {
    normal.draw=rnorm(n,mean=0,sd=1)
    if (i>1) {
         Xtemp=cbind(X[,1:(i-1)],normal.draw) 
         ftxt=dens.fun(Xtemp) } else { ftxt=dens.fun(cbind(normal.draw)) }
    X[,i]=normal.draw 
    w=w*ftxt/(ft1xt1*dnorm(normal.draw))
    ft1xt1=ftxt
    w=w/sum(w)
    N.eff[i+1]=1/sum(w^2)
    if (N.eff[i+1]<N.eff[1]/5) {
       rejuvs=rejuvs+1
       idx=sample(1:n,n,replace=T,prob=w)
       X=X[idx,]
       ft1xt1=dens.fun(X[,1:i])
       w=rep(1,n)/n
    } 
}

#OUTPUT
rejuvs     # NUMBER OF REJUVENATIONS
N.eff      # EFFECTIVE SAMPLE SIZES AT EACH ITERATION
median(N.eff)

#NOW TRY TO EXPEND ALL EFFORT ON ONE SIR OF 5000 PTS
set.seed(111)
x=matrix(rnorm(50*5000),5000,50)
g=dnorm(x)
f=dens.fun(x)
impwt=f/apply(g,1,prod)
impwt=impwt/sum(impwt)
#ESS
1/sum(impwt^2)  #Answer varies with random number seed



#########################################################################
### EXAMPLE 6.7 - 6.8  TERRAIN NAVIGATION
#########################################################################
# 
# 
# 
# 
#########################################################################
#Note: This example is rather complex and less transparent than
#most examples we provide.  It will also be slow on your computer.
#########################################################################
# n = number of sampled trajectories
# Yt = observed elevation data
# mxti = map elevations
# xt.x, xt.y = current position of point
# uti = weight adjustment factors
# wti = weights
# Neff = effective sample size
# alpha = rejuvenation trigger
# dsubt.x, dsubt.y = true drift
# epst.x, epst.y = location error
#######################################################
# Note: this example requires the packages {akima} and {mvtnorm}
#######################################################
##The Colorado data are stored as a matrix suitable
##for reading and plotting using the image() command.
##The first row and column of the matrix are *not* 
##elevations.  They are lat,lon coordinates (with a NA
##in the 1,1 spot in the matrix.  The first row and column
##should therefore be stripped away (see below).  The
##remainder of the matrix gives elevations over the
##coordinate system.  In summary, the following R
##code should be used to read and arrange the data:
#######################################################
colo=as.matrix(read.table(file="colorado.dat",sep="",header=F))
colorado.lat=colo[1,-1]
colorado.lon=colo[-1,1]
colorado.elev=colo[-1,][,-1]
dim(colorado.elev)  #should be 186 x 125
image(colorado.lon,colorado.lat,colorado.elev,col=gray(seq(.25,1,len=200)),
 xlim=c(-6000,34000),ylim=c(-6000,34000))
####################################################

library(mvtnorm)
library(akima)

##INITIAL VALUES
n=100
sigma=75 
q.value=400
k=.5  
sdx0=50
wti=rep(1/n,n)
neff.record=rep(NA,100)
rejuvcount=0
reset=F

##SET UP TRUE STARTING POINT, 100 INITIAL POINTS
##AND FIRST ELEVATION OBSERVATION
x0hat.x=0 ; x0hat.y=30000  #start at true X0 here
truex=x0hat.x
truey=x0hat.y
xthat.x=truex
xthat.y=truey
xt.x=rnorm(n,x0hat.x,sqrtP0)   #was x.xold 
xt.y=rnorm(n,x0hat.y,sqrtP0)   #was y.yold
colo.elev.interp=colorado.elev
colo.elev.interp[is.na(colo.elev.interp)]=
    mean(colo.elev.interp[!is.na(colo.elev.interp)])
colo.lon.rep=rep(colorado.lon,rep(125,186))
colo.lat.rep=rep(colorado.lat,186)
Yt=interp(colo.lon.rep,colo.lat.rep,
     colo.elev.interp,xo=0,yo=30000)$z

##SET UP TRUE DRIFT
route.theta=seq(0,pi/2,len=101)
route.x=30000*cos(route.theta)
route.y=30000*sin(route.theta)
route.x=rev(route.x)
route.y=rev(route.y)
dsubt.x=diff(route.x)
dsubt.y=diff(route.y)

##FUNCTION
rotnorm=function(N,slope,sigmamat) {
     v=rmvnorm(N,mean=c(0,0),sigma=sigmamat)
     xy=c(1,slope)
     Rot=cbind(c(-xy[1],-xy[2]),c(xy[2],-xy[1]))/sqrt(sum(xy^2))
     therot=t(Rot%*%t(v))
     therot }

image(colorado.lon,colorado.lat,colorado.elev,col=gray(seq(.25,1,len=200)),
 xlim=c(-6000,34000),ylim=c(-6000,34000))
lines(route.x,route.y,col=2) #truth

set.seed(75339)
for (i in 1:100) {
  #find m(x_t^i)
    xord=rank(xt.x)  
    yord=rank(xt.y)
    mapt=interp(colo.lon.rep,colo.lat.rep,colo.elev.interp,
       xo=sort(xt.x),yo=sort(xt.y))  
    mxti=mapt$z[cbind(xord,yord)] 
    extrap=is.na(mxti)
  #weight the points
    uti=ifelse(extrap,0,dnorm(Yt,c(mxti),rep(sigma,n)))
    wti=uti*wti
    wti=wti/sum(wti)
    Neff=1/sum(wti^2)
    neff.record[i]=Neff
  #preliminary calcs for drawing the plot
    xthat.old=c(xthat.x,xthat.y)
    xthat.x=sum(wti*xt.x)
    xthat.y=sum(wti*xt.y)
  #check if resample needed
    if (Neff<(alpha*n)) {
       idx=sample(1:n,n,replace=T,prob=wti)
       xtnew.x=xt.x[idx]
       xtnew.y=xt.y[idx]
       wti=rep(1/n,n) 
       rejuvcount=rejuvcount+1
       reset=T }
  #update cloud
    tangent.slope=-truex/truey
    Zsigmamat=cbind(c(q.value^2,0),1*c(0,(k*q.value)^2))
    xtnext=rotnorm(n,tangent.slope,Zsigmamat)  
    epst.x=xtnext[,1]
    epst.y=xtnext[,2]
    if (!reset) {
       xtnext.x=xt.x+dsubt.x[i]+epst.x      #still using old points
       xtnext.y=xt.y+dsubt.y[i]+epst.y 
    } else {
       xtnext.x=xtnew.x+dsubt.x[i]+epst.x   #start with new points
       xtnext.y=xtnew.y+dsubt.y[i]+epst.y 
       reset=F
    }
    xt.x=xtnext.x
    xt.y=xtnext.y
  #update truth and observed elevation data
    truex=truex+dsubt.x[i]
    truey=truey+dsubt.y[i]
    Yt=interp(colo.lon.rep,colo.lat.rep,
         colo.elev.interp,xo=truex,yo=truey)$z+rnorm(1,0,sigma) 
     lines(c(xthat.old[1],xthat.x),
               c(xthat.old[2],xthat.y),lwd=2) 
}

##OUTPUT  
             #Graph is made above
rejuvcount   #Number of rejuvenations

#Note, for bootstrap filter, we force the resampling step 
#to occur at each iteration, and hence we also set wi = 1 
#anew at each iteration. There is no multiplicative
#adjustment to the previous stage's weight.


#########################################################################
### EXAMPLE 6.9 NETWORK FAILURE
#########################################################################
# n = sample size
# p = failure probability
# pstar = importance sampling method failure probability
# numedges = number of edges in complete network
#########################################################################

##INITIAL VALUES
p=.05
pstar=.2
n=100000
numedges=20
failed.orig=rep(FALSE,n)
failed.is=rep(FALSE,n)    

##SETTING UP THE NETWORK
#PRE-PROCESSING NOT SHOWN HERE GENERATED A LIST OF ALL 
#CONNECTED PATHS.  THIS SHORTCUT IS USED TO SPEED THE EXAMPLE.
#Letters indicate links.  Characters assigned alphabetically
#working from left to right and then top to down.  Thus
#a, b, c, d represent the four links from A to one of the
#nodes directly to it's right.  The top node in the
#second column has links e, f, g, h to the four nodes
#in the third column.  Then labels are given to the second node 
#in the second column.  And so forth.

connecteds=c("ahnr","ahnos","ahnopt","ahnolmt","ahnokgmt",
  "ahnjfks","ahnjfkpt","ahnjfklmt","ahnjfgls","ahnjfglpt",
  "ahnjfgmt","ahnjfgmps","ahq","ainq","air","aios","aiopt",
  "aiolmt","aiokfmt","aijfgls","aijfglpt","aijfgmt","aijfgmps",
  "aijfks","aijfkpt","aijfklmt","aejnq","aejr","aejos",
  "aejopt","aejolmt","aejokgmt","aefkonq","aefkor","aefks",
  "aefkpt","aefklmt","aefglonq","aefgls","aefglpt","aefgmt",
  "aefgmps","aefgmpor","aefgmponq","behq","behnr","behnos",
  "behnopt","behnokgmt","behnolmt","beinq","beir","beios",
  "beiopt","beiolmt","beiokgmt","bjnq","bjr","bjos","bjopt",
  "bjolmt","bjokgmt","bjihq","bfkonq","bfkor","bfkoihq",
  "bfks","bfkpt","bfklmt","bfgloihq","bfglonq","bfglor",
  "bfgls","bfglpt","bfgmps","bfgmpor","bfgmpoihq","bfgmponq",
  "bfgmt","cfehq","cfehnr","cfehnos","cfehnolmt","cfehnopt",
  "cfeinq","cfeir","cfeios","cfeiopt","cfeiolmt","cfjnq",
  "cfjr","cfjos","cfjopt","cfjolmt","cfjihq","ckonq","ckor",
  "ckojehq","ckoihq","cks","ckpt","cklmt","cglonq","cglor",
  "cglojehq","cgloihq","cgls","cglpt","cgmponq","cgmpor",
  "cgmpojehq","cgmpoihq","cgmps","cgmt","dgfehq","dgfehnr",
  "dgfehnos","dgfehnopt","dgfeinq","dgfeir","dgfeios",
  "dgfeiopt","dgfjnq","dgfjr","dgfjos","dgfjopt","dgfjihq",
  "dgkonq","dgkor","dgkojehq","dgks","dgkpt","dlonq","dlor",
  "dlojehq","dloihq","dls","dlpt","dlkfehq","dlkfehnr",
  "dlkfeir","dlkfeinq","dlkfjr","dlkfjnq","dlkfjihq","dmponq",
  "dmpor","dmpojehq","dmpoihq","dmps","dmpkfehq","dmpkfehnr",
  "dmpkfeinq","dmpkfeir","dmpkfjihq","dmpkfjnq","dmpkfjr","dmt")

##GENERATE LOGICAL MATRIX STRUCTURE FLAGGING NECESSARY LINKS
##IN EACH POSSIBLE LINKED CONFIGURATION	
temp=matrix(0,nrow=158,ncol=9)
for (i in 1:9) {
   temp[,i]=substring(connecteds,i,i) 
}
mylet=c("",letters[1:numedges])
linkmat=matrix(0,158,9)
for (i in 1:9) {
  for (j in 1:158) {
    linkmat[j,i]=(0:numedges)[mylet==temp[j,i]]
  }
}

link.logic.mat=matrix(F,nrow=158,ncol=numedges)
for (i in 1:158) {
     for (j in 1:9) {
          if (linkmat[i,j]>0) {link.logic.mat[i,linkmat[i,j]]=TRUE} 
     } 
}

##CORE OF EXAMPLE BEGINS HERE

##SAMPLE NETWORKS AND CHECK WHETHER THEY FAIL
set.seed(126)
breaks=sample(c(T,F),numedges*n,prob=c(p,1-p),replace=T)
brokenlinks=matrix(breaks,nrow=n,ncol=numedges)
for (j in 1:n) {
config=brokenlinks[j,]
     if (sum(config)>0) {
          tested=t( t(link.logic.mat)&(!config) )
          failed.orig[j]=!any(!apply(xor(tested,link.logic.mat),1,any)) 
     } 
}

##IMPORTANCE SAMPLING APPROACH
set.seed(127)
breaks=sample(c(T,F),numedges*n,prob=c(pstar,1-pstar),replace=T)
brokenlinks=matrix(breaks,nrow=n,ncol=numedges)
for (j in 1:n) {
    config=brokenlinks[j,]
    if (sum(config)>0) {
        tested=t( t(link.logic.mat)&(!config) )
        failed.is[j]=!any(!apply(xor(tested,link.logic.mat),1,any)) 
    } 
}
failures.in.config=apply(brokenlinks,1,sum)
weights=failures.in.config*(log(p)-log(pstar))+
         (numedges-failures.in.config)*(log(1-p)-log(1-pstar))
weights=exp(weights)

##OUTPUT
sum(failed.orig)                #original count of failed networks
sum(failed.is)                  #count of failed networks with pstar=.25
mean(failed.is*weights)         #importance sampling estimate muhatstar_is
sqrt(var(failed.is*weights)/n)  #MC standard error


#########################################################################
### EXAMPLE 6.10 NORMAL EXPECTATION
#########################################################################
# n = sample size
# z = standard normal draws
# h = target function
#########################################################################

## INITIAL VALUES
n = 100000
z = rnorm(n)

## FUNCTIONS
h = function(x){x/((2^x)-1)}

## MONTE CARLO ESTIMATE
mu.mc = mean(h(z))
se.mc = sd(h(z))/sqrt(n)

## ANTITHETIC ESTIMATOR
mu.a = sum(h(z[1:50000])+h(-z[1:50000]))/n
rho = cor(h(z[1:50000]),h(-z[1:50000]))
se.a = (1+rho)*var(h(z[1:50000]))/n

## OUTPUT
mu.mc # MONTE CARLO ESTIMATOR
se.mc # MONTE CARLO STD ERROR
mu.a # ANTITHETIC ESTIMATOR
se.a # ANTITHETIC STD ERROR
rho # CORRELATION


#########################################################################
### EXAMPLE 6.13 OPTION PRICING
#########################################################################
# S = prices of stock over time
# S0 = price at time zero
# ST = price at time T
# K = strike price
# T = time of maturity
# r = risk-free rate of return
# n = number of iterations
# m = number of mc estimations
# sigma = stock's volatility
#########################################################################

## INITIAL VALUES
S0 = 100
K = 102
sigma = 0.3
T = 50
r = 0.05
n = 1000
m = 100

## BACKGROUND: MC ESTIMATES (EUROPEAN CALL OPTION)
mu.mc.e = NULL
for(j in 1:m){
      ST = S0*exp((r-(sigma^2)/2)*T/365 + sigma*rnorm(n)*sqrt(T/365))
      C = NULL
      for(i in 1:n){
      	    C[i] = exp(-r*T/365)*max(c(0,ST[i] - K))
      }
      mu.mc.e[j] = mean(C)
}
se.mc.e = sd(mu.mc.e)/sqrt(m)

## MC ESTIMATES (ASIAN ARITHMETIC AND GEOMETRIC CALL OPTION)
mu.mc = NULL
theta.mc=NULL
for(j in 1:m){
 #calculate MC estimate of A and theta
      A = NULL
      theta = NULL
      for(i in 1:n){
      	    ST = NULL
	    ST[1] = S0
	    for(k in 2:T){
	    	  ST[k] = ST[k-1]*exp(((r-(sigma^2)/2)/365) +
		    sigma*rnorm(1)/sqrt(365))
            }
      A[i] = exp(-r*T/365)*max(c(0,mean(ST) - K))
      theta[i] = exp(-r*T/365)*max(c(0,exp(mean(log(ST))) - K))
      }
      mu.mc[j] = mean(A)
      theta.mc[j]=mean(theta)
}

## ANALYTIC SOLUTION (GEOMETRIC MEAN)
N = T
c3 = 1 + 1/N
c2 = sigma*((c3*T/1095)*(1 + 1/(2*N)))^.5
c1 = (1/c2)*(log(S0/K) + (c3*T/730)*(r - (sigma^2)/2) +
       (c3*(sigma^2)*T/1095)*(1 + 1/(2*N)))
theta = S0*pnorm(c1)*exp(-T*(r + c3*(sigma^2)/6)*(1 - 1/N)/730) -
       K*pnorm(c1-c2)*exp(-r*T/365)

## CONTROL VARIATE
mu.cv=mu.mc-1*(theta.mc-theta)

## OUTPUT
sd(mu.mc)  #STANDARD DEVIATION FOR ORDINARY APPROACH
sd(mu.cv)  #STANDARD DEVIATION FOR CONTROL VARIATE APPROACH



#########################################################################
### END OF FILE
