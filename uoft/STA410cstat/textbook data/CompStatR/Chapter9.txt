############################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 9 EXAMPLES (last update 10/1/2012)

############################################################################
# Note:
# The random number seeds used here sometimes give slightly different
# answers than in the book.
############################################################################

############################################################################
### EXAMPLE 9.3-4 COPPER-NICKEL ALLOY (PAIRED BOOTSTRAPPING)
############################################################################
# alloy.dat = contains data
# z         = contains paired data
# itr       = number of iterations to run
# theta     = observed data estimate (beta1/beta0)
# thetas    = bootstrapped estimates (beta1/beta0)
############################################################################
## NOTES
# The R package {boot} can perform a wide variety of bootstrapping 
# techniques and is usually a simpler approach than directly programming 
# a method. 
############################################################################

## INITIAL VALUES
alloy.dat = read.table(file.choose(),header = TRUE)
z         = alloy.dat
itr       = 10000
theta     = NULL
thetas    = rep(0,itr)
set.seed(0)

## MAIN
model = lm(z[,2]~z[,1])
theta = as.numeric(model$coefficients[2]/model$coefficients[1])
for(i in 1:itr){
      z.new = z[sample(1:length(z[,1]),replace=T),]
      model = lm(z.new[,2]~z.new[,1])
      thetas[i] = model$coefficients[2]/model$coefficients[1]
}
bias = mean(thetas)-theta

## OUTPUT
theta               # OBSERVED DATA ESTIMATE
bias                # ESTIMATED BIAS
theta-bias          # BIAS-CORRECTED ESTIMATE

## PLOTS
hist(thetas,breaks=40)


############################################################################
### EXAMPLE 9.5-6 COPPER-NICKEL ALLOY (CONFIDENCE INTERVALS)
############################################################################
# alloy.dat = contains data
# z         = contains paired data
# itr       = number of iterations to run
# theta     = observed data estimate (beta1/beta0)
# thetas    = bootstrapped estimates (beta1/beta0)
# ci.95     = 95% CI based on empirical percentile
# ci.95.bc  = 95% CI based on accelerated bias-corrected percentile
############################################################################
## NOTES
# It's possible to have a resample that contains only one pair of original
# observations. This will produce a NA in lm(). 
############################################################################

## INITIAL VALUES
alloy.dat    = read.table(file.choose(),header = TRUE)
z            = alloy.dat
itr          = 10000
theta        = NULL
thetas       = rep(0,itr)
theta.hat.mi = rep(0,length(z[,1]))
psi          = rep(0,length(z[,1]))
ci.95        = rep(0,2)
ci.95.bc     = rep(0,2)
set.seed(0)

## MAIN
model = lm(z[,2]~z[,1])
theta = as.numeric(model$coef[2]/model$coef[1])
for(i in 1:itr){
      z.new = z[sample(1:length(z[,1]),replace=T),]
      model = lm(z.new[,2]~z.new[,1])
      thetas[i] = model$coef[2]/model$coef[1]
}
ci.95 = quantile(thetas,c(0.025,0.975),na.rm=T)

# COMPUTES 95% CI BASED ON ACCELERATED BIAS-CORRECTED PERCENTILE
for(i in 1:length(z[,1])){
      model = lm(z[-i,2]~z[-i,1])
      theta.hat.mi[i] = model$coef[2]/model$coef[1]
}
for(i in 1:length(z[,1])){
      psi[i] = mean(theta.hat.mi[-i])-theta.hat.mi[i]
}
a = (1/6)*sum(psi^3)/(sum(psi^2))^(3/2)
b = qnorm(mean(thetas<theta),0,1)
beta1 = pnorm(b + (b+qnorm(.025,0,1))/(1-a*(b+qnorm(.025,0,1))))
beta2 = pnorm(b + (b+qnorm(.975,0,1))/(1-a*(b+qnorm(.975,0,1))))
ci.95.bc = quantile(thetas,c(beta1,beta2),na.rm=T)

## OUTPUT
theta          # OBSERVED DATA ESTIMATE
ci.95          # 95% CI BASED ON EMPIRICAL PERCENTILE
ci.95.bc       # 95% CI BASED ON ACCELERATED BIAS-CORRECTED PERCENTILES

## PLOTS
hist(thetas,breaks=40)


