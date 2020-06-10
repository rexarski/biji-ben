############################################################################
# COMPUTATIONAL STATISTICS
# by Geof H. Givens and J. A. Hoeting
# CHAPTER 8 EXAMPLES (Last update: 11/7/2013)
############################################################################
### EXAMPLE 8.1 WHALE POPULATION DYNAMICS (ADAPTIVE METROPOLIS-WITHIN-GIBBS)
############################################################################
############################################################################


#Note: See the errata for the 2nd edition regarding Example 8.1.
#The code below had NOT yet been fixed to reverse the
#proposal ratio.  


Variables:
K=carrying capacity (see Equation 8.2)
r=intrinsic growth rate
N=abundance (population count)
C=catch
sigma=variance of log(N.hat) (see Equation 8.3)
truecv=coefficient of variation (see Equation 8.3)
Xt = survey abundance estimate (this is called \hat{N}_y in Example 8.1)

Functions:
gettraj=population trajectory
myloglik.tomax=log likelihood used for maximum likelihood estimation (not MCMC)
myloglik=log likelihood used for AMCMC
calcposterior= computes the value of the posterior
myposterior.tomax=posterior used to compute the MAP (maximum a posteriori) estimate
truncnormal=generates from the proposal distribution, see equations 8.4 and 8.6
truncunif=generates from the proposal distribution, see equation 8.5

###########Generate the data
K=10000
r=.03
N=rep(0,101)
sigma=0.30
truecv=sqrt(exp(sigma^2)-1)

#catch data
C=rep(0,101)
C=c(606,1151,928,1024,1375,939,701,573,350,322,278,254,
   rep(60,8),rep(30,10),rep(25,30),rep(20,41))
#Add noise to the catch data
set.seed(19359)
for (i in 13:101) {
  C[i]=C[i]*exp(rnorm(1,0,.5)) }
C=round(C,0)

#plot the true traj
N[1]=K
for(t in 1:100) {
  N[t+1]=N[t]-C[t]+r*N[t]*(1-(N[t]/K)^2) }
N=round(N)
plot(1:101,N,type="l",ylim=c(0,K+3000))

#use only surveys from five years
datyears=c(14,21,63,91,93,100)
n=length(datyears)

#generate surveys
set.seed(477)
Xt=N*exp(rnorm(101,0,sigma))
Xt=round(Xt,0)
#points(1:101,Xt)
points(datyears,Xt[datyears],pch=16,col=2)

## FUNCTIONS

gettraj=function(theK,ther) {
  Ntraj=rep(NA,101)
  Ntraj[1]=theK
  for(t in 1:100) {
    Ntraj[t+1]=Ntraj[t]-C[t]+ther*Ntraj[t]*(1-(Ntraj[t]/theK)^2) 
    if (Ntraj[t+1]<=0) { Ntraj[(t+1):101]=0.0001 ; break } }
    Ntraj 
}


myloglik.tomax=function(parms,dy=datyears) {
  K=parms[1]
  r=parms[2]
  cv=parms[3]
  sigma=sqrt(log(1+cv^2))
  Ntraj=gettraj(K,r) 
  nll=-sum(log(dlnorm(Xt[dy],log(Ntraj[dy]),sigma)))
  if(is.infinite(nll)) {nll=1e10}  
  nll }
 

myloglik=function(K,r,cv,dy=datyears) {
  sigma=sqrt(log(1+cv^2))
  Ntraj=gettraj(K,r) 
  sum(log(dlnorm(Xt[dy],log(Ntraj[dy]),sigma))) } 

calcposterior=function(K,r,cv) {
  ml=myloglik(K,r,cv) 
  if (is.infinite(ml) | K<7000 | K>100000 | r<.001 | r>.1 | cv<0 | cv>2) {p=0} else {
    pripart=(1/93000)*(1/.099)*dbeta(cv/2,2,10) 
    p=exp(ml)*pripart }
  p }



#functions needed to calculate transition probabilities

