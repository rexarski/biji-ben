setwd('/Users/akbota/Documents/STA601/Labs/lab8')
data <- read.table("data.txt", stringsAsFactors=F)
x=as.numeric(data[2:101,1])

a=0.5
b=0.5
mu0=0
tau0=15
N=10000
n=100
sig_sq<-c(2)
mu<-c(1)

#Gibbs sampling

for(i in 2:N){
  V=(n/sig_sq[i-1]+1/tau0)^(-1)
  M=V*(sum(log(x))/sig_sq[i-1]+mu0/tau0)
  mu[i]<-rnorm(1,M,sqrt(V))
  
  sumforf=0
  for(j in 1:n){
    sumforf=(log(x[j])-mu[i])^2+sumforf
  }
  f<-rgamma(1,shape=a+n/2, rate=b+0.5*sumforf)
  sig_sq[i]=1/f
}

#post burn-in plots

plot(mu[2001:10000], type='l', ylab=expression(mu), xlab="iterations")
plot(sig_sq[2001:10000], type='l', ylab=expression(sigma^2), xlab="iterations")

#CIs for mean and variance of lognormal

mean<-exp(mu[2001:10000]+sig_sq[2001:10000]/2)
var<-(exp(sig_sq[2001:10000])-1)*exp(2*mu[2001:10000]+sig_sq[2001:10000])

quantile(mean, probs=c(0.025, 0.925))
quantile(var, probs=c(0.025, 0.925))

