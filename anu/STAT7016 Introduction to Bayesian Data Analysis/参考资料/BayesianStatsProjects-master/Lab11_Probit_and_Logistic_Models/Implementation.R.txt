library(truncnorm)
library(mvtnorm)
library(optimbase)

setwd('/Users/akbota/Documents/STA601/Labs/lab11')
d<- read.csv("data.csv")

n=35
y=d$y
X=matrix(data=rep(1), nrow=n, ncol=4)
X[,2]=d$age
X[,3]=d$course
X[,4]=d$likeStats


N=12000
b0=rep(0,4)
B0=diag(4)

beta=matrix(nrow=4, ncol=N)
beta[,1]=rep(1,4)
y.star=matrix(nrow=n,ncol=N)

for(t in 2:N){
  
  for(i in 1:n){
    if(y[i]==1){
      y.star[i,t]=rtruncnorm(1, a=0, mean=X[i,]%*%beta[,t-1])
    }else if(y[i]==0){
      y.star[i,t]=rtruncnorm(1, b=0, mean=X[i,]%*%beta[,t-1])
    }
  }

  B=solve(solve(B0)+transpose(X)%*%X)
  b=B%*%(solve(B0)%*%b0+transpose(X)%*%y.star[,t])
  beta[,t]=rmvnorm(1, mean=b, sigma=B)
  
  
  if(t%%1000==0){
    print(t)
  }
}

plot(beta[2,], type='l', ylab=expression(beta[age]), xlab="iterations")
plot(y.star[2,], type='l', ylab=expression(y[2]^star), xlab="iterations")

Beta=c(mean(beta[1,2001:N]), mean(beta[2,2001:N]), mean(beta[3,2001:N]), mean(beta[4,2001:N]))

x.TA=c(1,26,0,1)
yis1.TA=pnorm(transpose(beta[,2001:N])%*%x.TA)

hist(yis1.TA, xlab="probability of an accident", main="Histogram")

pty.yis1.TA=pnorm(x.TA%*%Beta)

x1=c(1,17,1,0)
x2=c(1,18,1,1)
ptyx1=pnorm(x1%*%Beta)
ptyx2=pnorm(x2%*%Beta)
