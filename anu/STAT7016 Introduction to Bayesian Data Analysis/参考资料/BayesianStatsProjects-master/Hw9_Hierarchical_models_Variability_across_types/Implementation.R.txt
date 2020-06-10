#assume hyperparameters have the following values
a=0.5
b=0.5
c=0.5
d=0.5

#randomly pick #of costumes and #of children wearing each type
n<-sample(20:50,1)
n_i<-sample(20:50,n, replace=TRUE)

#assume true parameter values
theta=10
phi=10
lambda<-rgamma(n,shape=f,rate=f)

#generate data, letting t_ij be measured in hours
t<-matrix(NA,n, max(n_i))
y<-matrix(NA,n, max(n_i))
for(i in 1:n){
  for(j in 1:n_i[i]){
    t[i,j]<-sample(1:5,1, replace=TRUE)
    y[i,j]<-rpois(1,theta*lambda[i]*t[i,j])
  }
}

N<-10000
th<-c(1)
f<-c(5)
l<-matrix(NA,N,n)
l[1,]<-1
epsilon=1

for(k in 2:N){
  
  #update theta
  sum_y<-0
  sum_t<-0
  for(i in 1:n){
    for(j in 1:n_i[i]){
      sum_y=sum_y+y[i,j]
      sum_t=sum_t+t[i,j]*l[k-1,i]
    }
  }
  th[k]<-rgamma(1,shape=a+sum_y, rate=b+sum_t)
  
  #update all lambdas
  
  for(i in 1:n){
    l[k,i]<-rgamma(1, shape=f[k-1]+sum(y[i,1:n_i[i]]), rate=f[k-1]+th[k]*sum(t[i,1:n_i[i]]))
  }
  

  #update phi Metropolis Algo
  ff<-rgamma(1,shape=f[k-1]*epsilon, rate=epsilon)
  
  product.num=dgamma(x=ff, shape=c, rate=d, log=TRUE)+dgamma(x=f[k-1], shape=ff*epsilon, rate=epsilon, log=TRUE)
  product.denom=dgamma(x=f[k-1], shape=c, rate=d, log=TRUE)+dgamma(x=ff, shape=f[k-1]*epsilon, rate=epsilon, log=TRUE)
  for(i in 1:n){
    product.num=product.num+dgamma(x=l[k,i],shape=ff, rate=ff, log=TRUE)
    product.denom=product.denom+dgamma(x=l[k,i], shape=f[k-1], rate=f[k-1], log=TRUE)
  }
  
  alpha<-min(1, exp(product.num-product.denom))
  r<-runif(1)
  if(r<=alpha){
    f[k]=ff
  }else{
    f[k]=f[k-1]
  }
  
  #counter
  if(k%%2000==0){
    print(k)
  }
}


#derive posterior estimates

theta.hat=mean(th[2001:N])
phi.hat=mean(f[2001:N])
lambda.hat<-c()
for(s in 1:n){
  lambda.hat[s]=mean(l[2001:N,s])
}

plot(lambda, main="True parameter values vs. Bayes estimates", xlab="i", ylab=expression(lambda[i]))
points(lambda.hat, col="red")
legend(n-5, 2, c(expression(hat(lambda[i])), expression(lambda[i])), pt.lwd=c(2,2), pch=c(1,1), col=c("red","black"))
