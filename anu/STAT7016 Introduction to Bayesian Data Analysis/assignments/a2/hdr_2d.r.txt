##########
plot.hdr2d<-function(x,prob=c(.025,.25,.5,.75,.975),bw=c(5,5),
       cols=gray(  ((length(prob)-1):1)/length(prob)), 
       xlim=range(x[,1]),ylim=range(x[,2]),...) 
{

  #adapted from package hdrcde by Rob J Hyndman and Jochen Einbeck

  plot(c(0,0),xlim=xlim,ylim=ylim,type="n",...)
  add.hdr2d(x,prob,bw,cols) 
}

#########

#########
add.hdr2d<-function(x,prob=c(.025,.25,.5,.75,.975),bw=c(5,5),
       cols=gray(  ((length(prob)-1):1)/length(prob)  )) 
{

  require(ash)
  den <- ash2(bin2(x,nbin=round(rep(.5*sqrt(dim(x)[1]),2)) ), bw)
  fxy <- interp.2d(den$x,den$y,den$z,x[,1],x[,2])
  falpha <- quantile(sort(fxy), prob)
  index <- (fxy==max(fxy))
  mode <- c(x[index,1],x[index,2])
  .Internal(filledcontour(den$x,den$y,den$z,levels=c(falpha,1e10),col=cols ) )

}


##########
filledcontour<-function(x,y,z,nlevels=10,col=gray( (nlevels:0)/nlevels ),
                levels=pretty(range(z),nlevels) ) 
{
   .Internal(filledcontour(x,y,z,levels=c(levels,1e10),col=col ) )
}              
##########


#########
interp.2d<- function(x, y, z, x0, y0)
{
    # Bilinear interpolation of function (x,y,z) onto (x0,y0).
    # Taken from Numerical Recipies (second edition) section 3.6.
    # Called by hdr.info.2d
    # Vectorized version of old.interp.2d. 
    # Contributed by Mrigesh Kshatriya (mkshatriya@zoology.up.ac.za)

    nx <- length(x)
    ny <- length(y)
    n0 <- length(x0)
    z0 <- numeric(length = n0)
    xr <- diff(range(x))
    yr <- diff(range(y))
    xmin <- min(x)
    ymin <- min(y)
    j <- ceiling(((nx - 1) * (x0 - xmin))/xr)
    k <- ceiling(((ny - 1) * (y0 - ymin))/yr)
    j[j == 0] <- 1
    k[k == 0] <- 1
    j[j == nx] <- nx - 1
    k[k == ny] <- ny - 1
    v <- (x0 - x[j])/(x[j + 1] - x[j])
    u <- (y0 - y[k])/(y[k + 1] - y[k]) 
    AA <- z[cbind(j, k)]
    BB <- z[cbind(j + 1, k)]
    CC <- z[cbind(j + 1, k + 1)]
    DD <- z[cbind(j, k + 1)]
    z0 <- (1 - v) * (1 - u) * AA + v * (1 - u) * BB + v * u * CC + (1 - v) * u * DD
    return(z0)
}
#########
