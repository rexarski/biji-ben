############################################################################
# COMPUTATIONAL STATISTICS
# by Geof H. Givens and J. A. Hoeting
# CHAPTER 7 EXAMPLES (Last update: 1/9/2013)

############################################################################
### EXAMPLE 7.2 ESTIMATING A MIXTURE PARAMETER
############################################################################
############################################################################
# y     = observed data
# n     = number of iterations 
# x.val = contains mixture parameter values
# f     = posterior density
# R     = computes Metropolis-Hastings ratio
# g     = proposal density
############################################################################
# NOTES
# In the following, the density of the prior is uniform over the 
# support for the proposal and hence not included in the computation of the
# Metropolis-Hastings ratio.
############################################################################

## Mixture data
mixture.dat = read.table(file.choose(),header=TRUE)
y = mixture.dat$y

## HISTOGRAM OF DATA AND PLOT OF MIXTURE DISTRIBUTION (See figure 7.1)
par(mfrow=c(1,1))
x=seq(5,14,by=.01)
d=.7*dnorm(x,7,.5) + .3*dnorm(x,10,.5)
hist(y,breaks=20,freq=FALSE,main="Histogram of mixture data \n See Fig 7.1 in Givens and Hoeting",ylab="Density")
points(x,d,type="l")

## INITIAL VALUES
n = 10000
x.val1 = NULL
x.val2=NULL
set.seed(0)

## FUNCTIONS
f = function(x){prod(x*dnorm(y,7,0.5) + (1-x)*dnorm(y,10,0.5))}
R = function(xt,x){f(x)*g(xt)/(f(xt)*g(x))}

## MAIN
# BETA(1,1) PROPOSAL DENSITY
g = function(x){dbeta(x,1,1)}
x.val1[1] = rbeta(1,1,1)
for(i in 1:n){
      xt = x.val1[i]
      x = rbeta(1,1,1)
      p = min(R(xt,x),1)
      d = rbinom(1,1,p)
      x.val1[i+1] = x*d + xt*(1-d)
}
mean(x.val1[201:(n+1)])
par(mfrow=c(2,2))
plot(x.val1[201:(n+1)],ylim=c(0,1),type="l",ylab="delta",xlab="t")
title("Sample path for Beta(1,1) Proposal Dist.")
hist(x.val1[201:(n+1)],breaks=20,xlab="delta",
      main="Hist. for Beta(1,1) Proposal Dist.")

# BETA(2,10) PROPOSAL DENSITY
g = function(x){dbeta(x,2,10)}
x.val2[1] = rbeta(1,2,10)
for(i in 1:n){
      xt = x.val2[i]
      x = rbeta(1,2,10)
      p = min(R(xt,x),1)
      d = rbinom(1,1,p)
      x.val2[i+1] = x*d + xt*(1-d)
}
mean(x.val2[201:(n+1)])
plot(x.val2[201:(n+1)],ylim=c(0,1),type="l",ylab="delta",xlab="t")
title("Sample path for Beta(2,10) Proposal Dist.")
hist(x.val2[201:(n+1)],breaks=20,xlab="delta",
      main="Hist. for Beta(2,10) Proposal Dist.")



############################################################################
### EXAMPLE 7.3 ESTIMATING A MIXTURE PARAMETER (RANDOM WALK)
############################################################################
#
# x     	= observed data
# log.like 	= function to compute the log likelihood
# p        	= mixture parameter values
# u        	= logit of the mixture parameter values
# R     	= Metropolis-Hastings ratio
# num.its 	= number of iterations for the MCMC chain
############################################################################

## NOTES
# In the following, the density of the prior distribution is uniform over the 
# support for the proposal and hence not included in the computation of
# the Metropolis-Hastings ratio. Also, since the proposal density is 
# symmetric about zero, the Metropolis-Hastings ratio can be
# reduced to just the posterior densities and Jacobian. In
# this example we leave the unreduced version of the ratio to show 
# implementation, but in subsequent implementations it may be reduced when
# possible.
############################################################################

# UNIFORM(-1,1) WALK
## INITIAL VALUES
#READ IN THE DATA
mixture.dat = read.table(file.choose(),header=TRUE)
x = mixture.dat$y

#ESTABLISH INITIAL VALUES
u=rep(0,num.its)
u[1]= runif(1,-1,1)
p=rep(0,num.its)
p[1]=exp(u[1])/(1+exp(u[1]))

