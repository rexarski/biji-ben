############################################################################
# COMPUTATIONAL STATISTICS
# by Geof H. Givens and J. A. Hoeting
# CHAPTER 2 EXAMPLES (Last update: 10/1/2012)
#########################################################################

#########################################################################
### EXAMPLE 2.1 BISECTION
#########################################################################
# a = initial left endpoint
# b = initial right endpoint
# x = initial value
# itr = number of iterations to run
# g = objective function
# g.prime = first derivative of objective function
#########################################################################

## INITIAL VALUES
a = 1
b = 5
x = a+(b-a)/2
itr = 40

## FUNCTIONS
g = function(x){log(x)/(1+x)}
g.prime = function(x){(1+(1/x)-log(x))/((1+x)^2)}

## MAIN
for (i in 1:itr){
    if (g.prime(a)*g.prime(x) < 0) {b = x}
    else {a = x}
    x = a+(b-a)/2
}

## OUTPUT
x		# FINAL ESTIMATE
g(x)		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x) 	# GRADIENT AT ESTIMATE


#########################################################################
### EXAMPLE 2.2 NEWTON'S METHOD
#########################################################################

#########################################################################
# x = initial value
# itr = number of iterations to run
# g = objective function
# g.prime = first derivative of objective function
# g.2prime = second derivative of objective function
#########################################################################

## INITIAL VALUES
x = 3
itr = 40

## FUNCTIONS
g = function(x){log(x)/(1+x)}
g.prime = function(x){(1+(1/x)-log(x))/((1+x)^2)}
g.2prime = function(x){(-1/((x^2)+(x^3)))-2*(1+(1/x)-log(x))/((1+x)^3)}

## MAIN
for(i in 1:itr){x = x - g.prime(x)/g.2prime(x)}

## OUTPUT
x		# FINAL ESTIMATE
g(x)		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x)	# GRADIENT AT ESTIMATE


#########################################################################
### EXAMPLE 2.3 SCALED FIXED POINT ALGORITHM
#########################################################################

#########################################################################
# alpha = scale parameter
# x = initial value
# itr = number of iterations to run
# g = objective function
# g.prime = first derivative of objective function
# g.2prime = second derivative of objective function
#########################################################################

## INITIAL VALUES
alpha = 4
x = 1.75
itr = 100

## OBJECTIVE FUNCTION AND DERIVATIVE
g = function(x){log(x)/(1+x)}
g.prime = function(x){(1+(1/x)-log(x))/((1+x)^2)}

## MAIN
for(i in 1:itr){x = alpha*g.prime(x) + x}

## OUTPUT
x		# FINAL ESTIMATE
g(x) 		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x) 	# GRADIENT AT ESTIMATE


#########################################################################
### EXAMPLE 2.4 NEWTON'S METHOD (BIVARIATE)
#########################################################################

#########################################################################
# x = initial value
# itr = number of iterations to run
# x.values = contains values of x for each iteration
# g = objective function
# g.prime = first derivative of objective function
# g.2prime = second derivative of objective function
#########################################################################

## NOTES
# The objective function in the following example is the negative of
# Himmelblau's function.  This is different than the example
# in the book
#########################################################################

## INITIAL VALUES
x = c(-2,-2)
itr = 40
x.values = matrix(0,itr+1,2)
x.values[1,] = x

## OBJECTIVE FUNCTION AND DERIVATIVES
g = function(x){(-1)*((((x[1]^2)+x[2]-11)^2)+(x[1]+(x[2]^2)-7)^2)}

g.prime = function(x){
	g.prime.da = (-1)*((4*x[1]^3)+(4*x[1]*x[2])-(42*x[1])+(2*x[2]^2)-14)
	g.prime.db = (-1)*((2*x[1]^2)-(26*x[2])-22+(4*x[1]*x[2])+(4*x[2]^3))
	out = matrix(c(g.prime.da,g.prime.db),ncol=1)
	return(out)
}
g.2prime=function(x){
	g.2prime.da2 = (-1)*((12*x[1]^2)+(4*x[2])-42)
	g.2prime.db2 = (-1)*((12*x[2]^2)+(4*x[1])-26)
	g.2prime.dadb = (-1)*(4*(x[1]+x[2]))
	out = matrix(c(g.2prime.da2,g.2prime.dadb,
        	g.2prime.dadb,g.2prime.db2),nrow=2, byrow=TRUE)
	return(out)
}

