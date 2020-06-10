r=0.99999
n<-100
err<-rnorm(n, mean=0, sd=1)
mu=c(0,0)
Sigma=matrix(c(1,r,r,1),2,2)
x1_x2<-mvrnorm(n=n,mu=mu,Sigma=Sigma)

x0<-c()
for(i in 1:n){
  x0[i]=1
}
x<-matrix(c(x0,x1_x2),n,3)
b<-c(-1,1,1)

y<-x%*%b+err

b_mle<-solve(t(x)%*%x)%*%t(x)%*%y

mse_mle<-t(y-x%*%b_mle)%*%(y-x%*%b_mle)/100
