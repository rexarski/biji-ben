#########################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 4 EXAMPLES (last update 10/1/2012)
#########################################################################

### EXAMPLE 4.2 EM ALGORITHM (PEPPERED MOTHS)

#########################################################################
# x = observed phenotype counts (carbonaria, insularia, typica)
# n = expected genotype frequencies (CC, CI, CT, II, IT, TT)
# p = allele probabilities (carbonaria, insularia, typica)
# itr = number of iterations
# allele.e = computes expected genotype frequencies
# allele.m = computes allele probabilities
#########################################################################

## INITIAL VALUES
x = c(85, 196, 341)
n = rep(0,6)
p = rep(1/3,3)
itr = 40

## EXPECTATION AND MAXIMIZATION FUNCTIONS
allele.e = function(x,p){
    n.cc = (x[1]*(p[1]^2))/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ci = (2*x[1]*p[1]*p[2])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ct = (2*x[1]*p[1]*p[3])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ii = (x[2]*(p[2]^2))/((p[2]^2)+2*p[2]*p[3])
    n.it = (2*x[2]*p[2]*p[3])/((p[2]^2)+2*p[2]*p[3])
    n = c(n.cc,n.ci,n.ct,n.ii,n.it,x[3])
    return(n)
}

allele.m = function(x,n){
    p.c = (2*n[1]+n[2]+n[3])/(2*sum(x))
    p.i = (2*n[4]+n[5]+n[2])/(2*sum(x))
    p.t = (2*n[6]+n[3]+n[5])/(2*sum(x))
    p = c(p.c,p.i,p.t)
    return(p)
}

## MAIN
for(i in 1:itr){
    n = allele.e(x,p)
    p = allele.m(x,n)
}

## OUTPUT
p    # FINAL ESTIMATE FOR ALLELE PROBABILITIES (p.c, p.i, p.t)


#########################################################################
### EXAMPLE 4.6 -- SEM ALGORITHM (PEPPERED MOTHS)
#########################################################################

#########################################################################
# x = observed phenotype counts (carbonaria, insularia, typica)
# n = expected genotype frequencies (CC, CI, CT, II, IT, TT)
# p = allele probabilities (carbonaria, insularia, typica)
# p.em = em algorithm estimates
# n.em = em algorithm estimates
# itr = number of iterations
# allele.e = computes expected genotype frequencies
# allele.m = computes allele probabilities
#########################################################################

## INITIAL VALUES
x = c(85, 196, 341)
n = rep(0,6)
itr = 40
p = c(0.07, 0.19, 0.74)
p.em = p
theta = matrix(0,3,3)
psi = rep(0,3)
r = matrix(0,3,3)

## EXPECTATION AND MAXIMIZATION FUNCTIONS
allele.e = function(x,p){
    n.cc = (x[1]*(p[1]^2))/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ci = (2*x[1]*p[1]*p[2])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ct = (2*x[1]*p[1]*p[3])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ii = (x[2]*(p[2]^2))/((p[2]^2)+2*p[2]*p[3])
    n.it = (2*x[2]*p[2]*p[3])/((p[2]^2)+2*p[2]*p[3])
    n = c(n.cc,n.ci,n.ct,n.ii,n.it,x[3])
    return(n)
}

allele.m = function(x,n){
    p.c = (2*n[1]+n[2]+n[3])/(2*sum(x))
    p.i = (2*n[4]+n[5]+n[2])/(2*sum(x))
    p.t = (2*n[6]+n[3]+n[5])/(2*sum(x))
    p = c(p.c,p.i,p.t)
    return(p)
}

## COMPUTES EM ALGORITHM ESTIMATES
for(i in 1:itr){
    n.em = allele.e(x,p.em)
    p.em = allele.m(x,n.em)
}

## INTIALIZES THETA
for(j in 1:length(p)){
    theta[,j] = p.em
    theta[j,j] = p[j]
}

## MAIN
for(t in 1:5){
    n = allele.e(x,p)
    p.hat = allele.m(x,n)
    for(j in 1:length(p)){
        theta[j,j] = p.hat[j]
        n = allele.e(x,theta[,j])
        psi = allele.m(x,n)
        for(i in 1:length(p)){
            r[i,j] = (psi[i]-p.em[i])/(theta[j,j]-p.em[j])
        }
    }
    p = p.hat
}

## COMPLETE INFORMATION
iy.hat=matrix(0,2,2)
iy.hat[1,1] = ((2*n.em[1]+n.em[2]+n.em[3])/(p.em[1]^2) +
     (2*n.em[6]+n.em[3]+n.em[5])/(p.em[3]^2))
