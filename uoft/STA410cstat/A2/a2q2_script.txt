source("a2q2.r")
data <- read.table("./ass2-data.txt", header=T)
para <- cbind(rep(1, 10), rep(1, 10), rep(0.5, 10), rep(0.1, 10))
beetle(data, para, 100)

# other initial guess
# which does NOT WORK -> ll goes to NaN
# mu <- mean(data$mass)
# vu <- mean(data$ratio)
# rho <- mean(data$swamp)
# alpha <- 0.1
# para1 <- cbind(rep(mu, 10), rep(vu, 10), rep(rho, 10), rep(alpha, 10))
# beetle(data, para1, 100)

# which WORKS
# para2 <- cbind(rep(0.1, 10), rep(0.1, 10), rep(0.9, 10), rep(0.1, 10))
# beetle(data, para2, 100)

###############plotting###############

data2 <- data
data2[,3] <- log(data[,3])
data2[,4] <- log(data[,4])

# log(mass) vs log(ratio)

x <- c(data2[data2$species == 1,]$mass,
       data2[data2$species == 2,]$mass,
       data2[data2$species == 3,]$mass,
       data2[data2$species == 4,]$mass,
       data2[data2$species == 5,]$mass,
       data2[data2$species == 6,]$mass,
       data2[data2$species == 7,]$mass,
       data2[data2$species == 8,]$mass,
       data2[data2$species == 9,]$mass,
       data2[data2$species == 10,]$mass,
       data2[is.na(data2$species) && data2$genus == 1, ]$mass,
       data2[is.na(data2$species) && data2$genus == 2, ]$mass,
       data2[is.na(data2$species) && data2$genus == 3, ]$mass,
       data2[is.na(data2$species) && data2$genus == 4, ]$mass,
       data2[is.na(data2$species) && is.na(data2$genus), ]$mass)
y <- c(data2[data2$species == 1,]$ratio,
       data2[data2$species == 2,]$ratio,
       data2[data2$species == 3,]$ratio,
       data2[data2$species == 4,]$ratio,
       data2[data2$species == 5,]$ratio,
       data2[data2$species == 6,]$ratio,
       data2[data2$species == 7,]$ratio,
       data2[data2$species == 8,]$ratio,
       data2[data2$species == 9,]$ratio,
       data2[data2$species == 10,]$ratio,
       data2[is.na(data2$species) && data2$genus == 1, ]$ratio,
       data2[is.na(data2$species) && data2$genus == 2, ]$ratio,
       data2[is.na(data2$species) && data2$genus == 3, ]$ratio,
       data2[is.na(data2$species) && data2$genus == 4, ]$ratio,
       data2[is.na(data2$species) && is.na(data2$genus), ]$ratio)
plot(x, y, pch = c(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18),
     main = "log(mass) vs log(ratio)", xlab = "log(mass)", ylab = "log(ratio)")
legend("right", c("sp1","sp2","sp3","sp4","sp5","sp6","sp7","sp8","sp9","sp10","g1","g2","g3","g4","NA"),
       cex=0.8, pch=c(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18))

# log(mass) vs swamp

x1 <- c(data2[data2$species == 1,]$mass,
       data2[data2$species == 2,]$mass,
       data2[data2$species == 3,]$mass,
       data2[data2$species == 4,]$mass,
       data2[data2$species == 5,]$mass,
       data2[data2$species == 6,]$mass,
       data2[data2$species == 7,]$mass,
       data2[data2$species == 8,]$mass,
       data2[data2$species == 9,]$mass,
       data2[data2$species == 10,]$mass,
       data2[is.na(data2$species) && data2$genus == 1, ]$mass,
       data2[is.na(data2$species) && data2$genus == 2, ]$mass,
       data2[is.na(data2$species) && data2$genus == 3, ]$mass,
       data2[is.na(data2$species) && data2$genus == 4, ]$mass,
       data2[is.na(data2$species) && is.na(data2$genus), ]$mass)
y1 <- c(data2[data2$species == 1,]$swamp,
       data2[data2$species == 2,]$swamp,
       data2[data2$species == 3,]$swamp,
       data2[data2$species == 4,]$swamp,
       data2[data2$species == 5,]$swamp,
       data2[data2$species == 6,]$swamp,
       data2[data2$species == 7,]$swamp,
       data2[data2$species == 8,]$swamp,
       data2[data2$species == 9,]$swamp,
       data2[data2$species == 10,]$swamp,
       data2[is.na(data2$species) && data2$genus == 1, ]$swamp,
       data2[is.na(data2$species) && data2$genus == 2, ]$swamp,
       data2[is.na(data2$species) && data2$genus == 3, ]$swamp,
       data2[is.na(data2$species) && data2$genus == 4, ]$swamp,
       data2[is.na(data2$species) && is.na(data2$genus), ]$swamp)
plot(x1, y1, pch = c(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18),
     main = "log(mass) vs swamp", xlab = "log(mass)", ylab = "swamp")
legend("right", c("sp1","sp2","sp3","sp4","sp5","sp6","sp7","sp8","sp9","sp10","g1","g2","g3","g4","NA"),
       cex=0.8, pch=c(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18))

# log(ratio) vs swamp

x2 <- c(data2[data2$species == 1,]$ratio,
        data2[data2$species == 2,]$ratio,
        data2[data2$species == 3,]$ratio,
        data2[data2$species == 4,]$ratio,
        data2[data2$species == 5,]$ratio,
        data2[data2$species == 6,]$ratio,
        data2[data2$species == 7,]$ratio,
        data2[data2$species == 8,]$ratio,
        data2[data2$species == 9,]$ratio,
        data2[data2$species == 10,]$ratio,
        data2[is.na(data2$species) && data2$genus == 1, ]$ratio,
        data2[is.na(data2$species) && data2$genus == 2, ]$ratio,
        data2[is.na(data2$species) && data2$genus == 3, ]$ratio,
        data2[is.na(data2$species) && data2$genus == 4, ]$ratio,
        data2[is.na(data2$species) && is.na(data2$genus), ]$ratio)
y2 <- c(data2[data2$species == 1,]$swamp,
        data2[data2$species == 2,]$swamp,
        data2[data2$species == 3,]$swamp,
        data2[data2$species == 4,]$swamp,
        data2[data2$species == 5,]$swamp,
        data2[data2$species == 6,]$swamp,
        data2[data2$species == 7,]$swamp,
        data2[data2$species == 8,]$swamp,
        data2[data2$species == 9,]$swamp,
        data2[data2$species == 10,]$swamp,
        data2[is.na(data2$species) && data2$genus == 1, ]$swamp,
        data2[is.na(data2$species) && data2$genus == 2, ]$swamp,
        data2[is.na(data2$species) && data2$genus == 3, ]$swamp,
        data2[is.na(data2$species) && data2$genus == 4, ]$swamp,
        data2[is.na(data2$species) && is.na(data2$genus), ]$swamp)
plot(x2, y2, pch = c(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18),
     main = "log(ratio) vs swamp", xlab = "log(ratio)", ylab = "swamp")
legend("right", c("sp1","sp2","sp3","sp4","sp5","sp6","sp7","sp8","sp9","sp10","g1","g2","g3","g4","NA"),
       cex=0.8, pch=c(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18))