truncnormal=function(qlow=-Inf,qhi=Inf,current,sd) {
  plow=pnorm(qlow,current,sd)
  phi=pnorm(qhi,current,sd)
  u=runif(1,plow,phi)
  nextdraw=qnorm(u,current,sd)
  dforward=dnorm(nextdraw,current,sd)/(phi-plow)
  plow=pnorm(qlow,nextdraw,sd)
  phi=pnorm(qhi,nextdraw,sd)
  dbackward=dnorm(current,nextdraw,sd)/(phi-plow)
  list(nextdraw=nextdraw,dforward=dforward,dbackward=dbackward) }

truncunif=function(qlow,qhi,current,lim) {
  lower=max(qlow,current-lim)
  upper=min(qhi,current+lim)
  nextdraw=runif(1,lower,upper)
  dforward=1/(upper-lower)
  lower=max(qlow,nextdraw-lim)
  upper=min(qhi,nextdraw+lim)
  dbackward=1/(upper-lower)
  list(nextdraw=nextdraw,dforward=dforward,dbackward=dbackward) }

## MAIN

#Initialize

chainlen=45000 ; burnin=10000
postprob=rep(NA,chainlen)
trigger=1500  #how often to adapt
Kpath = rpath = cvpath = rep(NA,chainlen+1)
Kpath[1]=10000 ; rpath[1]=.03 ; cvpath[1]=.3
mhratiocheck.K = mhratiocheck.r = mhratiocheck.cv = rep(NA,chainlen)
asjd.K = asjd.r = asjd.cv = rep(NA,chainlen)
thefactor.K = thefactor.r = thefactor.cv = rep(NA,chainlen)
acceptcount.K = acceptcount.r = acceptcount.cv =0
acceptratio.K = acceptratio.r = acceptratio.cv = rep(NA,chainlen/trigger)

#first good run: new.K.sd= c(500,rep(NA,chainlen/trigger-1)) #results1
#new.K.sd= c(50,rep(NA,chainlen/trigger-1))     #results2
new.K.sd= c(200,rep(NA,chainlen/trigger-1))     #results3 (book choice)
new.r.lim= c(.03,rep(NA,chainlen/trigger-1))
new.cv.sd= c(.1,rep(NA,chainlen/trigger-1))
setpoint=1

set.seed(123)
for (t in 1:(chainlen)) {  
#browser()  
  ##adapt if necessary
 if (t>1 & (t-1)%%trigger==0) {   
    setpoint=setpoint+1
  #for K
    acceptratio.K[setpoint]=acceptcount.K/trigger
    acceptcount.K=0  
    upordown=ifelse(acceptratio.K[setpoint]<.44,-1,1)
    thefactor.K[setpoint] = exp(upordown*t^(-1/3))
    new.K.sd[setpoint]=new.K.sd[setpoint-1]*thefactor.K[setpoint] 
    new.K.sd[setpoint]=min(10000,new.K.sd[setpoint]) 
  #for r
    acceptratio.r[setpoint]=acceptcount.r/trigger
    acceptcount.r=0  
    upordown=ifelse(acceptratio.r[setpoint]<.44,-1,1)
    thefactor.r[setpoint] = exp(upordown*t^(-1/3))
    new.r.lim[setpoint]=new.r.lim[setpoint-1]*thefactor.r[setpoint]
    new.r.lim[setpoint]=min(.05,new.r.lim[setpoint]) 
  #for cv
    acceptratio.cv[setpoint]=acceptcount.cv/trigger
    acceptcount.cv=0  
    upordown=ifelse(acceptratio.cv[setpoint]<.44,-1,1)
    thefactor.cv[setpoint] = exp(upordown*t^(-1/3))
    new.cv.sd[setpoint]=new.cv.sd[setpoint-1]*thefactor.cv[setpoint] 
    new.cv.sd[setpoint]=min(10,new.cv.sd[setpoint]) }

  ##proposals
  gk=truncnormal(7000,100000,Kpath[t],new.K.sd[setpoint])
  prop.K=gk$nextdraw
  gr=truncunif(.001,.1,rpath[t],new.r.lim[setpoint])
  prop.r=gr$nextdraw
  gcv=truncnormal(0,2,cvpath[t],new.cv.sd[setpoint])
  prop.cv=gcv$nextdraw
  ##Gibbs cycles
   #for K
 mhr=calcposterior(prop.K,rpath[t],cvpath[t])*gk$dforward/
        (calcposterior(Kpath[t],rpath[t],cvpath[t])*gk$dbackward)
 mhratiocheck.K[t]=mhr
 asjd.K[t]=min(mhr,1)*(prop.K-Kpath[t])^2
 u=runif(1,0,1)
 if (mhr>=1 | u<=mhr) {
   acceptcount.K=acceptcount.K+1
   Kpath[t+1]=prop.K } else {
   Kpath[t+1]=Kpath[t] } 
  #for r
#if (t>120) browser()
 mhr=calcposterior(Kpath[t+1],prop.r,cvpath[t])*gr$dforward/
        (calcposterior(Kpath[t+1],rpath[t],cvpath[t])*gr$dbackward)
 mhratiocheck.r[t]=mhr
 asjd.r[t]=min(mhr,1)*(prop.r-rpath[t])^2
 u=runif(1,0,1)
 if (mhr>=1 | u<=mhr) {
   acceptcount.r=acceptcount.r+1
   rpath[t+1]=prop.r } else {
   rpath[t+1]=rpath[t] } 
 #for cv
 mhr=calcposterior(Kpath[t+1],rpath[t+1],prop.cv)*gcv$dforward/
        (calcposterior(Kpath[t+1],rpath[t+1],cvpath[t])*gcv$dbackward)
 mhratiocheck.cv[t]=mhr
 asjd.cv[t]=min(mhr,1)*(prop.cv-cvpath[t])^2
 u=runif(1,0,1)
 if (mhr>=1 | u<=mhr) {
   acceptcount.cv=acceptcount.cv+1
   cvpath[t+1]=prop.cv } else {
   cvpath[t+1]=cvpath[t] }   
 postprob[t]=calcposterior(Kpath[t+1],rpath[t+1],cvpath[t+1])
}