############################################################################
### EXAMPLE 9.7 COPPER-NICKEL ALLOY (STUDENTIZED BOOTSTRAP)
############################################################################
# alloy.dat = contains data
# z         = contains paired data
# itr       = number of iterations to run
# theta     = observed data estimate for (beta1/beta0)
# theta.var = estimated variance for theta
# theta.sd  = estimated std deviation for theta
# thetas    = bootstrapped estimates for (beta1/beta0)
# G         = studentized bootstrap values
# ci.95.t   = 95% CI for studentized bootstrap method
############################################################################
## NOTES
# It's possible to have a resample that contains only one pair of original
# observations. This will produce a NA in lm(). 
############################################################################

## INITIAL VALUES
alloy.dat = read.table(file.choose(),header = TRUE)
z         = alloy.dat
itr       = 10000
theta     = NULL
theta.var = NULL
theta.sd  = NULL
thetas    = rep(0,itr)
ci.95.t   = rep(0,2)
G         = rep(0,itr)
set.seed(0)

## MAIN
model = lm(z[,2]~z[,1])
theta = as.numeric(model$coef[2]/model$coef[1])
cov.m = summary(model)$cov
theta.var = (theta^2)*(cov.m[2,2]/(model$coef[2]^2) + 
        cov.m[1,1]/(model$coef[1]^2) - 2*cov.m[1,2]/(prod(model$coef)))
theta.sd  = as.numeric(sqrt(theta.var))
for(i in 1:itr){
      z.new = z[sample(1:length(z[,1]),replace=T),]
      model = lm(z.new[,2]~z.new[,1])
      thetas[i] = model$coef[2]/model$coef[1]
      cov.m = summary(model)$cov
      b.var = (thetas[i]^2)*(cov.m[2,2]/(model$coef[2]^2) + 
       cov.m[1,1]/(model$coef[1]^2) - 2*cov.m[1,2]/(prod(model$coef)))
      b.sd  = sqrt(b.var)
      G[i] = (thetas[i]-theta)/b.sd
}
ci.95.t[1] = theta - theta.sd*quantile(G,.975,na.rm=T)
ci.95.t[2] = theta - theta.sd*quantile(G,.025,na.rm=T)


## OUTPUT
theta          # OBSERVED DATA ESTIMATE
theta.sd       # ESTIMATED STD DEVIATION OF THETA
ci.95.t        # 95% CI FOR STUDENTIZED BOOTSTRAP METHOD


## PLOTS
hist(G,breaks=40)


############################################################################
### EXAMPLE 9.8 COPPER-NICKEL ALLOY (NESTED BOOTSTRAP)
############################################################################
# alloy.dat = contains data
# z         = contains paired data
# itr       = number of iterations to run for R0
# itr2      = number of iterations to run for R1
# theta     = observed data estimate for (beta1/beta0)
# thetas    = bootstrapped estimates for (beta1/beta0)
# thetas2   = nested bootstrapped estimates
# R0        = test statistics for bootstrapped estimates
# R1        = test statistics for nested bootstrapped estimates
# ci.95.n   = 95% CI for nested bootstrap method
############################################################################
## NOTES
# It's possible to have a resample that contains only one pair of original
# observations. This will produce a NA in lm(). 
############################################################################

## INITIAL VALUES
alloy.dat = read.table(file.choose(),header = TRUE)
z         = alloy.dat
itr       = 300
itr2      = 300
theta     = NULL
thetas    = rep(0,itr)
thetas2   = matrix(0,itr,itr2)
R0        = rep(0,itr)
R1        = rep(0,itr2)
ci.95.n   = rep(0,2)
set.seed(1)

## MAIN
model = lm(z[,2]~z[,1])
theta = as.numeric(model$coef[2]/model$coef[1])
for(i in 1:itr){
      z.new = z[sample(1:length(z[,1]),replace=T),]
      model = lm(z.new[,2]~z.new[,1])
      thetas[i] = model$coef[2]/model$coef[1]
      for(j in 1:itr2){
            z.new2 = z.new[sample(1:length(z[,1]),replace=T),]
            model = lm(z.new2[,2]~z.new2[,1])
            thetas2[i,j] = model$coef[2]/model$coef[1]
      }
}
R0 = thetas-theta
for(i in 1:itr2){R1[i] = mean((thetas2[i,]-thetas[i]) <= R0[i])}
R0.u = quantile(R0, quantile(R1,0.975,na.rm=T), na.rm=T)
R0.l = quantile(R0, quantile(R1,0.025,na.rm=T), na.rm=T)
ci.95.n[1] = theta - R0.u
ci.95.n[2] = theta - R0.l

