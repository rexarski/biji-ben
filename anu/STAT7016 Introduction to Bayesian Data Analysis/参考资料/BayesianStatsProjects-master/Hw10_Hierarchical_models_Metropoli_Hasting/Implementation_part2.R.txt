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
beta[1,]=rep(0.1,2)

alpha.star<-matrix(rep(NA), nrow=n, ncol=2*N)
alpha.star[,1:2]=0.1

sig.sq<-c(1)

Lambda<-matrix(rep(NA),nrow=2*N, ncol=2)
#Lambda[1:2,]<-matrix(data=c(0,0,0,0), nrow=2, ncol=2) #any matrix may be PSD too!
lll<-matrix(nrow=2,ncol=2)
for(i in 1:2){
  for(j in 1:2){
    lll[i,j]<-rnorm(1,mean=0, sd=1)
  }
}
Lambda[1:2,]=lll

alpha<-matrix(rep(NA), nrow=n, ncol=2*N)
alpha[,1:2]=alpha.star[,1:2]%*%transpose(Lambda[1:2,])

for(k in 2001:N){
  
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
   
  
  
  #update alpha*'s
  i2=0
  i1=1
  for(t in 1:n){
    l=length(which(id==t))
    i2=i2+l
    z_i=z[i1:i2,]
    V2=solve(transpose(Lambda[(2*(k-1)-1):(2*(k-1)),])%*%transpose(z_i)%*%z_i%*%Lambda[(2*(k-1)-1):(2*(k-1)),]/sig.sq[k]+diag(2))
    M2=V2%*%transpose(Lambda[(2*(k-1)-1):(2*(k-1)),])%*%transpose(z_i)%*%y.t[i1:i2]/sig.sq[k]
    alpha.star[t,(2*k-1):(2*k)]=rmvnorm(1,mean=M2, sigma=V2)
    i1=i1+l
  }

  
  #MH
  L<-matrix(nrow=2,ncol=2)
  
  for(i in 1:2){
    for(j in 1:2){
      L[i,j]<-rnorm(1,mean=Lambda[2*(k-1)-(2-i),j], sd=7)
    }
  }
  
  
  prod1<-0
  prod2<-0
  i2=0
  i1=1
  for(t in 1:n){
    
    l=length(which(id==t))
    i2=i2+l
    z_i=z[i1:i2,]
    
    prod1<-prod1+dmvnorm(x=y.t[i1:i2], mean=z_i%*%L%*%alpha.star[t,(2*(k-1)-1):(2*(k-1))], sigma=sig.sq[k-1]*diag(l), log=TRUE)
    prod2<-prod2+dmvnorm(x=y.t[i1:i2], mean=z_i%*%L%*%alpha.star[t,(2*(k-1)-1):(2*(k-1))], sigma=sig.sq[k-1]*diag(l), log=TRUE)
    
    i1=i1+l
  }
  
  p=exp(prod1-prod2)*(exp(-0.5*matrix.trace(t(L)%*%L)))/(exp(-0.5*matrix.trace(t(Lambda[(2*(k-1)-1):(2*(k-1)),]))))
  
  prty=min(1,p)
  
  q=runif(1,min=0,max=1)
  
  if(q<p){
    Lambda[(2*k-1):(2*k),]=L
  }else{
    Lambda[(2*k-1):(2*k),]=Lambda[(2*(k-1)-1):(2*(k-1)),]
  }
  
  alpha[,(2*k-1):(2*k)]=alpha.star[,(2*k-1):(2*k)]%*%transpose(Lambda[(2*k-1):(2*k),])
  
  print(k)
  
  
}


#Posterior inferences

alpham2=matrix(nrow=n,ncol=2)

for(row in 1:n){
  a1<-0
  a2<-0
  s=2001
  for(counter in 1:1000){
    a1=a1+alpha[row, s]
    a2=a2+alpha[row, s+1]
    s=s+2
  }
  alpham2[row,1]=a1/1000
  alpham2[row,2]=a2/1000
}

Omega2=cov(alpham2)

plot(alpham1[,1], col="blue", xlab="i", ylab=expression(alpha[i1]), main="Posterior point estimates method a ")
plot(alpham2[,1], col="red", xlab="i", ylab=expression(alpha[i1]), main="Posterior point estimates method b ")

plot(alpham1[,2], col="blue", xlab="i", ylab=expression(alpha[i2]),  main="Posterior point estimates method a")
plot(alpham2[,2], col="red", xlab="i", ylab=expression(alpha[i2]), main="Posterior point estimates method b ")



beta1_=mean(beta[1001:N,1])
beta1_nb=mean(beta[,1])
beta2_=mean(beta[1001:N,2])
beta2_nb=mean(beta[,2])

b1CI_=quantile(beta[1001:N,1], c(0.025, 0.975))
b2CI_=quantile(beta[1001:N,2], c(0.025, 0.975))
ssCI_=quantile(sig.sq, c(0.025, 0.975))

sigma.sq_=mean(sig.sq[1001:N])