## OUTPUT

plot(1:(chainlen+1),Kpath,type="l")
who=ifelse(mhratiocheck.K==0,T,F)
points((2:chainlen+1)[who],Kpath[2:chainlen][who],pch=16,col=2)
new.K.sd
acceptratio.K
m1=mean(Kpath[burnin:chainlen])  #true K = 10000
m1
#[1] 9680 (Note:  your answers will vary)
summary(Kpath[burnin:chainlen])

hist(Kpath[burnin:chainlen],nclass=50)
#mode 9748

plot(1:(chainlen+1),rpath,type="l")
who=ifelse(mhratiocheck.r==0,T,F)
#text(2:(chainlen+1),rpath[2:chainlen],round(mhratiocheck.r,4),col=who,cex=.75)
points((2:chainlen+1)[who],Kpath[2:chainlen][who],pch=16,col=2)
new.r.lim
acceptratio.r
m2=mean(rpath[burnin:chainlen])   #true r = 0.03
m2 
#[1] .04103

summary(rpath[burnin:chainlen])

hist(rpath[burnin:chainlen],nclass=50)
#.03295 mode

plot(1:(chainlen+1),cvpath,type="l")
who=ifelse(mhratiocheck.cv==0,T,F)
#text(2:(chainlen+1),cvpath[2:chainlen],round(mhratiocheck.cv,4),col=who,cex=.75)
points((2:chainlen+1)[who],Kpath[2:chainlen][who],pch=16,col=2)
new.cv.sd
acceptratio.cv
m3=mean(cvpath[burnin:chainlen]) #true cv= 0.307
m3 
#[1] 0.2509253
summary(cvpath[burnin:chainlen])
hist(cvpath[burnin:chainlen],nclass=50)
#mode 
#[1] .16295


#plot the true traj
N[1]=K
for(t in 1:100) {
  N[t+1]=N[t]-C[t]+r*N[t]*(1-(N[t]/K)^2) }
plot(1:101,N,type="l",ylim=c(0,K+3000))
points(datyears,Xt[datyears],pch=16,col=2)

#plot MLE
optim(c(14000,.04,.3),myloglik.tomax,
  control=list(parscale=c(10000,1/100,1/10))) 

