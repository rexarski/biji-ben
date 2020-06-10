lm.gprior<-function(y,X,g=dim(X)[1],nu0=1,s20=try(summary(lm(y~-1+X))$sigma^2,silent=TRUE),S=1000)
{

  n<-dim(X)[1] ; p<-dim(X)[2]
  Hg<- (g/(g+1)) * X%*%solve(t(X)%*%X)%*%t(X)
  SSRg<- t(y)%*%( diag(1,nrow=n)  - Hg ) %*%y

  s2<-1/rgamma(S, (nu0+n)/2, (nu0*s20+SSRg)/2 )

  Vb<- g*solve(t(X)%*%X)/(g+1)
  Eb<- Vb%*%t(X)%*%y

  E<-matrix(rnorm(S*p,0,sqrt(s2)),S,p)
  beta<-t(  t(E%*%chol(Vb)) +c(Eb))

  list(beta=beta,s2=s2)                                
}   

 
lmratio.gprior<-function(z0,z1,y,X,g=dim(X)[1],nu0=1,
                s200=mean( lm(y~-1+X[,z0==1])$res^2), 
                s201=mean( lm(y~-1+X[,z1==1])$res^2) ) 
{
  n<-dim(X)[1] 

  X0<-X[,z0==1]
  X1<-X[,z1==1]

  H0<- (g/(g+1)) * X0%*%solve(t(X0)%*%X0)%*%t(X0)
  SS0<- t(y)%*%( diag(1,nrow=n)  - H0 ) %*%y
  p0<-sum(z0==1) 

  H1<- (g/(g+1)) * X1%*%solve(t(X1)%*%X1)%*%t(X1)
  SS1<- t(y)%*%( diag(1,nrow=n)  - H1 ) %*%y
  p1<-sum(z1==1)  
 
   -.5*(p1-p0)*log( 2*pi*(1+g))  + 
    .5*nu0*log(s201/s200) + .5*(nu0+n)*log( (nu0*s200+SS0)/(nu0+s201+SS1) )
}




mselect.gprior<-function(y,X,S=500*dim(X)[2],verb=FALSE) 
{

  Z<-NULL
  z<-rep(1,dim(X)[2] )

  for(s in 1:S) 
  {
  
    for(j in sample(1:p)) 
    {
      z1<-z0<-z  ; z1[j]<-1 ; z0[j]<-0
      r<-lmratio.gprior(z0,z1,y,X)  
      z[j]<-rbinom(1,1,1/(1+exp(-r))) 
     } 
    Z<-rbind(Z,z) 
    if(verb==TRUE) {cat(s,mean(z),"\n") }
    }
  Z
} 

### need something for null model

lpy.X<-function(y,X,
   g=length(y),nu0=1,s20=try(summary(lm(y~-1+X))$sigma^2,silent=TRUE)) 
{
  n<-dim(X)[1] ; p<-dim(X)[2] 
  if(p==0) { s20<-mean(y^2) }
  H0<-0 ; if(p>0) { H0<- (g/(g+1)) * X%*%solve(t(X)%*%X)%*%t(X) }
  SS0<- t(y)%*%( diag(1,nrow=n)  - H0 ) %*%y

  -.5*n*log(2*pi) +lgamma(.5*(nu0+n)) - lgamma(.5*nu0)  - .5*p*log(1+g) +
   .5*nu0*log(.5*nu0*s20) -.5*(nu0+n)*log(.5*(nu0*s20+SS0))
}


####
mselect.gprior<-function(y,X,S=500*dim(X)[2],verb=FALSE) 
{

  Z<-NULL
  z<-rep(1,dim(X)[2] )

  for(s in 1:S)
  {

    for(j in sample(1:p))
    {
      z1<-z0<-z  ; z1[j]<-1 ; z0[j]<-0
      r<-lmratio.gprior(z0,z1,y,X)
      z[j]<-rbinom(1,1,1/(1+exp(-r)))
     }
    Z<-rbind(Z,z)
    if(verb==TRUE) {cat(s,mean(z),"\n") }
    }
  Z
}
#####