set.seed(1)
num.its = 10000

## FUNCTIONS
log.like<-function(p,x) {
	  sum(log(p*dnorm(x,7,.5)+(1-p)*dnorm(x,10,.5)))
}

## MAIN
for (i in 1:(num.its-1)) {
	u[i+1]=u[i]+runif(1,-1,1)
	p[i+1]=exp(u[i+1])/(1+exp(u[i+1]))
	R=exp(log.like(p[i+1],x)-log.like(p[i],x))*exp(u[i])/exp(u[i+1])
	if (R<1)
		 if(rbinom(1,1,R)==0)	{p[i+1]=p[i]; u[i+1]=u[i]}
}

mean(p[-burn.in])
par(mfrow=c(2,2))
plot(p,ylim=c(0,1),type="l",ylab="delta",xlab="t")
hist(p,breaks=20,xlab="delta",
      main="Hist. for Unif(-1,1) Walk")

# UNIFORM(-0.01,0.01) WALK
##INITIAL VALUES
p2=rep(0,num.its)
p2[1]=exp(u[1])/(1+exp(u[1]))

## MAIN
for (i in 1:(num.its-1)) {
	u[i+1]=u[i]+runif(1,-.01,.01)
	p2[i+1]=exp(u[i+1])/(1+exp(u[i+1]))
	R= exp(log.like(p2[i+1],x)-log.like(p2[i],x))*exp(u[i])/exp(u[i+1])
	if (R<1)
		 if(rbinom(1,1,R)==0)	{p2[i+1]=p2[i]; u[i+1]=u[i]}
}

mean(p2[-burn.in])
plot(p2,ylim=c(0,1),type="l",ylab="delta",xlab="t")
hist(p2,breaks=20,xlab="delta",
       main="Hist. for Unif(-0.01,0.01) Walk")


#Exercises:  
# 1. Recode example 7.3 using the likelihood instead of the log-likelihood.  What changes in the code?  
# 2. Re-run the Uniform(-0.01,0.01) code using more iterations.  What happens?  
# 3. Is either case sensitive to starting value?  Why or why not?

############################################################################
### EXAMPLE 7.6 FUR SEAL PUP CAPTURE-RECAPTURE STUDY (GIBBS SAMPLING)
############################################################################
# ci    	= number captured during each census
# mi    	= number newly caught during each census
# r     	= number of unique fur seal pups observed
# I		= number of census attempts
# N     	=  estimated population size
# alpha     = computes estimated capture probabilities for each census
# num.its  	= number of iterations
# burn.in  	= iterations to discard for burn-in
############################################################################
## INITIAL VALUES
ci = c(30,22,29,26,31,32,35)  
mi = c(30,8,17,7,9,8,5)
r = sum(mi)
I=7

alpha= matrix(0,num.its,I)
N=rep(0,num.its)
N[1]=sample(84:500,1) 
set.seed(4)
num.its=100000
burn.in = 1:1000

#MAIN
for (i in 2:num.its) {
   alpha[i,]=rbeta(I,ci+.5,N[i-1]-ci+.5)
   N[i]=rnbinom(1,r+1,1-prod(1-alpha[i,]))+r
}

# DISCARDING BURN-IN
alpha.out = alpha[-burn.in,]
N.out = N[-burn.in]


## OUTPUT
mean(N.out)      # POSTERIOR MEAN OF N

#MANUAL COMPUTATION OF AN HPD INTERVAL
#NOTE:  this is not a sophisticated method to compute an HPD interval, but
#it is adequate for a one-time computation of an HPD interval and a good learning tool.

table(N.out)
sum(N.out>=85 & N.out<=95)/length(N.out)
sum(N.out>=85 & N.out<=94)/length(N.out)
sum(N.out>=84 & N.out<=93)/length(N.out)
sum(N.out>=84 & N.out<=94)/length(N.out)

## OUTPUT PLOTS
plot((max(burn.in)+1):num.its,N.out,type="l",
      xlab="t",ylab="N",main="Sample path for N")

boxplot(split(rowMeans(alpha.out),N.out),ylab="Mean Capture Probability",
      xlab="N",main="Split boxplot for seal pup example")

hist(N.out,freq=FALSE,xlab="N",
      main="Estimated marginal posterior probabilities for N")

