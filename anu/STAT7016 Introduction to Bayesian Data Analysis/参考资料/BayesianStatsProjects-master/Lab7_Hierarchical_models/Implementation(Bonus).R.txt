#Bonus: R-code for the case with unequal variances

#setwd('/Users/akbota/Documents/STA601/Labs/lab7')
setwd('/net/nfs1/s/grad/dnv2/Desktop')
data=read.table('hier.txt')
dim(data)


Y = as.matrix(na.omit(data[,2:11]))
X = 1:10 - mean(1:10)

#looking at some data, which is technically cheating
plot(X,Y[1,])
plot(X,Y[2,])
plot(X,Y[67,])

#install.packages('pscl')
library(pscl)
hist(invGammaDraws<-rigamma(10000,5,4))

#setting hyperparameters
a=5
lambda=4
m0 = 12
m1 = 1
s0.sq = 1
s1.sq = 1



N=nrow(Y)
T=ncol(Y)
M=5000


beta1 = beta0 = matrix(nrow=M, ncol=nrow(Y))

##setting starting values
tau=matrix(nrow=M, ncol=nrow(Y))

tau0=tau1=mu0=mu1=rep(NA,M)

beta1[1,]=1
beta0[1,]=10
tau[1,]=.3
tau0[1]=tau1[1]= mu1[1] = .3; mu0[1] = 11
mui0 = mui1 = rep(NA,N)
sigmai0 = sigmai1 = rep(NA,N)
SUMX.sq = sum(X^2)


for(k in 2:M){
  
  for(i in 1:N){
    tau[k,i] =rigamma(1, T/2+a, 1/2*(sum(Y[i,] - beta0[k-1,i]-beta1[k-1,i]*X)^2)+lambda)
  }
 
  sum.for.lambda0 =0
  for(i in 1:N){
    sum.for.lambda0 = sum.for.lambda0 + sum(beta0[k-1,i] - mu0[k-1])^2
  }
  tau0[k] =rigamma(1, N/2+a, 1/2*sum.for.lambda0+lambda)
  
  
  sum.for.lambda1 =0
  for(i in 1:N){
    sum.for.lambda1 = sum.for.lambda1 + sum(beta1[k-1,i] - mu1[k-1])^2
  }
  tau1[k] =rigamma(1, N/2+a, 1/2*sum.for.lambda1+lambda) 
  
  
  sigstar<-(N/tau0[k] + 1/s0.sq)^(-1/2)
  mustar<- (sum(beta0[k-1,])/tau0[k] + m0/s0.sq )*sigstar^2
  mu0[k] = rnorm(1, mustar, sigstar)
  
  
  sigstar<-(N/tau1[k] + 1/s1.sq)^(-1/2)
  mustar<- (sum(beta1[k-1,])/tau1[k] + m1/s1.sq )*sigstar^2
  mu1[k] = rnorm(1, mustar, sigstar)
  
  
  
  ### Fill in the blanks  
  
  
  for(i in 1:N){
    sigmai0[i]= (10*(tau[k,i])^(-1)+(tau0[k])^(-1))^(-1/2)
    mui0[i] = (sum(Y[i,])-beta1[k-1,i]*sum(X))/tau[k,i]+mu0[k]/tau0[k]
  }
  beta0[k,] = rnorm(N, mui0*sigmai0^2, sigmai0)
  
  sigmai1 = (SUMX.sq/tau[k]+ 1/tau1[k])^(-1/2)
  # SUMX.sq = sum(X^2) is defined above (outside of loop)
  for(i in 1:N){
    sigmai1[i] = (SUMX.sq/tau[k,i]+ 1/tau1[k])^(-1/2)
    mui1[i] = (sum(Y[i,]*X)-beta0[k,i]*sum(X))/tau[k,i] + mu1[k]/tau1[k]
  }
  beta1[k,] = rnorm(N, mui1*sigmai1^2, sigmai1)
  
  if(k%%1000==0){print(k)}
}

#plots for some tau's to check autocorrelation
plot(tau[1001:5000,10], type='l', ylab=expression(tau[10]), xlab='iterations')
plot(tau[1001:5000,15], type='l', ylab=expression(tau[15]), xlab='iterations')
plot(tau[1001:5000,40], type='l', ylab=expression(tau[40]), xlab='iterations')
plot(tau[1001:5000,65], type='l', ylab=expression(tau[65]), xlab='iterations')