iy.hat[2,2] = ((2*n.em[4]+n.em[5]+n.em[2])/(p.em[2]^2) +
     (2*n.em[6]+n.em[3]+n.em[5])/(p.em[3]^2))
iy.hat[1,2] = iy.hat[2,1] = (2*n.em[6]+n.em[3]+n.em[5])/(p.em[3]^2)

## COMPUTES STANDARD ERRORS AND CORRELATIONS
var.hat = solve(iy.hat)%*%(diag(2)+t(r[-3,-3])%*%solve(diag(2)-t(r[-3,-3])))
sd.hat = c(sqrt(var.hat[1,1]),sqrt(var.hat[2,2]),sqrt(sum(var.hat)))
cor.hat = c(var.hat[1,2]/(sd.hat[1]*sd.hat[2]),
    (-var.hat[1,1]-var.hat[1,2])/(sd.hat[1]*sd.hat[3]),
    (-var.hat[2,2]-var.hat[1,2])/(sd.hat[2]*sd.hat[3]))

## OUTPUT
sd.hat    # STANDARD ERROR ESTIMATES (pc, pi, pt)
cor.hat   # CORRELATION ESTIMATES ({pc,pi}, {pc,pt}, {pi,pt})


#########################################################################
### (BEYOND EXAMPLE 4.6 BEN ADDED A BOOTSTRAP)
#########################################################################

#########################################################################
# x = observed phenotype counts (carbonaria, insularia, typica)
# n = expected genotype frequencies (CC, CI, CT, II, IT, TT)
# p = allele probabilities (carbonaria, insularia, typica)
# itr = number of iterations
# theta = allele probabilities for psuedo-data
# allele.e = computes expected genotype frequencies
# allele.m = computes allele probabilities
#########################################################################

## INITIAL VALUES
x = c(85, 196, 341)
n = rep(0,6)
p = rep(1/3,3)
itr = 40
theta = matrix(0,3,10000)
set.seed(0)

## EXPECTATION AND MAXIMIZATION FUNCTIONS
allele.e = function(x,p){
    n.cc = (x[1]*(p[1]^2))/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ci = (2*x[1]*p[1]*p[2])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ct = (2*x[1]*p[1]*p[3])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ii = (x[2]*(p[2]^2))/((p[2]^2)+2*p[2]*p[3])
    n.it = (2*x[2]*p[2]*p[3])/((p[2]^2)+2*p[2]*p[3])
    n = c(n.cc,n.ci,n.ct,n.ii,n.it,x[3])
    return(n)
}
allele.m = function(x,n){
    p.c = (2*n[1]+n[2]+n[3])/(2*sum(x))
    p.i = (2*n[4]+n[5]+n[2])/(2*sum(x))
    p.t = (2*n[6]+n[3]+n[5])/(2*sum(x))
    p = c(p.c,p.i,p.t)
    return(p)
}

## MAIN
for(i in 1:itr){
    n = allele.e(x,p)
    p = allele.m(x,n)
}
theta[,1] = p
for(j in 2:10000){
   n.c = rbinom(1, sum(x), x[1]/sum(x))
   n.i = rbinom(1, sum(x) - n.c, x[2]/(sum(x)-x[1]))
   n.t = sum(x) - n.c - n.i
   x.new = c(n.c, n.i, n.t)
   n = rep(0,6)
   p = rep(1/3,3)
   for(i in 1:itr){
       n = allele.e(x.new,p)
       p = allele.m(x.new,n)
   }
   theta[,j] = p
}

sd.hat = c(sd(theta[1,]), sd(theta[2,]), sd(theta[3,]))
cor.hat = c(cor(theta[1,],theta[2,]), cor(theta[1,],theta[3,]),
    cor(theta[2,],theta[3,]))

## OUTPUT
theta[,1] # EM ESTIMATE FOR ALLELE PROBABILITIES (p.c, p.i, p.t)
sd.hat    # STANDARD ERROR ESTIMATES (p.c, p.i, p.t)
cor.hat   # CORRELATION ESTIMATES ({p.c,p.i}, {p.c,p.t}, {p.i,p.t})


#########################################################################
### EXAMPLE 4.9 EM GRADIENT ALGORITHM (PEPPERED MOTHS)
#########################################################################

#########################################################################
# x = observed phenotype counts (carbonaria, insularia, typica)
# n = expected genotype frequencies (CC, CI, CT, II, IT, TT)
# p = allele probabilities (carbonaria, insularia, typica)
# itr = number of iterations
# prob.values = allele probabilities (used for plotting)
# alpha.default = default scaling parameter
# allele.e = computes expected genotype frequencies
# allele.l = computes log likelihood
# Q.prime = computes the gradient of Q
# Q.2prime = computes the hessian of Q
#########################################################################