## MAIN
for(i in 1:itr){
      x = x - solve(g.2prime(x))%*%g.prime(x)
      x.values[i+1,] = x
}

## OUTPUT
x		# FINAL ESTIMATE
g(x) 		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x) 	# GRADIENT AT ESTIMATE

## PLOT OF CONVERGENCE
z = matrix(0,100,100)
x1.max = max(4.5,ceiling(max(x.values[,1])))
x1.min = min(-2,floor(min(x.values[,1])))
x2.max = max(3,ceiling(max(x.values[,2])))
x2.min = min(-2,floor(min(x.values[,2])))
x1 = seq(x1.min,x1.max,length=100)
x2 = seq(x2.min,x2.max,length=100)
for(i in 1:100){
      for(j in 1:100){
      	    z[i,j] = g(c(x1[i],x2[j]))
      }
}
contour(x1,x2,z,nlevels=20,drawlabels=FALSE)
for(i in 1:itr){
      segments(x.values[i,1],x.values[i,2],x.values[i+1,1],
      x.values[i+1,2],lty=2)
}


#########################################################################
### EXAMPLE 2.5 HUMAN FACE RECOGNITION (IRLS)
#########################################################################

#########################################################################
###  Note: the dataset provided here differs slightly from the data used
###  in the book: it omits 30 cases.  Thus, the answer here is
###  slightly different
#
# face.dat = observed data
# n = number of observations
# itr = number of iterations to run
# y = observed response data (1=correct match)
# z = covariate matrix
# w = weights
# beta.val = beta estimates at each iteration
# pi.val = pi estimates at each iteration
#########################################################################

## INITIAL VALUES
  #THE INPUT FILE IS: FACE-RECOGNITION.DAT
face.dat = read.table(file.choose(),header=TRUE,sep=" ")
n = nrow(face.dat)
itr = 40
y = face.dat$match
z = cbind(rep(1,n),face.dat$eyediff)
w = rep(0,n)
beta.val = matrix(0,itr+1,2)
pi.val = rep(0,n)
beta.val[1,1]=.9591309

## MAIN
for(j in 1:itr){
      pi.val = 1/(1+exp(-1*z%*%beta.val[j,]))
      w = pi.val*(1-pi.val)
      hessian = matrix(0,2,2)
      hessian[1,1] = -sum(w)
      hessian[1,2] = hessian[2,1] = -t(w)%*%z[,2]
      hessian[2,2] = -t(w)%*%(z[,2]^2)
      hessian.inv = solve(hessian)
      score = t(z)%*%(y-pi.val)
      betas = beta.val[j,]-hessian.inv%*%score
      beta.val[j+1,] = betas
}

## OUTPUT
betas #FINAL ESTIMATE


#########################################################################
### EXAMPLE 2.6 STEEPEST ASCENT
#########################################################################

#########################################################################
# x = initial value
# M = Hessian approximation
# itr = number of iterations to run
# alpha = scale parameter
# x.values = contains values of x for each iteration
# g = objective function
# g.prime = first derivative of objective function
#########################################################################
## NOTES
# The objective function in the following example is the negative of
# Himmelblau's function.  This is different than the function
# used in the book
#########################################################################

## INITIAL VALUES
x = c(0,0)
M = diag(-1,2,2)
itr = 40
alpha.default = 1
alpha = alpha.default
x.values = matrix(0,itr+1,2)
x.values[1,] = x

## OBJECTIVE FUNCTION AND DERIVATIVES
g = function(x){(-1)*((((x[1]^2)+x[2]-11)^2)+(x[1]+(x[2]^2)-7)^2)}
g.prime = function(x){
	g.prime.da = (-1)*((4*x[1]^3)+(4*x[1]*x[2])-(42*x[1])+(2*x[2]^2)-14)
	g.prime.db = (-1)*((2*x[1]^2)-(26*x[2])-22+(4*x[1]*x[2])+(4*x[2]^3))
	out = matrix(c(g.prime.da,g.prime.db),ncol=1)
	return(out)
}

