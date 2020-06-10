############################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 5 EXAMPLES (last update 10/1/2012)

############################################################################
### EXAMPLE 5.1 ALZHEIMER'S DISEASE 
############################################################################
# y        = observed data
# b.0      = initial beta estimates
# s2.0     = initial variance estimate
# interval = vector of length 2 containing (min,max)
# n        = number of subintervals
# f        = target function
# riemann  = computes Riemann's rule for (n) subintervals
############################################################################

## INITIAL VALUES
y    = read.table(file.choose(),header=T)
options(digits=15)
b.0  = c(1.804,0.165)
s2.0 = 0.015^2
interval = c(-.07,.085)
n    = 256

## FUNCTIONS
f = function(g,s2,b,id){
      x      = matrix(c(rep(1,5),1:5),5,2)
      lambda = exp(x%*%b+rep(g,5))
      y.sub  = y[y$subject==id,3]
      out    = (dnorm(g,mean=0,sd=sqrt(s2))*((1:5)%*%(y.sub-lambda))*
                prod(dpois(y.sub,lambda)))
      return(out)
}
f = Vectorize(f,vectorize.args = "g")

riemann = function(interval,n,s2,b,id){
      h   = (interval[2]-interval[1])/n
      x   = interval[1] + (0:(n-1))*h
      out = h*f(x,s2,b,id)
      return(out)
}

# MAIN
R1 = riemann(interval,n,s2.0,b.0,1)

# OUTPUT
sum(R1)      # RIEMANN APPROXIMATION

# OUTPUT PLOT
x = seq(interval[1],interval[2],length.out=1000)
d = f(x,s2.0,b.0,1)
plot(x,d,type="l",xlab=expression(gamma))


############################################################################
### EXAMPLE 5.2 ALZHEIMER'S DISEASE (TRAPEZOIDAL RULE)
############################################################################
# y           = observed data
# b.0         = initial beta estimates
# s2.0        = initial variance estimate
# interval    = vector of length 2 containing (min,max)
# n           = number of subintervals
# f           = target function
# trapezoidal = computes trapezoidal rule for (n) subintervals
############################################################################
# INITIAL VALUES
y    = read.table(file.choose(),header=T)
options(digits=15)
b.0  = c(1.804,0.165)
s2.0 = 0.015^2
interval = c(-.07,.085)
n    = 256

## FUNCTIONS
f = function(g,s2,b,id){
      x      = matrix(c(rep(1,5),1:5),5,2)
      lambda = exp(x%*%b+rep(g,5))
      y.sub  = y[y$subject==id,3]
      out    = (dnorm(g,mean=0,sd=sqrt(s2))*((1:5)%*%(y.sub-lambda))*
                prod(dpois(y.sub,lambda)))
      return(out)
}
f = Vectorize(f,vectorize.args = "g")

trapezoidal = function(interval,n,s2,b,id){
      h   = (interval[2]-interval[1])/n
      x   = interval[1] + (1:(n-1))*h
      out = h/2*f(interval[1],s2,b,id)
      out = c(out, h*f(x,s2,b,id))
      out = c(out, h/2*f(interval[2],s2,b,id))
      return(out)
}


# MAIN
T1 = trapezoidal(interval,n,s2.0,b.0,1)

# OUTPUT
sum(T1)      # TRAPEZOIDAL APPROXIMATION



############################################################################
### EXAMPLE 5.3 ALZHEIMER'S DISEASE (SIMPSON'S RULE)
############################################################################
# y        = observed data
# b.0      = initial beta estimates
# s2.0     = initial variance estimate
# interval = vector of length 2 containing (min,max)
# n        = number of subintervals
# f        = target function
# simpsons = computes simpson's rule for (n) subintervals
############################################################################
# INITIAL VALUES
y    = read.table(file.choose(),header=T)
options(digits=15)
b.0  = c(1.804,0.165)
s2.0 = 0.015^2
interval = c(-.07,.085)
n    = 256

