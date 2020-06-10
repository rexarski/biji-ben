# l is a function deals with likelihood which iterates through all
# necessary species (either given genus or not)
# para: the parameter matrix, as given initial guess at first,
#       updates after every iteration
# m: the log mass of this beetle
# r: the log ratio of this beetle
# w: the swamp condition of this beetle
# g: the genus type of this beetle,
#   - when g == 1, the species type could be 1, 2, 3
#   - when g == 2, the species type could be 4, 5
#   - when g == 3, the species type could be 6, 7
#   - when g == 4, the species type could be 8, 9, 10
#   - when g is NA (set to 5), the species type could be any number in 1:10
# sp: TRUE if this beetle has speices already;
#     FALSE if this beetle does not.

l <- function(para, m, r, w, g, sp){
  res <- 1
  if (sp == FALSE) {
    if (g == 5) {
      for (i in 1:10) {
        res <- res * helper(para, m, r, w, i)
      }
    }
    if (g == 1) {
      for (i in 1:3) {
        res <- res * helper(para, m, r, w, i)
      }
    }
    if (g == 2) {
      for (i in 4:5) {
        res <- res * helper(para, m, r, w, i)
      }
    }
    if (g == 3) {
      for (i in 6:7) {
        res <- res * helper(para, m, r, w, i)
      }
    }
    if (g == 4) {
      for (i in 8:10) {
        res <- res * helper(para, m, r, w, i)
      }
    }
  } else if (sp == TRUE) {
    res <- helper(para, m, r, w, g)
  }
  return(res)
}

# a helper function used multiple times in likelihood function,
# basically it calculates the product of different probability densities
# assuming the beetle is one certain species. So, if we want to calculate
# the likelihood of a beetle given genus, we should take cumulative product
# among all possible species of this genus; similarly, if genus not given,
# we should rather take cumulative product among all 10 possible species.

helper <- function(para, m, r, w, i) {
  mu_sd <- 0.08
  vu_sd <- 0.1
  return(dnorm(m, para[i, 1], mu_sd) * dnorm(r, para[i, 2], vu_sd) * 
           (para[i, 3]^w) * ((1 - para[i, 3])^(1 - w)) *
           para[i, 4])
}

# data: the data we want to operate on
#     - data[i, 1]: the species of i-th beetle in data
#     - data[i, 2]: the genus of i-th beetle in data
#     - data[i, 3]: the mass of i-th beetle in data
#     - data[i, 4]: the ratio of i-th beetle in data
#     - data[i, 5]: the swamp condition of i-th beetle in data
# iter: the number of iterations we manually plug in

beetle <- function(data, para, iter) {
  p <- matrix(0, 500, 10)
  g <- 0
  for (j in 1:iter) {
    ll <- 0
    # ll: log-likelihood
    for (i in 1:nrow(data)) {
      # if this beetle has no species
      if (is.na(data[i, 1])) {
        if (is.na(data[i, 2])) {
          # if it also has no genus
          g <- 5
          p[i,] <- estep(para, log(data[i, 3]), log(data[i, 4]), data[i, 5], g)
          ll <- ll + log(l(para, log(data[i, 3]), log(data[i, 4]), data[i, 5], g, FALSE))
        } else {
          # has genus
          g <- data[i, 2]
          p[i,] <- estep(para, log(data[i, 3]), log(data[i, 4]), data[i, 5], g)
          ll <- ll + log(l(para, log(data[i, 3]), log(data[i, 4]), data[i, 5], g, FALSE))
        }
      } else {
        # it has species and genus
        g <- data[i, 1]
        p[i, g] <- 1
        ll <- ll + log(l(para, log(data[i, 3]), log(data[i, 4]), data[i, 5], g, TRUE))
      }
    }
    cat("Log-likelihood of", j, "itertaion is", ll, "\n")
    para <- mstep(para, p, data)
    # print(para)
    # the previous line is only not commented out for calculating rate of convergence
  }
  # update para and return it in a good form
  colnames(para) <- rbind("mu", "vu", "rho", "alpha")
  rownames(para) <- cbind("sp1", "sp2", "sp3", "sp4", "sp5", "sp6", "sp7", "sp8", "sp9", "sp10")
  return(para)
}

# E-step
# pm: a 10 by 1 probability matrix/vector
estep <- function(para, m, r, w, g) {
  pm <- matrix(0, nrow(para), 1)
  deno <- 0
  if (g == 1) {
    for (i in 1:3) {
      pm[i, 1] <- helper(para, m, r, w, i)
      deno<- deno + helper(para, m, r, w, i)
    }
  }
  if (g == 2) {    
    for (i in 4:5) {
      pm[i, 1] <- helper(para, m, r, w, i)
      deno<- deno + helper(para, m, r, w, i)
    }
  }
  if(g == 3) {
    for(i in 6:7) {
      pm[i, 1] <- helper(para, m, r, w, i)
      deno<- deno + helper(para, m, r, w, i)
    }
  }
  if (g == 4) {  
    for (i in 8:10) {
      pm[i, 1] <- helper(para, m, r, w, i)
      deno<- deno + helper(para, m, r, w, i)
    }
  }
  if (g == 5) {
    for (i in 1:10) {
      pm[i, 1] <- helper(para, m, r, w, i)
      deno<- deno + helper(para, m, r, w, i)
    }
  } 
  pm <- pm / deno
  return(t(pm))
}

# M-step
# para[i, 1]: estimated mean mass of species i
# para[i, 2]: estimated mean ratio of species i
# para[i, 3]: estimated mean swamp condition of species i
# para[i, 4]: estimated collected probability of species i

mstep <- function(para, p, data) {
  for (i in 1:10) {
    para[i, 1] <- sum(log(data[,3]) * p[,i]) / sum(p[,i])
    para[i, 2] <- sum(log(data[,4]) * p[,i]) / sum(p[,i])
    para[i, 3] <- sum(data[,5] * p[,i]) / sum(p[,i])
    para[i, 4] <- sum(p[,i]) / sum(p)
  }
  return(para)
}