## MAIN
for (i in 1:itr){
    hessian.inv = solve(M)
    xt = x - alpha*hessian.inv%*%g.prime(x)
    # REDUCE ALPHA UNTIL A CORRECT STEP IS REACHED
    while(g(xt) < g(x)){
    		alpha = alpha/2
		xt = x - alpha*hessian.inv%*%g.prime(x)
    }
    x.values[i+1,] = x = xt
    alpha = alpha.default
}

## OUTPUT
x		# FINAL ESTIMATE
g(x) 		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x) 	# GRADIENT AT ESTIMATE

## PLOT OF CONVERGENCE
z = matrix(0,100,100)
x1.max = max(4.5,ceiling(max(x.values[,1])))
x1.min = min(-2,floor(min(x.values[,1])))
x2.max = max(3,ceiling(max(x.values[,2])))
x2.min = min(-2,floor(min(x.values[,2])))
x1 = seq(x1.min,x1.max,length=100)
x2 = seq(x2.min,x2.max,length=100)
for(i in 1:100){
for(j in 1:100){
      z[i,j] = g(c(x1[i],x2[j]))
      }
}
contour(x1,x2,z,nlevels=20,drawlabels=FALSE)
for(i in 1:itr){
      segments(x.values[i,1],x.values[i,2],x.values[i+1,1],
      x.values[i+1,2],lty=2)
}


#########################################################################
### EXAMPLE 2.7 QUASI-NEWTON METHOD (BFGS UPDATE AND BACKTRACKING)
#########################################################################

#########################################################################
# x = initial value
# M = Hessian approximation
# itr = number of iterations to run
# x.values = contains values of x for each iteration
# alpha = scale parameter
# epsilon = tolerance
# g = objective function
# g.prime = first derivative of objective function
#########################################################################

#########################################################################
## NOTES
# The objective function in the following example is the negative of
# Himmelblau's function.  This is different than the book
#########################################################################

## INITIAL VALUES
x = c(-4,0)
M = diag(-1,2,2)
itr = 40
epsilon = 1e-10
x.values = matrix(0,itr+1,2)
x.values[1,] = x
alpha.default = 1
alpha = alpha.default

## FUNCTIONS
g = function(x){(-1)*((((x[1]^2)+x[2]-11)^2)+(x[1]+(x[2]^2)-7)^2)}
g.prime = function(x){
	g.prime.da = (-1)*((4*x[1]^3)+(4*x[1]*x[2])-(42*x[1])+(2*x[2]^2)-14)
	g.prime.db = (-1)*((2*x[1]^2)-(26*x[2])-22+(4*x[1]*x[2])+(4*x[2]^3))
	out = matrix(c(g.prime.da,g.prime.db),ncol=1)
	return(out)
}

## MAIN
for(i in 1:itr){
      hessian.inv = solve(M)
      xt = x - alpha*hessian.inv%*%g.prime(x)
      # REDUCE ALPHA UNTIL A CORRECT STEP IS REACHED
      while(g(xt) < g(x)){
      		  alpha = alpha/2
		  xt = x - alpha*hessian.inv%*%g.prime(x)
      }
      x.values[i+1,] = xt
      z = xt-x
      y = g.prime(xt)-g.prime(x)
      v = y-M%*%z
      M.old = M
      M = M-((M%*%z%*%t(M%*%z))/((t(z)%*%M%*%z)[1]))+
           ((y%*%t(y))/((t(z)%*%y)[1]))
      if(abs((t(v)%*%z)[1]) < epsilon){M = M.old}
      alpha = alpha.default
      x = xt
}

## OUTPUT
x		# FINAL ESTIMATE
g(x) 		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x) 	# GRADIENT AT ESTIMATE

