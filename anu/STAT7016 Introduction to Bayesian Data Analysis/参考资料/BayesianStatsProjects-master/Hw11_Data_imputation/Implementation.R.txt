library(MCMCpack) #inv-wishart
library(pscl) #inv-gamma
library(mvtnorm)
library(optimbase)

setwd('/Users/akbota/Documents/STA601/HWs/hw11')
data = read.csv("data_set.csv", header = TRUE)

y=data$Y
n=length(y)
X=matrix(rep(1), nrow=n, ncol=3)
X[,2]=data$X.1
X[,3]=data$X.2

#MLE coeffs
beta.MLE = lm(y~X[,2:3])$coefficients


#Bayes Gibbs

T=3000

a=1
b=1
m.b=c(0,0,0)
m.b=transpose(m.b)
V.b=diag(3)

k0=1
v0=4
L0=diag(2)
mu0=c(0,0)

beta=matrix(ncol=T, nrow=3)
beta[,1]=c(1,1,1)
mu=matrix(ncol=T, nrow=2)
mu[,1]=c(1,1)
sig.sq=c(1)
Sigma=matrix(ncol=2*T, nrow=2)
Sigma[,1:2]=riwish(2,diag(2))

q<-rep(0,n)
for(i in 1:n){
  if(is.na(X[i,2])){
    q[i]=1
    if(is.na(X[i,3])){
      q[i]=3
    }
  }else if(is.na(X[i,3])){
    q[i]=2
  }
}



for(t in 2:T){
  
  #impute missing data
  
  V=solve(solve(Sigma[,(2*(t-1)-1):(2*(t-1))])+transpose(beta[2:3,t-1])%*%beta[2:3,t-1]/sig.sq[t-1])
  
  for(i in 1:n){
    
    if(q[i]!=0){
      M=V%*%(beta[2:3,t-1]*(y[i]+beta[1,t-1])/sig.sq[t-1]+solve(Sigma[,(2*(t-1)-1):(2*(t-1))])%*%mu[,t-1])
      
      if(q[i]==1 ||q[i]==2){
        
        X[i,q[i]+1]=rnorm(1, mean=M[q[i]]+V[1,2]/V[q[i],q[i]]*(X[i,3-q[i]+1]-M[3-q[i]]), sd=sqrt(V[q[i],q[i]]-V[1,2]*V[2,1]/V[3-q[i],3-q[i]])  )
        
      }else{
        X[i,2:3]=mvrnorm(n=1,M,V)
      }
    }
  }
  
  #update beta and sig.sq
  
  V.b.st=solve(solve(V.b)+transpose(X)%*%X)
  m.b.st=V.b.st%*%(solve(V.b)%*%m.b+transpose(X)%*%y)
  a.st=a+n/2
  b.st=b+0.5*(transpose(m.b)%*%solve(V.b)%*%m.b+y%*%transpose(y)-transpose(m.b.st)%*%solve(V.b.st)%*%m.b.st)
  
  sig.sq[t]=rigamma(1,a.st,b.st)
  
  beta[,t]=mvrnorm(n=1,mu=m.b.st, Sigma=sig.sq[t]*V.b.st)
  
  #update mu and Sigma
  
  k.n=k0+n
  mu.n=(k0*mu0+sum(y))/k.n
  v.n=v0+n
  x.bar=c()
  x.bar[1]=mean(X[,2])
  x.bar[2]=mean(X[,3])
  S=sum((X[,2]-x.bar[1])^2)+sum((X[,3]-x.bar[2])^2)
  L.n=L0+S+k0*n/k.n*transpose(x.bar-mu0)%*%(x.bar-mu0)
  
  Sigma[,(2*t-1):(2*t)]=riwish(v.n, L.n)
  mu[,t]=mvrnorm(n=1, mu=mu.n, Sigma=Sigma[,(2*t-1):(2*t)]/k.n)
  
  if(t%%200==0){
    print(t)
  }
  
}


plot(beta[1,], type='l', xlab='iterations', ylab=expression(beta[1]))
plot(sig.sq, type='l', xlab='iterations', ylab=expression(sigma^2))

mean(beta[1,1001:T])
mean(beta[2,1001:T])
mean(beta[3,1001:T])
quantile(beta[1,1001:T], c(0.025, 0.975))
quantile(beta[2,1001:T], c(0.025, 0.975))
quantile(beta[3,1001:T], c(0.025, 0.975))
mean(sig.sq[1001:T])
quantile(sig.sq[1001:T], c(0.025, 0.975))


