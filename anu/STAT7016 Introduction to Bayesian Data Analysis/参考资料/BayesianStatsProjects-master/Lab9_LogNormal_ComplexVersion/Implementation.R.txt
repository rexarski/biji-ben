setwd('/Users/akbota/Documents/STA601/Labs/lab9')
data <- read.table("data.txt", stringsAsFactors=F)
data=data[-1,]

#weekdays
x=as.numeric(data[data[,2]!="Saturday" & data[,2]!="Sunday",1])

#weekends
y=as.numeric(data[data[,2]=="Saturday" | data[,2]=="Sunday",1])

#initialize variables
a=1
b=1
c=1
d=1
mu1.0=0
mu2.0=0
tau1=100
tau2=100
N=12000
n1=length(x)
n2=length(y)
sig_sq1<-c(3)
sig_sq2<-c(3)
mu1<-c(2)
mu2<-c(1)


#Gibbs
for(i in 2:N){
  
  V1=(n1/sig_sq1[i-1]+1/tau1)^(-1)
  M1=V1*(sum(log(x))/sig_sq1[i-1]+mu1.0/tau1)
  
  V2=(n2/sig_sq2[i-1]+1/tau2)^(-1)
  M2=V2*(sum(log(y))/sig_sq2[i-1]+mu2.0/tau2)
  
  mu1[i]<-rnorm(1,mean=M1, sd=sqrt(V1))
  mu2[i]<-rtruncnorm(1,b=mu1[i],mean=M2,sd=sqrt(V2))

  
  sumforf1=0
  for(j in 1:n1){
    sumforf1=(log(x[j])-mu1[i])^2+sumforf1
  }
  f1<-rgamma(1,shape=a+n1/2, rate=b+0.5*sumforf1)
  sig_sq1[i]=1/f1
  
  sumforf2=0
  for(j in 1:n2){
    sumforf2=(log(y[j])-mu2[i])^2+sumforf2
  }
  f2<-rgamma(1,shape=c+n2/2, rate=c+0.5*sumforf2)
  sig_sq2[i]=1/f2
  
  if(i%%2000==0){
    print(i)
  }
}

#Burn-in
m1=mu1[2001:N]
m2=mu2[2001:N]
ss1=sig_sq1[2001:N]
ss2=sig_sq2[2001:N]

#traceplots
plot(m1, type='l', xlab="iterations", ylab=expression(mu[1]))
plot(ss1, type='l', xlab="iterations", ylab=expression(sigma[1]^2))

#posterior point estimates
mean(m1)
mean(m2)
mean(ss1)
mean(ss2)

#CIs
quantile(m1, probs=c(0.025,0.975))
quantile(m2, probs=c(0.025,0.975))
quantile(ss1, probs=c(0.025,0.975))
quantile(ss2, probs=c(0.025,0.975))

#posterior probabilities
mean(m1>m2)
mean(ss1>ss2)

tues<-c()
sat<-c()
for(k in 1:length(m1)){
  sat[k]<-rlnorm(1,meanlog=exp(m2[k]+ss2[k]/2), sdlog=sqrt((exp(ss2[k])-1)*exp(2*m2[k]+ss2[k])))
  tues[k]<-rlnorm(1,meanlog=exp(m1[k]+ss1[k]/2), sdlog=sqrt((exp(ss1[k])-1)*exp(2*m1[k]+ss1[k])))
}
mean(tues > sat)