## INITIAL VALUES
x = c(85, 196, 341)
n = rep(0,6)
p = rep(1/3,3)
itr = 40
prob.values = matrix(0,3,itr+1)
prob.values[,1] = p
alpha.default = 2

## FUNCTIONS
allele.e = function(x,p){
    n.cc = (x[1]*(p[1]^2))/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ci = (2*x[1]*p[1]*p[2])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ct = (2*x[1]*p[1]*p[3])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ii = (x[2]*(p[2]^2))/((p[2]^2)+2*p[2]*p[3])
    n.it = (2*x[2]*p[2]*p[3])/((p[2]^2)+2*p[2]*p[3])
    n = c(n.cc,n.ci,n.ct,n.ii,n.it,x[3])
    return(n)
}

allele.l = function(x,p){
    l = ( x[1]*log(2*p[1] - p[1]^2) + x[2]*log(p[2]^2 + 2*p[2]*p[3]) +
          2*x[3]*log(p[3]) )
    return(l)
}

Q.prime = function(n,p){
    da = (2*n[1]+n[2]+n[3])/(p[1]) - (2*n[6]+n[3]+n[5])/(p[3])
    db = (2*n[4]+n[5]+n[2])/(p[2]) - (2*n[6]+n[3]+n[5])/(p[3])
    dQ = c(da,db)
    return(dQ)
}

Q.2prime = function(n,p){
    da2 = -(2*n[1]+n[2]+n[3])/(p[1]^2) - (2*n[6]+n[3]+n[5])/(p[3]^2)
    51
    db2 = -(2*n[4]+n[5]+n[2])/(p[2]^2) - (2*n[6]+n[3]+n[5])/(p[3]^2)
    dab = -(2*n[6]+n[3]+n[5])/(p[3]^2)
    d2Q = matrix(c(da2,dab,dab,db2), nrow=2, byrow=TRUE)
    return(d2Q)
}

## MAIN
l.old = allele.l(x,p)
for(i in 1:itr){
    alpha = alpha.default
    n = allele.e(x,p)
    p.new = p[1:2] - alpha*solve(Q.2prime(n,p))%*%Q.prime(n,p)
    p.new[3] = 1 - p.new[1] - p.new[2]
    if(p.new > 0 && p.new < 1){l.new = allele.l(x,p.new)}
        # REDUCE ALPHA UNTIL A CORRECT STEP IS REACHED
        while(p.new < 0 || p.new > 1 || l.new < l.old){
        alpha = alpha/2
        p.new = p[1:2] - alpha*solve(Q.2prime(n,p))%*%Q.prime(n,p)
        p.new[3] = 1 - p.new[1] - p.new[2]
        if(p.new > 0 && p.new < 1){l.new = allele.l(x,p.new)}
    }
    p = p.new
    prob.values[,i+1] = p
    l.old = l.new
}

## OUTPUT
p     # FINAL ESTIMATE FOR ALLELE PROBABILITIES (p.c, p.i, p.t)

## PLOT OF CONVERGENCE
pb = seq(0.001,0.4,length=100)
c = outer(pb,pb,function(a,b){1-a-b})
pbs = matrix(0,3,10000)
pbs[1,] = rep(pb,100)
pbs[2,] = rep(pb,each=100)
pbs[3,] = as.vector(c)
z = matrix(apply(pbs,2,allele.l,x=x),100,100)
contour(pb,pb,z,nlevels=20)
for(i in 1:itr){
    segments(prob.values[1,i],prob.values[2,i],prob.values[1,i+1],
    prob.values[2,i+1],lty=2)
}


#########################################################################
### EXAMPLE 4.10 AITKEN ACCELERATION (PEPPERED MOTHS)
#########################################################################

#########################################################################
# x = observed phenotype counts (carbonaria, insularia, typica)
# n = expected genotype frequencies (CC, CI, CT, II, IT, TT)
# p = allele probabilities (carbonaria, insularia, typica)
# itr = number of iterations
# prob.values = allele probabilities (used for plotting)
# alpha.default = default scaling parameter
# allele.e = computes expected genotype frequencies
# allele.m = computes allele probabilities
# allele.l = computes log likelihood
# allele.iy = computes the complete information
# allele.l.2prime = computes the hessian of the log likelihood
#########################################################################

## INITIAL VALUES
x = c(85, 196, 341)
n = rep(0,6)
p = rep(1/3,3)
itr = 40
prob.values = matrix(0,3,itr+1)
prob.values[,1] = p
alpha.default = 2