## PLOT OF CONVERGENCE
z = matrix(0,100,100)
x1.max = max(4.5,ceiling(max(x.values[,1])))
x1.min = min(-2,floor(min(x.values[,1])))
x2.max = max(3,ceiling(max(x.values[,2])))
x2.min = min(-2,floor(min(x.values[,2])))
x1 = seq(x1.min,x1.max,length=100)
x2 = seq(x2.min,x2.max,length=100)
for(i in 1:100){
      for(j in 1:100){
      	    z[i,j] = g(c(x1[i],x2[j]))
      }
}
contour(x1,x2,z,nlevels=20,drawlabels=FALSE)
for(i in 1:itr){
      segments(x.values[i,1],x.values[i,2],x.values[i+1,1],
      x.values[i+1,2],lty=2)
}


#########################################################################
### EXAMPLE 2.8 - 2.9 NELDER-MEAD
#########################################################################

#########################################################################
## NOTE
#  These examples are meant to illustrate concepts rather than a
#  detailed implementation.
#  The Nelder-Mead algorithm is the default method used
#  in the R function optim()
#########################################################################


#########################################################################
### EXAMPLE 2.10 GAUSS-SEIDEL (NEWTON)
#########################################################################

#########################################################################
# x = initial value
# itr = number of iterations to run
# x.values = contains values of x for each iteration
# alpha = scale parameter
# g = objective function
# g.prime = first derivative of objective function
# g.2prime = second derivative of objective function
#########################################################################

#########################################################################
## NOTES
# The objective function in the following example is the negative of
# Himmelblau's function.  This is different than in the book.  Also,
# the results of the example here are very sensitive to starting value.
#########################################################################

## INITIAL VALUES
x = c(-1.5,1.5)
itr = 40
x.values = matrix(0,itr+1,2)
x.values[1,] = x

## OBJECTIVE FUNCTION AND DERIVATIVES
g = function(x){(-1)*((((x[1]^2)+x[2]-11)^2)+(x[1]+(x[2]^2)-7)^2)}
g.prime = function(x){
	g.prime.da = (-1)*((4*x[1]^3)+(4*x[1]*x[2])-(42*x[1])+(2*x[2]^2)-14)
	g.prime.db = (-1)*((2*x[1]^2)-(26*x[2])-22+(4*x[1]*x[2])+(4*x[2]^3))
	out = matrix(c(g.prime.da,g.prime.db),ncol=1)
	return(out)
}
g.2prime = function(x){
	 g.2prime.da2 = (-1)*((12*x[1]^2)+(4*x[2])-42)
	 g.2prime.db2 = (-1)*((12*x[2]^2)+(4*x[1])-26)
	 g.2prime.dadb = (-1)*(4*(x[1]+x[2]))
	 out = matrix(c(g.2prime.da2,g.2prime.dadb,
	 g.2prime.dadb,g.2prime.db2),nrow=2, byrow=TRUE)
	 return(out)
}

## MAIN
for (j in 1:itr){
    for (i in 1:itr){
    	xt = x[1]-((g.prime(x)[1])/(g.2prime(x)[1,1]))
	x.values[j+1,1] = xt
	x[1] = xt
    }
    for (i in 1:itr){
    	xt = x[2]-((g.prime(x)[2])/(g.2prime(x)[2,2]))
	x.values[j+1,2] = xt
	x[2] = xt
    }
}

## OUTPUT
x		# FINAL ESTIMATE
g(x) 		# OBJECTIVE FUNCTION AT ESTIMATE
g.prime(x)	# GRADIENT AT ESTIMATE

## PLOT OF CONVERGENCE
z = matrix(0,100,100)
x1.max = max(4.5,ceiling(max(x.values[,1])))
x1.min = min(-2,floor(min(x.values[,1])))
x2.max = max(3,ceiling(max(x.values[,2])))
x2.min = min(-2,floor(min(x.values[,2])))
x1 = seq(x1.min,x1.max,length=100)
x2 = seq(x2.min,x2.max,length=100)
for(i in 1:100){
      for(j in 1:100){
      	    z[i,j] = g(c(x1[i],x2[j]))
      }
}
contour(x1,x2,z,nlevels=20,drawlabels=FALSE)
for(i in 1:itr){
      segments(x.values[i,1],x.values[i,2],x.values[i+1,1],
      x.values[i,2],lty=2)
      segments(x.values[i+1,1],x.values[i,2],x.values[i+1,1],
      x.values[i+1,2],lty=2)
}


#########################################################################
### END OF FILE