optim(myloglik.tomax,c(10000,.03,.3)
#max is
[1] 9.906669e+03 3.167191e-02 1.258889e-01

#plot MLE
Ntemp=rep(NA,101)
Ntemp[1]=  9907
rtemp=   .03167191
h=gettraj(Ntemp[1],rtemp)
lines(1:101,h,type="l",col=2,lwd=2)

#MAP estimate
myposterior.tomax=function(params) {
  -log(calcposterior(params[1],params[2],params[3])) }

optim(c(12000,.04,.3),myposterior.tomax, 
  control=list(trace=2,parscale=c(10000,1/100,1/10)))

#max at
[1] 9.906014e+03 3.168095e-02 1.300854e-01


#posterior

#priors:
#K ~ unif(7000,100000)
#r ~ unif(.001,.1)
#cv/2 ~ beta(2,10)  #meancv=.336


Ntemp=rep(NA,101)
Ntemp[1]=  9888
rtemp=   .03226434
h=gettraj(Ntemp[1],rtemp)
lines(1:101,h,type="l",col=2,lwd=2)

h=gettraj(9748,.03295)
lines(1:101,h,col=4)

who=postprob==max(postprob)  #joint MAP
cbind(Kpath,rpath,cvpath)[-1,][who,]
#       Kpath        rpath       cvpath 
#9.913550e+03 3.165349e-02 1.317438e-01 


h=gettraj(9914,.0316535)  #joint MAP
lines(1:101,h,col=6)

par(mfrow=c(1,2))
plot(1:30,acceptratio.K,type="l",xlab="t",ylim=c(0.20,0.68))
abline(h=0.44,lty=2)
plot(1:30,new.K.sd,type="l",xlab="t",ylab="200delta_k^t")

par(mfrow=c(1,2))
plot(1:30,acceptratio.r,type="l",xlab="t",,ylim=c(0.20,0.68))
abline(h=0.44,lty=2)
plot(1:30,new.r.lim,type="l",xlab="t",ylab="0.036delta_r^t")

par(mfrow=c(1,2))
plot(1:30,acceptratio.cv,type="l",xlab="t",,ylim=c(0.20,0.68))
abline(h=0.44,lty=2)
plot(1:30,new.cv.sd,type="l",xlab="t",ylab="0.1delta_psi^t")


#create a list of all the relevant output
results3=list(Kpath=Kpath,rpath=rpath,cvpath=cvpath,
  acceptratio.K=acceptratio.K,acceptratio.r=acceptratio.r,
  acceptratio.cv=acceptratio.cv,new.K.sd=new.K.sd,new.r.lim=new.r.lim,
  new.cv.sd=new.cv.sd,asjd.K=asjd.K,asjd.r=asjd.r,asjd.cv=asjd.cv,
  postprob=postprob)

#only last 7500 iterations:
which=37500:45000
mean(asjd.K[which])
mean(asjd.r[which])
mean(asjd.cv[which])

############################################################################
### EXAMPLE 8.3 BASEBALL SALARIES, CONTINUED (RJMCMC)
############################################################################
baseball.dat = contains data
ball.run1 = implements RJMCMC for the baseball data using the BMA package in R
############################################################################
## NOTES
#This example uses the BMA package in R.  You'll have to install the package
#first. 
#
#You should examine the MC3.REG algorithm from the BMA library in R so that you can 
#further understand the implementation of a fully working reversible jump MCMC algorithm.  
#The MC3.REG function calls several other functions including: 
#
# For.MC3.REG     = Helper function for MC3.REG which implements each step of 
#                   the Metropolis-Hastings algorithm.
# MC3.REG.logpost = Helper function to MC3.REG that calculates the posterior 
#                   model probability (up to a constant).
# MC3.REG.choose  = Helper function to MC3.REG that chooses the proposal model 
#                   for a Metropolis-Hastings step.
############################################################################

#INPUTS
library(BMA)  
baseball.dat = read.table(file.choose(),header=T)

## MAIN
ball.run1<-MC3.REG(baseball.dat[,1], baseball.dat[,-1], num.its=200000,
    rep(TRUE,27), outliers = FALSE)

## OUTPUTS
summary(ball.run1)
ball.run1[1:20,]
ball.run1[200000,]

############################################################################
### EXAMPLE 8.6 UTAH SERVICEBERRY DISTRIBUTION (GIBBS SAMPLER)
############################################################################
# utahserviceberry.dat = contains data
# x         = true presence- true absence (1=presence, 0=absence)
# y         = observed presence- observed absence (1=presence, 0=absence)
# a         = alpha parameter 
# b         = beta parameter
# itr       = number of cycles to run
# y2        = alternate coding of y (-1=presence, 1=absence)
# xt        = estimated presence-absence information
#             (1=presence, 0=absence)
# x2        = alternate coding of xt (-1=presence, 1=absence)
# xt.all    = xt for each cycle
# xt.p      = mean posterior estimates for each pixel
# f         = computes probability of setting pixel(pos) to 1 (presence)
# neighbors = finds indices of the neighbors to pixel(pos)
############################################################################
## NOTES
# The image function in R rotates the matrix 90 degrees counter-clockwise.
# See the ?image help page for more information.
############################################################################

## INITIAL VALUES
utahserviceberry.dat = read.csv(file.choose(),header=T)
dim(utahserviceberry.dat)   
#Check dimensions to make sure that you have read in data correctly
[1] 2484    1

x = utahserviceberry.dat[,1]
a = 1
b = 0.8
itr = 100
set.seed(0)
y = x
n.row = 54
n.col = 46
n = n.row*n.col
bad = sample.int(n,745)
y[bad] = !y[bad]
y2 = (!y) - y
x2 = y2
xt = y
xt.all = matrix(0,itr,n)

## FUNCTIONS
f = function(pos){
      (1 + exp(a*y2[pos] + b*sum(x2[neighbors(pos)])))^-1
}

neighbors = function(pos){
      if((pos-1)%%n.row != 0 & pos%%n.row != 0){
            out = c(pos-1,pos+1,pos-n.row,pos+n.row)
            out = out[out>0 & out<(n+1)]
      }
      if((pos-1)%%n.row == 0 | pos%%n.row == 0){
            if(pos%%n.row != 0){
                  out = c(pos+1,pos-n.row,pos+n.row)
                  out = out[out>0 & out<(n+1)]
            }
            if(pos%%n.row == 0){
                  out = c(pos-1,pos-n.row,pos+n.row)
                  out = out[out>0 & out<(n+1)]
            }
      }
      return(out)
}

## MAIN
for(j in 1:itr){
      for(i in 1:n){
            q = f(i)
            d = rbinom(1,1,q)
            xt[i] = d
            x2[i] = 1-2*d
      }
      xt.all[j,] = xt
}
xt.p = colMeans(xt.all)
x.est = (xt.p>=.5)
p.correct = 1-mean(abs(x.est - x))

## OUTPUT
                 # PERCENT OF CORRECT ESTIMATES 
p.correct        # POSTERIOR MEAN >= .5 IS CLASSIFIED AS 1, ELSE 0

## PLOTS
par(pty="s",mfrow=c(2,2))
x.image = matrix(x,n.row,n.col)
x.image = x.image[,n.col:1]
image(1:n.row,1:n.col,x.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="True presence-absence")

y.image = matrix(y,n.row,n.col)
y.image = y.image[,n.col:1]
image(1:n.row,1:n.col,y.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="Obs presence-absence")

xt.p.image = matrix(xt.p,n.row,n.col)
xt.p.image = xt.p.image[,n.col:1]
image(1:n.row,1:n.col,xt.p.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="Est presence-absence")


############################################################################
### EXAMPLE 8.7 UTAH SERVICEBERRY DISTRIBUTION (SWENDSEN-WANG)
############################################################################
# utahserviceberry.dat = contains data
# x         = true presence-absence information
# y         = observed presence-absence information
# a         = alpha parameter 
# b         = beta parameter
# itr       = number of cycles to run
# xt        = estimated presence-absence information (1=presence)
# xt.m      = matrix form of xt
# xt.all    = xt for each cycle
# xt.p      = mean posterior estimates for each pixel
# g         = computes probability of setting cluster to 1 (presence)
# neighbors = finds indices of the neighbors to pixel(pos)
# cluster   = finds indices of all pixels in cluster containing pixel(pos)
############################################################################
## INITIAL VALUES
utahserviceberry.dat = read.table(file.choose())
x = utahserviceberry.dat[,1]
a = 1
b = 0.8
itr = 100
set.seed(0)
y = x
n.row = 54
n.col = 46
n = n.row*n.col
bad = sample.int(n,745)
y[bad] = !y[bad]
xt = y
xt.all = matrix(0,itr,n)

## FUNCTIONS
neighbors = function(pos){
      if((pos-1)%%n.row != 0 & pos%%n.row != 0){
            out = c(pos-1,pos+1,pos-n.row,pos+n.row)
            out = out[out>0 & out<(n+1)]
      }
      if((pos-1)%%n.row == 0 | pos%%n.row == 0){
            if(pos%%n.row != 0){
                  out = c(pos+1,pos-n.row,pos+n.row)
                  out = out[out>0 & out<(n+1)]
            }
            if(pos%%n.row == 0){
                  out = c(pos-1,pos-n.row,pos+n.row)
                  out = out[out>0 & out<(n+1)]
            }
      }
      return(out)
}

g = function(clust){
      exp(a*sum(y[clust]))/(exp(a*sum(y[clust]==0)) + exp(a*sum(y[clust])))
}

cluster = function(pos){
      done = FALSE
      clust = c(pos)
      m = 1
      while(!done){
            pos = clust[m]
            k = neighbors(pos)
            more = NULL
            k.l = sort(k[k<pos])
            k.u = sort(k[!(k %in% k.l)])
            if(length(k.u)==1 & k.u[1]==(pos+1)){
                  if(bv[pos]){more = c(more,k.u[1])}}
            if(length(k.u)==1 & k.u[1]!=(pos+1)){
                  if(bh[pos]){more = c(more,k.u[1])}}
            if(length(k.u)==2){
                  if(bv[pos]){more = c(more,k.u[1])}
                  if(bh[pos]){more = c(more,k.u[2])}}
            if(length(k.l)==1 & k.l[1]==(pos-1)){
                  if(bv[pos-1]){more = c(more,k.l[1])}}
            if(length(k.l)==1 & k.l[1]!=(pos-1)){
                  if(bh[k.l[1]]){more = c(more,k.l[1])}}
            if(length(k.l)==2){
                  if(bh[k.l[1]]){more = c(more,k.l[1])}
                  if(bv[pos-1]){more = c(more,k.l[2])}}            
            if(length(more)>0){clust = unique(c(clust,more))}
            if(length(clust)==m){done=TRUE}
            m = m+1
            }
      return(clust)
}

## MAIN
for(k in 1:itr){
      # BUILDS HORIZONTAL AND VERTICAL BONDS
      xt.m = matrix(xt,n.row,n.col)
      bondv = matrix(0,n.row,n.col)
      bondh = matrix(0,n.row,n.col)
      for(j in 1:n.col){
      for(i in 1:n.row){
            if(i%%n.row != 0)
            {bondv[i,j] = runif(1,0,exp(b*(xt.m[i,j]==xt.m[i+1,j])))}
            if(j%%n.col != 0)
            {bondh[i,j] = runif(1,0,exp(b*(xt.m[i,j]==xt.m[i,j+1])))}
      }
      }
      bondv = bondv>1
      bondh = bondh>1
      bv = as.vector(bondv)
      bh = as.vector(bondh)

      # ASSIGNS COLORS TO CLUSTERS
      clust.check = rep(1,n)
      for(pos in 1:n){
            if(clust.check[pos]){
            clust = cluster(pos)
            q = g(clust)
            d = rbinom(1,1,q)
            xt[clust] = d
            clust.check[clust]=0
            }
      }
      xt.all[k,] = xt
}
xt.p = colMeans(xt.all)
x.est = (xt.p>=.5)
p.correct = 1-mean(abs(x.est - x))

## OUTPUT
                 # PERCENT OF CORRECT ESTIMATES 
p.correct        # POSTERIOR MEAN >= .5 IS CLASSIFIED AS 1, ELSE 0

## PLOTS
par(pty="s",mfrow=c(2,2))
x.image = matrix(x,n.row,n.col)
x.image = x.image[,n.col:1]
image(1:n.row,1:n.col,x.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="True presence-absence")

y.image = matrix(y,n.row,n.col)
y.image = y.image[,n.col:1]
image(1:n.row,1:n.col,y.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="Obs presence-absence")

xt.p.image = matrix(xt.p,n.row,n.col)
xt.p.image = xt.p.image[,n.col:1]
image(1:n.row,1:n.col,xt.p.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="Est presence-absence")


############################################################################
### EXAMPLE 8.9 UTAH SERVICEBERRY DISTRIBUTION (CFTP)
############################################################################
# utahserviceberry.dat = contains data
# x         = true presence-absence information
# y         = observed presence-absence information
#             (1=presence, 0=absence)
# a         = alpha parameter 
# b         = beta parameter
# y2        = alternate coding of y (-1=presence, 1=absence)
# xt.black  = estimated presence-absence information for max space
#             (1=presence, 0=absence)
# x2.black  = alternate coding of max space (-1=presence, 1=absence)
# xt.white  = estimated presence-absence information for min space
#             (1=presence, 0=absence)
# x2.white  = alternate coding of min space (-1=presence, 1=absence)
# tau       = time to reach stationary distribution of the chain
# f         = computes probability of setting pixel(pos) to 1 (presence)
# neighbors = finds indices of the neighbors to pixel(pos)
############################################################################
## INITIAL VALUES
utahserviceberry.dat = read.table(file.choose())
x = utahserviceberry.dat[,1]
a = 1
b = 0.8
set.seed(0)
y = x
n.row = 54
n.col = 46
n = n.row*n.col
bad = sample.int(n,745)
y[bad] = !y[bad]
y2 = (!y) - y
xt.black = rep(1,n)
xt.white = rep(0,n)
x2.black = rep(-1,n)
x2.white = rep(1,n)
done = FALSE
tau = 0

## FUNCTIONS
f = function(pos){
      k = neighbors(pos)
      out = NULL
      out[1] = (1 + exp(a*y2[pos] + b*sum(x2.black[k])))^-1
      out[2] = (1 + exp(a*y2[pos] + b*sum(x2.white[k])))^-1
      return(out)
}
neighbors = function(pos){
      if((pos-1)%%n.row != 0 & pos%%n.row != 0){
            out = c(pos-1,pos+1,pos-n.row,pos+n.row)
            out = out[out>0 & out<(n+1)]
      }
      if((pos-1)%%n.row == 0 | pos%%n.row == 0){
            if(pos%%n.row != 0){
                  out = c(pos+1,pos-n.row,pos+n.row)
                  out = out[out>0 & out<(n+1)]
            }
            if(pos%%n.row == 0){
                  out = c(pos-1,pos-n.row,pos+n.row)
                  out = out[out>0 & out<(n+1)]
            }
      }
      return(out)
}

## MAIN
while(!done){
      for(i in 1:n){
            q = f(i)
            d = runif(1,0,1) < q
            xt.black[i] = d[1]
            xt.white[i] = d[2]
            x2.black[i] = 1-2*d[1]
            x2.white[i] = 1-2*d[2] 
      }
      if(sum(xt.black == xt.white)==n){done = TRUE}
      tau = tau + 1
}


## OUTPUT
tau      # TIME TO REACH STATIONARY DISTRIBUTION OF THE CHAIN

#percent correct 
#This is quite poor.  Students:  improve the algorithm to see if you can improve % correct
1-mean(abs(xt.image-x))


## PLOTS
par(pty="s",mfrow=c(2,2))
x.image = matrix(x,n.row,n.col)
x.image = x.image[,n.col:1]
image(1:n.row,1:n.col,x.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="True presence-absence")

y.image = matrix(y,n.row,n.col)
y.image = y.image[,n.col:1]
image(1:n.row,1:n.col,y.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="Obs presence-absence")

xt.image = matrix(xt.black,n.row,n.col)
xt.image = xt.image[,n.col:1]
image(1:n.row,1:n.col,xt.image, xlab="", ylab="", xaxt="n", yaxt="n",
      main="Stationary distribution")


############################################################################
### END OF FILE