## FUNCTIONS
allele.e = function(x,p){
    n.cc = (x[1]*(p[1]^2))/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ci = (2*x[1]*p[1]*p[2])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ct = (2*x[1]*p[1]*p[3])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ii = (x[2]*(p[2]^2))/((p[2]^2)+2*p[2]*p[3])
    n.it = (2*x[2]*p[2]*p[3])/((p[2]^2)+2*p[2]*p[3])
    n = c(n.cc,n.ci,n.ct,n.ii,n.it,x[3])
    return(n)
}

allele.m = function(x,n){
    p.c = (2*n[1]+n[2]+n[3])/(2*sum(x))
    p.i = (2*n[4]+n[5]+n[2])/(2*sum(x))
    p.t = (2*n[6]+n[3]+n[5])/(2*sum(x))
    p = c(p.c,p.i,p.t)
    return(p)
}

allele.l = function(x,p){
    l = ( x[1]*log(2*p[1] - p[1]^2) + x[2]*log(p[2]^2 + 2*p[2]*p[3]) +
      2*x[3]*log(p[3]) )
    return(l)
}

allele.iy = function(n,p){
    iy.hat=matrix(0,2,2)
    iy.hat[1,1] = ((2*n[1]+n[2]+n[3])/(p[1]^2) +
       (2*n[6]+n[3]+n[5])/(p[3]^2))
    iy.hat[2,2] = ((2*n[4]+n[5]+n[2])/(p[2]^2) +
       (2*n[6]+n[3]+n[5])/(p[3]^2))
    iy.hat[1,2] = iy.hat[2,1] = (2*n[6]+n[3]+n[5])/(p[3]^2)
    return(iy.hat)
}

allele.l.2prime = function(x,p){
    l.2prime = matrix(0,2,2)
    l.2prime[1,1] = ( (-x[1]*(2-2*p[1])^2)/((2*p[1]-p[1]^2)^2) -
      2*x[1]/(2*p[1]-p[1]^2) -
      (4*x[2])/((-2*p[1]-p[2]+2)^2) -
      2*x[3]/(p[3]^2))
    l.2prime[2,2] = ( (-4*x[2]*p[3]^2)/((p[2]^2 + 2*p[2]*p[3])^2) -
      2*x[2]/(p[2]^2 + 2*p[2]*p[3]) -
      2*x[3]/(p[3]^2))
    l.2prime[1,2] = ((-2*x[2])/((-2*p[1]-p[2]+2)^2) -
      2*x[3]/(p[3]^2))
    l.2prime[2,1] = l.2prime[1,2]
    return(l.2prime)
}

## MAIN
l.old = allele.l(x,p)
for(i in 1:itr){
    alpha = alpha.default
    n = allele.e(x,p)
    p.em = allele.m(x,n)
    p.new = (p[1:2] - alpha*solve(allele.l.2prime(x,p))%*%
      allele.iy(n,p)%*%(p.em[1:2]-p[1:2]))
    p.new[3] = 1 - p.new[1] - p.new[2]
    if(p.new > 0 && p.new < 1){l.new = allele.l(x,p.new)}
      # REDUCE ALPHA UNTIL A CORRECT STEP IS REACHED
    while(p.new < 0 || p.new > 1 || l.new < l.old){
        alpha = alpha/2
        p.new = (p[1:2] - alpha*solve(allele.l.2prime(x,p))%*%
         allele.iy(n,p)%*%(p.em[1:2]-p[1:2]))
        p.new[3] = 1 - p.new[1] - p.new[2]
        if(p.new > 0 && p.new < 1){l.new = allele.l(x,p.new)}
    }
    p = p.new
    prob.values[,i+1] = p
    l.old = l.new
}

## OUTPUT
p    # FINAL ESTIMATE FOR ALLELE PROBABILITIES (p.c, p.i, p.t)

## PLOT OF CONVERGENCE
pb = seq(0.001,0.4,length=100)
c = outer(pb,pb,function(a,b){1-a-b})
pbs = matrix(0,3,10000)
pbs[1,] = rep(pb,100)
pbs[2,] = rep(pb,each=100)
pbs[3,] = as.vector(c)
z = matrix(apply(pbs,2,allele.l,x=x),100,100)
contour(pb,pb,z,nlevels=20)
for(i in 1:itr){
    segments(prob.values[1,i],prob.values[2,i],prob.values[1,i+1],
      prob.values[2,i+1],lty=2)
}


#########################################################################
### EXAMPLE 4.11 QUASI-NEWTON ACCELERATION (PEPPERED MOTHS)
#########################################################################

