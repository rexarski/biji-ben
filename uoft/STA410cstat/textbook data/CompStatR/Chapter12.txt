############################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 12 EXAMPLES (last update 10/1/2012)

############################################################################
### EXAMPLE 12.1 NORWEGIAN PAPER
############################################################################
# norwaypaper.dat = observed data
# y  = observed response data
# x1 = observed predictor data
# x2 = observed predictor data
############################################################################
## NOTES
# The following uses the gam() and interp() functions in the {gam} package
# for fitting generalized additive models. See the ?gam and ?interp
# help pages for more information. The {mgcv} package also contains a 
# newer implementation of gam() that is different than the version in 
# the {gam} package.  The {akima} package provides an interp() function.
############################################################################

## INITIAL VALUES
norwaypaper.dat = read.table(file.choose(),header=T)
y  = norwaypaper.dat$negy5
x1 = norwaypaper.dat$x1
x2 = norwaypaper.dat$x3
library(gam)    #you may need to install these packages
library(akima)

## MAIN
lmodel  = lm(y~x1+x2)
gamodel = gam(y~s(x1)+s(x2),family="gaussian")

## OUTPUT
summary(lmodel)       # SUMMARY OF LINEAR MODEL FIT
summary(gamodel)      # SUMMARY OF GAM FIT

## OUTPUT PLOTS
h.lm  = interp(x1,x2,fitted(lmodel))
h.gam = interp(x1,x2,fitted(gamodel))
par(mfrow=c(1,2))
persp(h.lm,theta=30,phi=15,ticktype="detailed",expand=0.5,
      xlab="x1",ylab="x2",zlab="y",main="Ordinary Linear Model")
persp(h.gam,theta=30,phi=15,ticktype="detailed",expand=0.5,
      xlab="x1",ylab="x2",zlab="y",main="Generalized Additive Model")


############################################################################
### EXAMPLE 12.2 DRUG ABUSE
############################################################################
# drugabuse.dat = observed data
# y  = observed response data
# x1 = observed predictor data
# x2 = observed predictor data
############################################################################
## NOTES
# The following uses the gam() and interp() functions in the {gam} package
# for fitting generalized additive models. See the ?gam and ?interp
# help pages for more information. The {mgcv} package also contains a 
# newer implementation of gam() that is different than the version in the 
# {gam} package.
############################################################################

## INITIAL VALUES
drugabuse.dat = read.table(file.choose(),header=T)
y  = drugabuse.dat$drugfree
x1 = drugabuse.dat$numtreatments
x2 = drugabuse.dat$age
library(gam)
library(akima)

## MAIN
gamodel = gam(y~s(x1)+s(x2),family="binomial")

## OUTPUT
summary(gamodel)      # SUMMARY OF MODEL FIT

## OUTPUT PLOTS
h.gam = interp(x1,x2,fitted(gamodel),duplicate="strip")
persp(h.gam,theta=30,phi=15,ticktype="detailed",expand=0.5,
      xlab="x1",ylab="x2",zlab="P[drug-free]",
      main="Generalized Additive Model")



############################################################################
### EXAMPLE 12.3 NORWEGIAN PAPER, PROJECTION PURSUIT REGRESSION
############################################################################
# norwaypaper.dat = observed data
# y  = observed response data
# x1 = observed predictor data
# x2 = observed predictor data
############################################################################
## NOTES
# The following uses the ppr() function. See the ?ppr help page
# for more information.
############################################################################

## INITIAL VALUES
norwaypaper.dat = read.table(file.choose(),header=T)
y  = norwaypaper.dat$negy5
x1 = norwaypaper.dat$x1
x2 = norwaypaper.dat$x3
x  = cbind(x1,x2)

## MAIN
ppr.m = ppr(x,y,nterms=2)

## OUTPUT
summary(ppr.m)      # SUMMARY OF MODEL FIT

## OUTPUT PLOTS
par(mfrow=c(1,2))
smod = ppr.m$smod
yx = matrix(smod[-(1:(length(smod)-2*length(x)))],length(y),4)
plot(yx[,3],yx[,1] + ppr.m$res,xlab="Term 1",ylab="")
lines(sort(yx[,3]),yx[order(yx[,3]),1])
plot(yx[,4],yx[,2] + ppr.m$res,xlab="Term 2",ylab="")
lines(sort(yx[,4]),yx[order(yx[,4]),2])



############################################################################
### EXAMPLE 12.4-6 STREAM MONITORING (CART)
############################################################################
# stream.dat = observed data
# y = observed response data
# x = observed predictor data
############################################################################
## NOTES
# The following uses functions in the {tree} package. See the ?tree
# help page for more information.
############################################################################

## INITIAL VALUES
stream.dat = read.table(file.choose(),header=T)
y = as.matrix(stream.dat[,2])
x = as.matrix(stream.dat[,c(17,23)])
colnames(x) = c("rock size","population")
library(tree)  #Note: you may need to install this package

## MAIN
model = tree(y~x)
sub.model = prune.tree(model,best=5)

## OUTPUT
sub.model

## OUTPUT PLOTS
par(ask=T)
plot(sub.model)
text(sub.model)

plot(x,cex=scale(y,center=F)+1)
abline(v=c(.4,-1.96))
segments(x0=c(-1.96,.4),y0=c(3.1,2.3),x1=c(.4,4),y1=c(3.1,2.3))

# In Edition 1, the methods used in Splus were a bit different.
# As a result, we omit Fig. 12.10 here


############################################################################
### EXAMPLE 12.7 PRINCIPAL CURVE FOR BIVARIATE DATA
############################################################################
# bivariatecurve.dat = observed data
# x  = observed data
# st = starting curve
############################################################################
## NOTES
# The following uses the principal.curve() function in the {princurve}
# package. See the ?principal.curve help page for more information.
############################################################################

## INITIAL VALUES
bivariatecurve.dat = read.table(file.choose(),header=T)
x    = as.matrix(bivariatecurve.dat)
st.x = c(seq(.5,-2,len=66),rep(-2,67),seq(-2,.5,len=66))
st.y = c(rep(1,66),seq(1,-1,len=67),rep(-1.3,66))
st   = cbind(st.x,st.y)
library(princurve)  #Note: you may need to install this package

## MAIN
model = principal.curve(x,start=st,df=10)

## OUTPUT PLOTS
plot(x)
lines(st,lty=2)
lines(model)


############################################################################
### END OF FILE

