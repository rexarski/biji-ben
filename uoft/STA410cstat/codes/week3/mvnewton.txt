# FUNCTION TO FIND A ZERO OF A MULTIVARIATE FUNCTION USING NEWTON'S METHOD.
#
# R. M. Neal, September 2014
#
# Arguments:
#    f = function we want to find a zero of (vector argument, vector value)
#    g = function computing derivative of f (vector argument, matrix value)
#    x = initial guess at location of zero (vector)
#    n = number of iterations
#
# Returned value:  
#    point, x, at which f(x) is approximately zero

mvnewton <- function (f, g, x, n)
{
    if (n < 1)
        stop("invalid number of iterations")

    for (i in 1:n) {
        cat("\nAt iteration",i,":\n\n")
        cat("x =",x,"\n")
        cat("f(x) =",f(x),"\n")
        cat("g(x) =\n")
        print(g(x));
        x <- x - solve(g(x),f(x))  # computes inverse of g(x) times f(x)
    }
  
    x
}

# Function to test mvnewton.

mvnewton_test <- function (initial_x, niters) {

    f <- function (x) 
           c (sin(x[1]) + 0.3*x[2] + 0.7, 0.4*x[2]^3 + (1+x[1])*x[2] + 0.2)
    g <- function (x) 
           matrix (c (cos(x[1]), x[2], 0.3, 3*0.4*x[2]^2 + 1 + x[1]), 2, 2)

    grid <- seq(-2,2,by=0.02)
    fx1 <- matrix(nrow=length(grid),ncol=length(grid))
    fx2 <- matrix(nrow=length(grid),ncol=length(grid))
    for (i in 1:length(grid)) {
        for (j in 1:length(grid)) {
            fx <- f(c(grid[i],grid[j]))
            fx1[i,j] <- fx[1]
            fx2[i,j] <- fx[2]
        }
    }
    contour(grid,grid,fx1,col="red")
    contour(grid,grid,fx2,add=TRUE,col="blue")
    points(initial_x[1],initial_x[2],pch="+")

    x <- mvnewton(f,g,initial_x,niters)

    points(x[1],x[2])
}
