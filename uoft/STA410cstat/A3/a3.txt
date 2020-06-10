# a function to calculate the probability of each species given a certain k-th beetle entry
# m := log mass of this beetle
# r := log ratio of this beetle
# sw := swamp condition of this beetle
# para is a 10 by 3 parameter matrix

calcProb <- function(k, data, para, alpha) { 
  
  entry <- data[k,]
  sp <- entry[1, 1]
  g <- entry[1, 2]
  m <- log(entry[1, 3])
  r <- log(entry[1, 4])
  sw <- entry[1, 5]
  up <- rep(0, 10)
  down <- 0
  
  if (is.na(sp) && is.na(g)) {
    for (i in 1:10) {
      up[i] <- helper(i, para, m, r, sw)
      down <- down+helper(i, para, m, r, sw)
    }
  }
  
  if (!is.na(g) && is.na(sp)) {
    if (g==1) {
      for (i in 1:3) {
        up[i] <- helper(i, para, m, r, sw)
        down <- down+helper(i, para, m, r, sw)
      }
    }
    
    if(g==2){
      for(i in 4:5){
        up[i] <- helper(i, para, m, r, sw)
        down <- down+helper(i, para, m, r, sw)
      }
    }
    
    if(g==3){
      for(i in 6:7){
        up[i] <- helper(i, para, m, r, sw)
        down <- down+helper(i, para, m, r, sw)
      }
    }
    
    if(g==4){
      for(i in 8:10){
        up[i] <- helper(i, para, m, r, sw)
        down <- down+helper(i, para, m, r, sw)
      }
    }
  }
  up <- up/down
  return(up)
}

helper <- function(i, para, m, r, sw) {
  return(dnorm(m, para[i, 1], 0.08)*dnorm(r, para[i, 2], 0.1)*
    (para[i, 3]^sw)*((1-para[i, 3])^(1-sw))*(alpha[i]))
}

# a function used to generate a species "manually" for those
# beetles that don't have species information at the beginning
dataModify <- function(data,para,alpha) {
  
  data1 <- data
  for (k in 1:nrow(data1)) {
    if (is.na(data1[k,1])) {
      data1[k,1] <- sample(1:10, 1, prob=calcProb(k, data, para, alpha))
    } else {
      data1[k,1] <- data[k,1]
    }
  }
  return(data1)
}

gibbs <- function(data, initial, iter) {
  
  results <- list(mu=matrix(nrow=iter, ncol=10), vu=matrix(nrow=iter, ncol=10),
   rho=matrix(nrow=iter, ncol=10))

  para <- initial
  
  storage <- matrix(0,iter,2)
  
  for (t in 1:iter) {
    data2 <- dataModify(data,para,alpha)
    # the following if-loop is only used for a test-run
    if (test==1) {
      storage[t, 1] <- data2[3, 1]
      storage[t, 2] <- data2[4, 1]
    }
    for (i in 1:10) {
      n <- sum(data2[, 1]==i)
      rho_temp <- sum(data2[which(data2[, 1]==i), 5])/n
      results$mu[t, i] <- rnorm(1, (0.5+2*sum(log(data2[which(data2[, 1]==i), 3]))/0.08^2)/(2*sqrt(0.25+n/0.08^2)), 1) *
        (1/(sqrt(0.25+n/0.08^2)))
      results$vu[t, i] <- rnorm(1, (0.5+2*sum(log(data2[which(data2[, 1]==i), 4]))/0.1^2)/(2*sqrt(0.25+n/0.1^2)), 1) *
        (1/(sqrt(0.25+n/0.1^2)))
      results$rho[t, i] <- rbeta(1, sum(data2[which(data2[, 1]==i), 5]) + 1, n + 1 -  sum(data2[which(data2[, 1]==i), 5]))
      para[i, 1] <- results$mu[t, i]
      para[i, 2] <- results$vu[t, i]
      para[i, 3] <- results$rho[t, i]
    }
  }
  # also only for a test-run
  if (test==1) {
    return(storage)
  }
  results
}
