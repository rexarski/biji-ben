source("a3.r")
data <- read.table("./ass2-data.txt", header=T)
initial <- matrix(0.5, 10, 3)
alpha <- c(0.05, 0.20, 0.05, 0.06, 0.04, 0.15, 0.05, 0.15, 0.20, 0.05)

# To see whether the manually sampled species for "missing-species data" is consistent,
# we want to do this tiny test run. The target beetles are the third and fourth beetles
# in original data which don't have species.

test <- 1

res <- gibbs(data,initial,30)

plot(1:30, res[, 1], main="beetle 3 simulated species", 
     xlab="simulation times ", ylab="species", pch=19, family="Palatino")
plot(1:30, res[, 2], main="beetle 4 simulated species", 
     xlab="simulation times ", ylab="species", pch=19, family="Palatino")

# consider burn-in?
plot(16:30, res[16:30, 1], main="beetle 3 simulated species with burn-in", 
     xlab="simulation times ", ylab="species", pch=19, family="Palatino")
plot(16:30, res[16:30, 2], main="beetle 4 simulated species with burn-in", 
     xlab="simulation times ", ylab="species", pch=19, family="Palatino")

# Test run swithc off (for better performance)
test <- 0

r <- gibbs(data,initial,300)

plot(NULL, xlim=c(1, 300), ylim=range(c(r$rho, r$mu)), xlab="simulation times", ylab="value", family="Palatino")
for (i in 1:ncol(r$mu)) lines (r$mu[, i])
for (i in 1:ncol(r$vu)) lines (r$vu[, i], col="red") 
for (i in 1:ncol(r$rho)) lines (r$rho[, i], col="blue")

plot(NULL, xlim=c(1, 300), ylim=range(c(0, r$mu)), xlab="simulation times", ylab="value", family="Palatino")
for (i in 1:ncol(r$mu)) lines (r$mu[, i])

plot(NULL, xlim=c(1, 300), ylim=range(c(0, r$vu)), xlab="simulation times", ylab="value", family="Palatino")
for (i in 1:ncol(r$vu)) lines (r$vu[, i])

plot(NULL, xlim=c(1,300), ylim=range(c(0, r$rho)), xlab="simulation times", ylab="value", family="Palatino")
for (i in 1:ncol(r$rho)) lines (r$rho[, i])

# Discard first 15 iterations as burn-in

burn_in <- 15

# print estimated posterior means and standard deviations of each parameters

m1 <- rbind(colMeans(r$mu[(burn_in+1):300, ]),
            apply(r$mu[(burn_in+1):300, ], 2, sd))
colnames(m1) <- c("sp1", "sp2", "sp3", "sp4", "sp5", "sp6", "sp7", "sp8", "sp9", "sp10")
rownames(m1) <- c("mean", "sd")
print(m1)

m2 <- rbind(colMeans(r$vu[(burn_in+1):300, ]),
            apply(r$vu[(burn_in+1):300,], 2, sd))
colnames(m2) <- c("sp1", "sp2", "sp3", "sp4", "sp5", "sp6", "sp7", "sp8", "sp9", "sp10")
rownames(m2) <- c("mean", "sd")
print(m2)

m3 <- rbind(colMeans(r$rho[(burn_in+1):300,] ),
            apply(r$rho[(burn_in+1):300,], 2, sd))
colnames(m3) <- c("sp1", "sp2", "sp3", "sp4", "sp5", "sp6", "sp7", "sp8", "sp9", "sp10")
rownames(m3) <- c("mean", "sd")
print(m3)


