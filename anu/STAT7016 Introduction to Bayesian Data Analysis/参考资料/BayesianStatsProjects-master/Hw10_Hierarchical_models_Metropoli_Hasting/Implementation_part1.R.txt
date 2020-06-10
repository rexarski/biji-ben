library(mvtnorm)
library(optimbase)

setwd('/Users/akbota/Documents/STA601/HWs/hw10')
data<- read.table("BP.csv", header=TRUE)

m<-length(data$id) #number of observations in total
n<-length(unique(data$id)) #number of people

#modify data id's
data$newid[1]=1
d=1
for(j in 2:m){
  if(data$id[j]!=data$id[j-1]){
    d=d+1
  }
  data$newid[j]=d
}
data$id<-NULL
names(data)[4]="id"

#normalize y's
y<-data$BP_syst/data$BP_dia
y<-(y-mean(y))/sd(y)

id=data$id

x=x=matrix(data=c(rep(1,m), data$age), ncol=2, nrow=m)
z=x

#Gibbs

N<-2000
a<-1
b<-1

beta<-matrix(rep(NA), nrow=N, ncol=2)
beta[1,]=rep(0,2)

alpha<-matrix(rep(NA), nrow=n, ncol=2*N)
alpha[,1:2]=0

sig.sq<-c(1)

Omega<-matrix(rep(NA),nrow=2*N, ncol=2)
Omega[1:2,]<-riwish(v=3, S=diag(2))

for(k in 2:N){
  
  #y*
  y.star<-c()
  j=1
  for(i in id){
    y.star[j]=y[j]-z[j,]%*%alpha[i,(2*(k-1)-1):(2*(k-1))]
    j=j+1
  }
  
  #update beta
  V1=solve(t(x)%*%x/sig.sq[k-1]+diag(2))
  M1=V1%*%t(x)%*%y.star/sig.sq[k-1]
  beta[k,]=rmvnorm(1, mean=M1, sigma=V1)
  
  #update sigma^2
  f=rgamma(1,shape=a+m/2, rate=b+0.5*t(y.star-x%*%beta[k-1,])%*%(y.star-x%*%beta[k-1,]))
  sig.sq[k]=1/f
  
  #y.tilde
  y.t=y-x%*%beta[k-1,]
  
  
  #update alpha's
  i2=0
  i1=1
  for(t in 1:n){
    l=length(which(id==t))
    i2=i2+l
    z_i=z[i1:i2,]
    V2=solve(transpose(z_i)%*%z_i/sig.sq[k-1]+solve(Omega[(2*(k-1)-1):(2*(k-1)),]))
    M2=V2%*%transpose(z_i)%*%y.t[i1:i2]/sig.sq[k-1]
    alpha[t,(2*k-1):(2*k)]=rmvnorm(1,mean=M2, sigma=V2)
    i1=i1+l
  }
  
  #update Omega
  A=t(alpha[,(2*(k-1)-1):(2*(k-1))])%*%alpha[,(2*(k-1)-1):(2*(k-1))]
  Omega[(2*k-1):(2*k),]=riwish(v=3+n, S=A+diag(2))
  
  
  print(k)
}

alpham1=matrix(nrow=n,ncol=2)

for(row in 1:n){
  a1<-0
  a2<-0
  s=2001
  for(counter in 1:1000){
    a1=a1+alpha[row, s]
    a2=a2+alpha[row, s+1]
    s=s+2
  }
  alpham1[row,1]=a1/1000
  alpham1[row,2]=a2/1000
}

Omega1=cov(alpham1)

beta1=mean(beta[1001:N,1])
beta1nb=mean(beta[,1])
beta2=mean(beta[1001:N,2])
beta2nb=mean(beta[,2])

b1CI=quantile(beta[1001:N,1], c(0.025, 0.975))
b2CI=quantile(beta[1001:N,2], c(0.025, 0.975))

sigma.sq=mean(sig.sq[1001:N])
ssCI=quantile(sig.sq, c(0.025, 0.975))

