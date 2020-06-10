options(digits=17)

# assume that z1 as the number of male who played Minecraft in the first survey
# assume also that z2 as the number of male who DID NOT play Minecraft in the first survey
# then z1, z2 are missing data in our EM-algorithm

# helper functions

a <- function(x, p1, p2) {
  return (x*p1/(p1+p2))
}

b <- function(n, x, p1, p2) {
  return ((n-x)*(1-p1)/(2-p1-p2))
}

c <- function(x, p1, p2) {
  return (x-x*p1/(p1+p2))
}

d <- function(n, x, p1, p2) {
  return (n-x-(n-x)*(1-p1)/(2-p1-p2))
}

ll <- function(n, x, m1, m2, x1, x2, p1, p2, z1, z2) {
  return (log(choose(z1+z2, z1) * p1^z1 * (1-p1)^z2 * choose(n-z1-z2, x-z1) * p2^(x-z1) * (1-p2)^(n-x-z2)
              * choose(m1, x1) * p1^x1 * (1-p1)^(m1-x1) * choose(m2, x2) * p2^x2 * (1-p2)^(m2-x2)))
}

em <- function(n, x, m1, m2, x1, x2, p1, p2, iter) {
  # p1 and p2 are initial guesses here
  
  m <- matrix(nrow=iter, ncol=3)
  colnames(m) <- rbind('est.p1', 'est.p2', 'log-likelihood')
  rownames(m) <- cbind(1:iter)
  
  for (i in 1:iter) {
    p1 <- ((a(x, p1, p2)+x1)/(a(x, p1, p2)+b(n, x, p1, p2)+m1))
    p2 <- ((c(x, p1, p2)+x2)/(c(x, p1, p2)+d(n, x, p1, p2)+m2))
    m[i,1] <- p1
    m[i,2] <- p2
    z1 <- x*p1/(p1+p2)
    z2 <- (n-x)*(1-p1)/(2-p1-p2)
    m[i,3] <- ll(n, x, m1, m2, x1, x2, p1, p2, z1, z2)
  }
  print(m)
}