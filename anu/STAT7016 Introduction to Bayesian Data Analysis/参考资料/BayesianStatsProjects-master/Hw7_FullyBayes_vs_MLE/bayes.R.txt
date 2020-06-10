N<-1000
tau<-c(1)
sig_sq<-c(1)
B<-matrix(c(10,10,10), N, 3)
c=0.5
d=0.5
v0=1
sig0sq=1


for(i in 2:N){
  
  tau[i]=rgamma(1, shape=c+n/2, rate=1/(2*sig_sq[i-1])*(B[i-1,]%*%t(B[i-1,]))+d)
  
  SSR=t(y)%*%y-2*t(B[i-1,])%*%t(x)%*%y+t(B[i-1,])%*%t(x)%*%x%*%B[i-1,]
  f=rgamma(1, shape=(v0+n)/2, rate=(v0*sig0sq+SSR)/2)
  sig_sq[i]=1/f
  
  Sigma0<-(tau[i]^(-1))*sig_sq[i]*diag(3)
  V=solve(solve(Sigma0)+1/(sig_sq[i])*t(x)%*%x)
  E=solve(solve(Sigma0)+t(x)%*%x*1/(sig_sq[i]))%*%(t(x)%*%y*1/(sig_sq[i]))
  B[i,]=mvrnorm(n=1, mu=E, Sigma=V)
}

b_bayes<-c(mean(B[100:N,1]), mean(B[100:N,2]), mean(B[100:N,3]))
mse_bayes<-t(y-x%*%b_bayes)%*%(y-x%*%b_bayes)/100