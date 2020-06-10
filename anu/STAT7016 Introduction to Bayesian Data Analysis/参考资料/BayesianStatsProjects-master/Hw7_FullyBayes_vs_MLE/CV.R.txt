x_trng<-x[1:90,]
x_test<-x[91:100,]
y_trng<-y[1:90]
y_test<-y[91:100]
n=90
mse<-c()
post_mean<-matrix(c(0,0,0), 10, 3)

N<-1000
tau2<-c(1, 10, 25, 34, 40, 50, 63, 75, 83, 100)
sig_sq<-c(1)
B<-matrix(c(10,10,10), N, 3)
c=0.5
d=0.5
v0=1
sig0sq=1

for(j in 1:10){
  for(i in 2:N){
    SSR=t(y_trng)%*%y_trng-2*t(B[i-1,])%*%t(x_trng)%*%y_trng+t(B[i-1,])%*%t(x_trng)%*%x_trng%*%B[i-1,]
    f=rgamma(1, shape=(v0+n)/2, rate=(v0*sig0sq+SSR)/2)
    sig_sq[i]=1/f
    
    Sigma0<-(tau2[j]^(-1))*sig_sq[i]*diag(3)
    V=solve(solve(Sigma0)+1/(sig_sq[i])*t(x_trng)%*%x_trng)
    E=solve(solve(Sigma0)+t(x_trng)%*%x_trng*1/(sig_sq[i]))%*%(t(x_trng)%*%y_trng*1/(sig_sq[i]))
    B[i,]=mvrnorm(n=1, mu=E, Sigma=V)
  }
  
  post_mean[j,]<-c(mean(B[100:N,1]), mean(B[100:N,2]), mean(B[100:N,3]))
  mse[j]=(t(y_test-x_test%*%post_mean[j,])%*%(y_test-x_test%*%post_mean[j,]))/10
}

index<-which.min(mse)
b_cv<-post_mean[index,]
mse_cv=mse[index]