## FUNCTIONS
f = function(g,s2,b,id){
      x      = matrix(c(rep(1,5),1:5),5,2)
      lambda = exp(x%*%b+rep(g,5))
      y.sub  = y[y$subject==id,3]
      out    = (dnorm(g,mean=0,sd=sqrt(s2))*((1:5)%*%(y.sub-lambda))*
                prod(dpois(y.sub,lambda)))
      return(out)
}
f = Vectorize(f,vectorize.args = "g")

simpsons = function(interval,n,s2,b,id){
      h   = (interval[2]-interval[1])/n
      x   = interval[1] + (0:n)*h
      out = NULL
      for(i in 1:(n/2)){
            out[i] = h/3*f(x[2*i - 1],s2,b,id)
            out[i] = out[i] + 4*h/3*f(x[2*i],s2,b,id)
            out[i] = out[i] + h/3*f(x[2*i + 1],s2,b,id)
      }
      return(out)
}


# MAIN
S1 = simpsons(interval,2*n,s2.0,b.0,1)

# OUTPUT
sum(S1)      # SIMPSON'S APPROXIMATION


############################################################################
### EXAMPLE 5.4 ALZHEIMER'S DISEASE (ROMBERG INTEGRATION)
############################################################################
# y           = observed data
# b.0         = initial beta estimates
# s2.0        = initial variance estimate
# interval    = vector of length 2 containing (min,max)
# n           = number of subintervals
# f           = target function
# trapezoidal = computes trapezoidal rule for (n) subintervals
# romberg     = computes Romberg integration to (m) for (n) subintervals
############################################################################
# INITIAL VALUES
y    = read.table(file.choose(),header=T)
options(digits=15)
b.0  = c(1.804,0.165)
s2.0 = 0.015^2
interval = c(-.07,.085)
n    = 256
m    = 10

## FUNCTIONS
f = function(g,s2,b,id){
      x      = matrix(c(rep(1,5),1:5),5,2)
      lambda = exp(x%*%b+rep(g,5))
      y.sub  = y[y$subject==id,3]
      out    = (dnorm(g,mean=0,sd=sqrt(s2))*((1:5)%*%(y.sub-lambda))*
                prod(dpois(y.sub,lambda)))
      return(out)
}
f = Vectorize(f,vectorize.args = "g")

trapezoidal = function(interval,n,s2,b,id){
      h   = (interval[2]-interval[1])/n
      x   = interval[1] + (1:(n-1))*h
      out = h/2*f(interval[1],s2,b,id)
      out = c(out, h*f(x,s2,b,id))
      out = c(out, h/2*f(interval[2],s2,b,id))
      return(out)
}

romberg = function(interval,m,s2,b,id){
      out = matrix(0,m+1,m+1)
      out[1,1] = sum(diff(interval)/2*f(interval,s2,b,id))
      for(i in 2:(m+1)){
       out[i,1] = sum(trapezoidal(interval,2^(i-1),s2,b,id))
        for(j in 2:i){
         out[i,j] = out[i,j-1] + (out[i,j-1]-out[i-1,j-1])/((4^(j-1))-1)
        }
      }
      diag(out) = 0
      out = out[-1,]
      return(out)
}


# MAIN
T.hat = romberg(interval,m,s2.0,b.0,1)

# OUTPUT
T.hat[,1:3]      # ROMBERG INTEGRATION ESTIMATES


############################################################################
### EXAMPLE 5.5 ALZHEIMER'S DISEASE (GAUSSIAN QUADRATURE)
############################################################################

#For the second edition, we prefer to direct our readers to
#code available online for Gaussian quadrature.  For example,
#the functions gauss.quad.prob() and gauss.quad() calculate
#the nodes and weights.  These functions are available within
#the R package {statmod} found via www.r-project.org

############################################################################
### END OF FILE
