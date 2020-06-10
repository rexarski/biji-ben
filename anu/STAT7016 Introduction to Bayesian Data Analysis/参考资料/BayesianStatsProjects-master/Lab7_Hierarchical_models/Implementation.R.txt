#Akbota Anuarbek

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
tau=tau0=tau1=mu0=mu1=rep(NA,M)

beta1[1,]=1
beta0[1,]=10
tau[1] = tau0[1]=tau1[1]= mu1[1] = .3; mu0[1] = 11
mui0 = mui1 = rep(NA,N)
SUMX.sq = sum(X^2)


for(k in 2:M){
  
  
  sum.for.lambda =0
  for(i in 1:N){
    sum.for.lambda = sum.for.lambda + sum(Y[i,] - beta0[k-1,i]-beta1[k-1,i]*X)^2
  }
  #sum.for.lambda
  tau[k] =rigamma(1, N*T/2+a, 1/2*sum.for.lambda+lambda)
  
  
  
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
  
  sigmai0= (10*(tau[k])^(-1)+(tau0[k])^(-1))^(-1/2)
  for(i in 1:N){
    mui0[i] = (sum(Y[i,])-beta1[k-1,i]*sum(X))/tau[k]+mu0[k]/tau0[k]
  }
  beta0[k,] = rnorm(N, mui0*sigmai0^2, sigmai0)
  
  sigmai1 = (SUMX.sq/tau[k]+ 1/tau1[k])^(-1/2)
  # SUMX.sq = sum(X^2) is defined above (outside of loop)
  for(i in 1:N){
    mui1[i] = (sum(Y[i,]*X)-beta0[k,i]*sum(X))/tau[k] + mu1[k]/tau1[k]
  }
  beta1[k,] = rnorm(N, mui1*sigmai1^2, sigmai1)
  
  if(k%%1000==0){print(k)}
}

#approximate probability that new patient has slope greater than 0.5
p_beta1<-c()
for(i in 1001:5000){
  p_beta1[i-1000]=rnorm(1, mean=mu1[i], sd=sqrt(tau1[i]))  
}
mean(p_beta1>0.5)

#plots for tau
plot(tau[1001:5000], type='l', ylab=expression(tau), xlab='iterations', col="red")
acf(tau[1001:5000], col="red", main=expression(tau))

#plots for other variables
plot(tau1[1001:5000], type='l', ylab=expression(tau[1]), xlab='iterations')
plot(tau0[1001:5000], type='l', ylab=expression(tau[0]), xlab='iterations')
plot(mu1[1001:5000], type='l', ylab=expression(mu[1]), xlab='iterations')
plot(mu0[1001:5000], type='l', ylab=expression(mu[0]), xlab='iterations')
plot(beta1[1001:5000,1], type='l', ylab=expression(beta['1 1']), xlab='iterations')
plot(beta1[1001:5000,10], type='l', ylab=expression(beta['1 10']), xlab='iterations')
plot(beta0[1001:5000,25], type='l', ylab=expression(beta['0 25']), xlab='iterations')
plot(beta0[1001:5000,33], type='l', ylab=expression(beta['0 33']), xlab='iterations')

