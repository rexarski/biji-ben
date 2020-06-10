library(truncnorm)

setwd('/Users/akbota/Documents/STA601/Labs/lab10')
data<- read.table("data.txt", stringsAsFactors=F)

y<-as.numeric(data[2:101,1])

N<-12000
a=1
b=1
c=1
d=1
m1=0
m2=0
tau1=100
tau2=100
n=length(y)
ss1<-c(3)
ss2<-c(3)
mu1<-c(2)
mu2<-c(1)
th<-c(0.5)
z<-c()

#Gibbs

for(t in 2:N){
  
  for(i in 1:n){
    term1=th[t-1]*(y[i]*sqrt(ss1[t-1]*2*pi))^(-1)*exp(-((log(y[i])-mu1[t-1])^2)/(2*ss1[t-1]))
    term2=(1-th[t-1])*(y[i]*sqrt(ss2[t-1]*2*pi))^(-1)*exp(-((log(y[i])-mu2[t-1])^2)/(2*ss2[t-1]))
      
    z[i]<-rbinom(1, 1, prob=term1/(term1+term2))
  }
  
  V1=(1/tau1+sum(z)/ss1[t-1])^(-1)
  M1=V1*(m1/tau1+sum(z*log(y))/ss1[t-1])
  V2=(1/tau2+sum(1-z)/ss2[t-1])^(-1)
  M2=V2*(m2/tau2+sum((1-z)*log(y))/ss2[t-1])
  
  mu1[t]<-rnorm(n=1, mean=M1, sd=sqrt(V1))
  mu2[t]<-rtruncnorm(n=1, b=mu1[t], mean=M2, sd=sqrt(V2))
  
  f<-rgamma(1, shape=a+0.5*sum(z), rate=b+0.5*sum(z*(log(y)-mu1[t])^2))
  ss1[t]=1/f
  
  f<-rgamma(1, shape=c+0.5*sum(1-z), rate=d+0.5*sum((1-z)*(log(y)-mu2[t])^2))
  ss2[t]=1/f
  
  th[t]=rbeta(1, shape1 = 5+sum(z), shape2 = 2+n-sum(z))
  
  if(t%%100==0){
    print(t)
  }
}

plot(mu1[2001:N], type='l', xlab='iterations', ylab=expression(mu[1]))
plot(th[2001:N], type='l', xlab='iterations', ylab=expression(theta))

#part3
plot(mu1[2001:N], mu2[2001:N], xlab=expression(mu[1]), ylab=expression(mu[2]), col="purple")

#part4
mean(th[2001:N]*100)
quantile(th[2001:N]*100, c(0.025, 0.975))
mean(th[2001:N]>=5/7)

#part5
mean(mu1[2001:N])
quantile(mu1[2001:N], c(0.025, 0.975))
mean(mu2[2001:N])
quantile(mu2[2001:N], c(0.025, 0.975))
mean(ss1[2001:N])
quantile(ss1[2001:N], c(0.025, 0.975))
mean(ss2[2001:N])
quantile(ss2[2001:N], c(0.025, 0.975))



