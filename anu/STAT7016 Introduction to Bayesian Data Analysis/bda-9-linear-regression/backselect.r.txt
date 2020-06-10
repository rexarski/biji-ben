bselect<-function(y,X,p=0.05) 
{
  Xc<-X 
  remain<-1:dim(Xc)[2]
  removed<-NULL

  fit<-lm(y~-1+Xc)   
  pv<-summary(fit)$coef[,4]

  while(any(pv>p) & length(remain)> 0) {
    jpmax<-which.max(pv)
    Xc<-Xc[,-jpmax,drop=FALSE]
    removed<-c(removed,remain[jpmax])
    remain<-remain[-jpmax] 
    if(length(remain)>0 ) {fit<-lm(y~-1+Xc)   ; pv<-summary(fit)$coef[,4] }
    
                    }  
  list(remain=remain,removed=removed) 
} 


bselect.tcrit<-function(y,X,tcrit=qnorm(.975))
{
  Xc<-X
  remain<-1:dim(Xc)[2]
  s2<-removed<-NULL

  fit<-lm(y~-1+Xc)
  ts<-summary(fit)$coef[,3]
  s2<-summary(fit)$sigma^2
  while(any(abs(ts)<tcrit) & length(remain)> 0) {
    jpmax<-which.min(abs(ts))
    Xc<-Xc[,-jpmax,drop=FALSE]
    removed<-c(removed,remain[jpmax])
    remain<-remain[-jpmax]
    if(length(remain)>0 ) {fit<-lm(y~-1+Xc)   ; ts<-summary(fit)$coef[,3] ;
         s2<-c(s2,summary(fit)$sigma^2) }
   
                    }
  list(remain=remain,removed=removed)
}