#########################################################################
# x = observed phenotype counts (carbonaria, insularia, typica)
# n = expected genotype frequencies (CC, CI, CT, II, IT, TT)
# p = allele probabilities (carbonaria, insularia, typica)
# itr = number of iterations
# m = approximation of the hessian of the log likelihood
# b = update information for m
# prob.values = allele probabilities (used for plotting)
# alpha.default = default scaling parameter
# allele.e = computes expected genotype frequencies
# allele.l = computes log likelihood
# Q.prime = computes the gradient of Q
# Q.2prime = computes the hessian of Q
#########################################################################

## INITIAL VALUES
x = c(85, 196, 341)
n = rep(0,6)
p = rep(1/3,3)
itr = 20
m = matrix(0,2,2)
b = matrix(0,2,2)
prob.values = matrix(0,3,itr+1)
prob.values[,1] = p
alpha.default = 2

## FUNCTIONS
allele.e = function(x,p){
    n.cc = (x[1]*(p[1]^2))/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ci = (2*x[1]*p[1]*p[2])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ct = (2*x[1]*p[1]*p[3])/((p[1]^2)+2*p[1]*p[2]+2*p[1]*p[3])
    n.ii = (x[2]*(p[2]^2))/((p[2]^2)+2*p[2]*p[3])
    n.it = (2*x[2]*p[2]*p[3])/((p[2]^2)+2*p[2]*p[3])
    n = c(n.cc,n.ci,n.ct,n.ii,n.it,x[3])
    return(n)
}

allele.l = function(x,p){
    l = ( x[1]*log(2*p[1] - p[1]^2) + x[2]*log(p[2]^2 + 2*p[2]*p[3]) +
          2*x[3]*log(p[3]) )
    return(l)
}

Q.prime = function(n,p){
    da = (2*n[1]+n[2]+n[3])/(p[1]) - (2*n[6]+n[3]+n[5])/(p[3])
    db = (2*n[4]+n[5]+n[2])/(p[2]) - (2*n[6]+n[3]+n[5])/(p[3])
    dQ = c(da,db)
    return(dQ)
}

Q.2prime = function(n,p){
    da2 = -(2*n[1]+n[2]+n[3])/(p[1]^2) - (2*n[6]+n[3]+n[5])/(p[3]^2)
    db2 = -(2*n[4]+n[5]+n[2])/(p[2]^2) - (2*n[6]+n[3]+n[5])/(p[3]^2)
    dab = -(2*n[6]+n[3]+n[5])/(p[3]^2)
    d2Q = matrix(c(da2,dab,dab,db2), nrow=2, byrow=TRUE)
    return(d2Q)
}

## MAIN
l.old = allele.l(x,p)
for(i in 1:itr){
    alpha = alpha.default
    n = allele.e(x,p)
    m = Q.2prime(n,p) - b
    p.new = p[1:2] - alpha*solve(m)%*%Q.prime(n,p)
    p.new[3] = 1 - p.new[1] - p.new[2]
    if(p.new > 0 && p.new < 1){l.new = allele.l(x,p.new)}
      # REDUCE ALPHA UNTIL A CORRECT STEP IS REACHED
    while(p.new < 0 || p.new > 1 || l.new < l.old){
        alpha = alpha/2
        p.new = p[1:2] - alpha*solve(m)%*%Q.prime(n,p)
        p.new[3] = 1 - p.new[1] - p.new[2]
        if(p.new > 0 && p.new < 1){l.new = allele.l(x,p.new)}
    }
    at = p.new[1:2]-p[1:2]
    n = allele.e(x,p.new)
    bt = Q.prime(n,p)-Q.prime(n,p.new)
    vt = bt - b%*%at
    ct = as.numeric(1/(t(vt)%*%at))
    b = b + ct*vt%*%t(vt)
    p = p.new
    prob.values[,i+1] = p
    l.old = l.new
}

## OUTPUT
p   # FINAL ESTIMATE FOR ALLELE PROBABILITIES (p.c, p.i, p.t)

## PLOT OF CONVERGENCE
pb = seq(0.001,0.4,length=100)
c = outer(pb,pb,function(a,b){1-a-b})
pbs = matrix(0,3,10000)
pbs[1,] = rep(pb,100)
pbs[2,] = rep(pb,each=100)
pbs[3,] = as.vector(c)
z = matrix(apply(pbs,2,allele.l,x=x),100,100)
contour(pb,pb,z,nlevels=20)
for(i in 1:itr){
    segments(prob.values[1,i],prob.values[2,i],prob.values[1,i+1],
      prob.values[2,i+1],lty=2)
}


#########################################################################
### END OF FILE