## OUTPUT
theta          # OBSERVED DATA ESTIMATE
ci.95.n        # 95% CI FOR NESTED BOOTSTRAP METHOD

## PLOTS
hist(R1)


############################################################################
### EXAMPLE 9.9 INDUSTRIALIZED COUNTRY GDP EXAMPLE
############################################################################
# blocks = arranges the blocks in a matrix for easy manipulation
# xbar   = means from block bootstrap pseudo-datasets
############################################################################
##INITIAL VALUES
gdp=read.table(file.choose(),header=TRUE)
blocks=rbind(gdp[1:8,2],gdp[9:16,2],gdp[17:24,2],gdp[25:32,2],gdp[33:40,2])
xbar=rep(NA,10000)

##NON-MOVING BLOCK BOOTSTRAP
set.seed(567890)
for (i in 1:10000) {
    take.blocks=sample(1:5,5,replace=T)
    newdat=c(t(blocks[take.blocks,]))
    xbar[i]=mean(newdat) }

##OUTPUT
sqrt(var(xbar))  


############################################################################
### EXAMPLE 9.10 INDUSTRIALIZED COUNTRY GDP EXAMPLE, CONT.
############################################################################
# blocks = arranges the blocks in a matrix for easy manipulation
# xbar   = means from block bootstrap pseudo-datasets
############################################################################
# NOTE: See errata for typo in the text for this example
############################################################################

###INITIAL VALUES
gdp=read.table(file.choose(),header=TRUE)
blocks=gdp[1:8,2]
for (i in 2:33) {
  blocks=rbind(blocks,gdp[i:(i+7),2]) }

##MOVING BLOCK BOOTSTRAP
xbar=rep(NA,10000)
set.seed(0)  
for (i in 1:10000) {
  take.blocks=sample(1:33,5,replace=T)
  newdat=c(t(blocks[take.blocks,]))
  xbar[i]=mean(newdat) }

##OUTPUT
sqrt(var(xbar))

hist(xbar)


############################################################################
### EXAMPLE 9.11 TREE RINGS
############################################################################
# n = number of data points
# p = number of data points per small block
# n.block = number of big blocks (blocks-of-blocks)
# len.block = number of small blocks per big block
# smallblocks = one column per small block, p rows
# bigblocks = array: row=small block, col=data, 3rd dim=big block 
# lag2cor = bootstrap estimates of lag-2 correlation
############################################################################

##INITIAL VALUES
basal=read.table(file.choose(),header=TRUE)
p=3
n=452
n.block=450
len.block=25

##FUNCTION
calc.rhat=function(x) {
  n=dim(x)[1]
  xwhole=c(x[,1],x[(n-1):n,3])
  xm=mean(xwhole)
  return(sum((x[,1]-xm)*(x[,3]-xm))/sum((xwhole-xm)^2)) }

##ESTABLISH BLOCKS and BLOCKS-OF-BLOCKS
smallblocks=rbind(basal[1:(n-2),2],basal[2:(n-1),2],basal[3:n,2])
bigblocks=array(NA,c(p,len.block,n.block-len.block+1))
for (i in 1:(n.block-len.block+1)) {
  bigblocks[,,i]=smallblocks[,i:(i+len.block-1)] }
bigblocks=aperm(bigblocks,c(2,1,3))

##B-O-B BOOTSTRAP
lag2cor=rep(NA,10000)
set.seed(567890)
for (i in 1:10000) {
  take.blocks=sample(1:(n.block-len.block+1),n.block/len.block,replace=T)
  newdat=apply(bigblocks[,,take.blocks],2,rbind)
  lag2cor[i]=calc.rhat(newdat)  
}

##OUTPUT
sqrt(var(l22)) 

##NOTE: The {tseries} package includes tsbootstrap() which is a
##  convenient tool for some of these methods and includes a bootstrap
##  bias estimate as provided in the text.


############################################################################
### END OF FILE