#Exercise:
#1.  Write a function to compute the HPD interval for discrete data like the N in the seal example.  


############################################################################
### EXAMPLE 7.8 MIXTURE DISTRIBUTION, CONTINUED
############################################################################
#See EXAMPLE 7.2 to calculate these inputs:
#x.val1 = delta values from independence chain with Beta(1,1) proposal density
#x.val2 = delta values from independence chain with Beta(2,10) proposal density

acf(x.val1)
acf(x.val2)

############################################################################
### EXAMPLE 7.10 FUR SEAL PUP CAPTURE-RECAPTURE STUDY, CONTINUED
############################################################################
# ci    	= number captured during each census
# mi    	= number newly caught during each census
# r     	= number of unique fur seal pups observed
# I		= number of census attempts
# N.val 	=  estimated population size
# alpha.val = computes estimated capture probabilities for each census
# u.val 	= contains log values of the parameters for estimating the capture probs
# num.its  	= number of iterations
# burn.in  	= iterations to discard for burn-in

# f     = computes posterior density, p(theta|alpha)
# J     = computes Jacobian
# R     = computes Metropolis-Hastings ratio

############################################################################
############################################################################
## NOTES
# Since the proposal density is symmetric about zero, the 
# Metropolis-Hastings ratio is reduced to just the posterior 
# densities and Jacobian. 
############################################################################

## INITIAL VALUES
ci = c(30,22,29,26,31,32,35)  
mi = c(30,8,17,7,9,8,5)
r = sum(mi)
I=7

set.seed(4)
num.its=100000
burn.in = 1:1000

alpha.val= matrix(0,num.its,I)
u.val = matrix(0,num.its,2)
N.val=rep(0,num.its)
N.val[1]=sample(84:500,1) 


## FUNCTIONS
new.log.target=function(exp.uv,p) {
  I*(lgamma(sum(exp.uv))-lgamma(exp.uv[1])-lgamma(exp.uv[2])) +
    exp.uv[1]*sum(log(p))+exp.uv[2]*sum(log(1-p))-sum(exp.uv)/1000+
    log(exp.uv[1])+log(exp.uv[2])
}

R = function(new,old,alphas) {
   exp(new.log.target(exp(new),alphas)-new.log.target(exp(old),alphas))
}


## MAIN
for (i in 2:num.its) {
   alpha.val[i,]=rbeta(I,ci+exp(u.val[i-1,1]),N.val[i-1]-ci+exp(u.val[i-1,2]))
   N.val[i]=rnbinom(1,r,1-prod(1-alpha.val[i,])) + r
   u.star=u.val[i-1,]+rnorm(2,0,.085)
   p=min(R(u.star,u.val[i-1,],alpha.val[i,]),1)
   d = rbinom(1,1,p)
   u.val[i,] = u.star*d + u.val[i-1,]*(1-d)
}

# DISCARDING BURN-IN
N.out = N.val[-burn.in]
u.out = u.val[-burn.in,]
alpha.out = alpha.val[-burn.in,]

## OUTPUT
mean(N.out)      # POSTERIOR MEAN OF N

#MANUAL COMPUTATION OF AN HPD INTERVAL
#NOTE:  this is not a sophisticated method to compute an HPD interval, but
#it is adequate for a one-time computation of an HPD interval and a good learning tool.

table(N.out)
sum(N.out>=85 & N.out<=95)/length(N.out)
sum(N.out>=85 & N.out<=94)/length(N.out)
sum(N.out>=84 & N.out<=93)/length(N.out)
sum(N.out>=84 & N.out<=94)/length(N.out)

## OUTPUT PLOTS 
#Plots like Figures 7.10
acf(alpha.out[,1])
a=(dim(u.out)[1]-999):dim(u.out)[1]
plot(u.out[a,2],u.out[a,1],type="l")

#These plots aren't in the book, but are similar to the plots in Example 7.6
plot((max(burn.in)+1):num.its,N.out,type="l",
      xlab="t",ylab="N",main="Sample path for N")

boxplot(split(rowMeans(alpha.out),N.out),ylab="Mean Capture Probability",
      xlab="N",main="Split boxplot for seal pup example")

hist(N.out,freq=FALSE,xlab="N",
      main="Estimated marginal posterior probabilities for N")

############################################################################
### END OF FILE