#randomly generate betas
p<-100
z<-sample(1:p, 5, replace=FALSE)
beta<-rep(0, p)
for(i in 1:5){
  beta[z[i]]<-rnorm(1, mean=0, sd=sqrt(2))
}

#generate data using betas
library(MASS)
n<-100
err<-rnorm(n, mean=0, sd=1)
mu<-rep(0,p)
Sigma=diag(p)
x<-mvrnorm(n=n,mu=mu,Sigma=Sigma)
y<-x%*%beta+err

#fully Bayes ridge
N<-2000
a=1
b=1
c=0.5
d=0.5

tau<-c(1)
sig_sq<-c(1)
B<-matrix(rep(1, p), N, p)

for(i in 2:N){
  V=solve((t(x)%*%x/sig_sq[i-1]+tau[i-1]*diag(p)/sig_sq[i-1]))
  M=V%*%t(x)%*%y/sig_sq[i-1]
  B[i,]<-mvrnorm(n=1, mu=M , Sigma=V)
  
  SSR=t(y-x%*%B[i,])%*%(y-x%*%B[i,])
  f=rgamma(1, shape=a+n/2, rate=b+SSR/2)
  sig_sq[i]=1/f
  
  tau[i]=rgamma(1, shape=c+p/2, rate=d+0.5*t(B[i,])%*%B[i,]/sig_sq[i])
  
  if(i%%500==0){
    print(i)
  }
}

beta_bayes<-c()
for(j in 1:p){
  beta_bayes[j]<-mean(B[200:N,j])
}

#t-prior with v=1
N<-2000
a=1
b=1
c=0.5
d=0.5
v=1

tau<-c(1)
sig_sq<-c(1)
B<-matrix(rep(1, p), N, p)
lambda<-matrix(rep(1,p), N, p)

for(i in 2:N){
  Sigma_l=diag(1/lambda[i-1,1:p])
  Sigma0=sig_sq[i-1]*(tau[i-1]^(-1))*Sigma_l
  V=solve(t(x)%*%x/sig_sq[i-1]+solve(Sigma0))
  M=V%*%t(x)%*%y/sig_sq[i-1]
  B[i,]=mvrnorm(n=1, mu=M, Sigma=V)
  
  SSR=t(y-x%*%B[i,])%*%(y-x%*%B[i,])
  f=rgamma(1, shape=a+n/2, rate=b+SSR/2)
  sig_sq[i]=1/f
  
  tau[i]=rgamma(1, shape=c+p/2, rate=d+0.5/sig_sq[i]*t(B[i,])%*%solve(Sigma_l)%*%B[i,])
  
  for(j in 1:p){
    lambda[i,j]=rgamma(1,shape=(v+1)/2, rate=(v+tau[i]/sig_sq[i]*B[i,j]^2)/2)
  }
  
  if(i%%500==0){
    print(i)
  }
}

beta_t1<-c()
for(j in 1:p){
  beta_t1[j]<-mean(B[200:N,j])
}

#t-prior with v=0.001
N<-2000
a=1
b=1
c=0.5
d=0.5
v=0.001

tau<-c(1)
sig_sq<-c(1)
B<-matrix(rep(1, p), N, p)
lambda<-matrix(rep(1,p), N, p)

for(i in 2:N){
  Sigma_l=diag(1/lambda[i-1,1:p])
  Sigma0=sig_sq[i-1]*(tau[i-1]^(-1))*Sigma_l
  V=solve(t(x)%*%x/sig_sq[i-1]+solve(Sigma0))
  M=V%*%t(x)%*%y/sig_sq[i-1]
  B[i,]=mvrnorm(n=1, mu=M, Sigma=V)
  
  SSR=t(y-x%*%B[i,])%*%(y-x%*%B[i,])
  f=rgamma(1, shape=a+n/2, rate=b+SSR/2)
  sig_sq[i]=1/f
  
  tau[i]=rgamma(1, shape=c+p/2, rate=d+0.5/sig_sq[i]*t(B[i,])%*%solve(Sigma_l)%*%B[i,])
  
  for(j in 1:p){
    lambda[i,j]=rgamma(1,shape=(v+1)/2, rate=(v+tau[i]/sig_sq[i]*B[i,j]^2)/2)
  }
  
  if(i%%500==0){
    print(i)
  }
}

beta_t2<-c()
for(j in 1:p){
  beta_t2[j]<-mean(B[200:N,j])
}

#Lasso
las <- lars(x, y, type="lasso", intercept=FALSE)
beta_lasso = coef(las, s=5, mode="lambda") 

#plots
plot(beta, ylab=expression(beta[i]), xlab=expression(i), main="Fully Bayes ridge")
points(beta_bayes, col="brown")

plot(beta, ylab=expression(beta[i]), xlab=expression(i), main="t-prior with v=1")
points(beta_t1, col="red")

plot(beta, ylab=expression(beta[i]), xlab=expression(i), main="t-prior with v=0.01")
points(beta_t2, col="blue")

plot(beta, ylab=expression(beta[i]), xlab=expression(i), main="Lasso")
points(beta_lasso, col="green")

#MSE for Y
mse_bayes=t(y-x%*%beta_bayes)%*%(y-x%*%beta_bayes)/n
mse_t1=t(y-x%*%beta_t1)%*%(y-x%*%beta_t1)/n
mse_t2=t(y-x%*%beta_t2)%*%(y-x%*%beta_t2)/n
mse_lasso=t(y-x%*%beta_lasso)%*%(y-x%*%beta_lasso)/n

