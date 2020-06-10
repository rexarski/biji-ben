set.seed(7016)
library(ggplot2)
library(ggfortify)
library(coda)
library(fitR)
library(survival)
library(survminer)
library(ggthemes)
source("regression_gprior.r")

# -------------------DATA PREP---------------------
death <- read.csv("character-deaths.csv",header=T)
death$Allegiances <- sub("House ","",death$Allegiances)
unique(death$Allegiances)
death <- death[!is.na(death$Book.Intro.Chapter),] # now we have 905 characters left

# add a Book.of.Intro variable
death$Book.of.Intro = 0
X1 = which(death$GoT == 1)
X2 = which(death$CoK == 1 & death$GoT == 0)
X3 = which(death$SoS== 1 & death$CoK == 0 & death$GoT == 0)
X4 = which(death$FfC ==1 & death$SoS == 0 & death$CoK == 0 & death$GoT == 0)
X5 = which(death$DwD == 1 & death$FfC == 0 & death$SoS == 0 & death$CoK == 0 & death$GoT == 0)
death$Book.of.Intro[X1] = 1
death$Book.of.Intro[X2] = 2
death$Book.of.Intro[X3] = 3
death$Book.of.Intro[X4] = 4
death$Book.of.Intro[X5] = 5

# # same book death
# same.book.death <- which(death$Book.of.Intro==death$Book.of.Death)
# sbd1 = sum(death$Book.of.Intro[same.book.death]==1)
# sbd2 = sum(death$Book.of.Intro[same.book.death]==2)
# sbd3 = sum(death$Book.of.Intro[same.book.death]==3)
# sbd4 = sum(death$Book.of.Intro[same.book.death]==4)
# sbd5 = sum(death$Book.of.Intro[same.book.death]==5)
# summary(c(sbd1,sbd2,sbd3,sbd4,sbd5))
# # Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# # 9.0    26.0    48.0    37.8    53.0    53.0 

# life span of a character
bookch <- c(73-1,70-1,82-1,46-1,73-1) # minus appendix of each book
max.life <- sum(bookch) # 339
death$Life <- death$GoT*bookch[1]+death$CoK*bookch[2]+
    death$SoS*bookch[3]+death$FfC*bookch[4]+death$DwD*bookch[5]
# subtract chapters in the intro book but before introduction
for (i in c(X1,X2,X3,X4,X5)) {
    death$Life[i] <- death$Life[i]-death$Book.Intro.Chapter[i]
}
# death[!is.na(death$Book.of.Death)&is.na(death$Death.Chapter),]
# 8 characters have a book of death but no chapter of death
# subtract chapters in the death book but after death
for (i in 1:nrow(death)){
    if (!is.na(death$Book.of.Death[i])) {
        if (is.na(death$Death.Chapter[i])) {
            # the special procedure: we assume they survived 
            # half of the chapters in that book
            death$Life[i] <- death$Life[i]-
                (floor(bookch[death$Book.of.Death[i]]*0.5))
        } else {
            # the common procedure
            death$Life[i] <- death$Life[i]-(bookch[death$Book.of.Death[i]]
                                            -death$Death.Chapter[i])    
        }
    }
}

death <- death[-which(death$Life<0),] # remove some negative life characters

# add variable Status
death$Status <- rep(NA,nrow(death))
for (i in 1:nrow(death)) {
    if (is.na(death$Death.Chapter[i])) {
        death$Status[i] <- 1
    } else {
        death$Status[i] <- 0
    }
}

# add another variable POV for major characters (book 6 excluded)

death$POV <- rep(0,nrow(death))
POVnames <- c("Eddard Stark","Catelyn Tully","Sansa Stark","Arya Stark",
              "Bran Stark","Jon Snow","Daenerys Targaryen","Tyrion Lannister",
              "Theon Greyjoy","Davos Seaworth","Samwell Tarly","Jaime Lannister",
              "Cersei Lannister","Brienne of Tarth","Areo Hotah","Arys Oakheart",
              "Arianne Martell","Asha Greyjoy","Aeron Greyjoy","Victarion Greyjoy",
              "Quentyn Martell","Jon Connington","Barristan Selmy","Melisandre")
POVcounts <- c(15,25,24,33,21,42,31,47,13,13,10,17,12,8,2,1,2,4,2,4,4,2,4,1)

for (aMan in 1:length(POVnames)) {
    death$POV[which(death$Name==POVnames[aMan])] <- POVcounts[aMan]
}

df <- subset(death,select=c("Name","Life","Gender","Nobility","POV","Allegiances","Status"))

# Arryn <- ifelse(df$Allegiances=="Arryn",1,0)
# Baratheon <- ifelse(df$Allegiances=="Baratheon",1,0)
# Greyjoy <- ifelse(df$Allegiances=="Greyjoy",1,0)
# Lannister <- ifelse(df$Allegiances=="Lannister",1,0)
# Martell <- ifelse(df$Allegiances=="Martell",1,0)
# NightsWatch <- ifelse(df$Allegiances=="Night's Watch",1,0)
# None <- ifelse(df$Allegiances=="None",1,0)
# Stark <- ifelse(df$Allegiances=="Stark",1,0)
# Targaryen <- ifelse(df$Allegiances=="Targaryen",1,0)
# Tully <- ifelse(df$Allegiances=="Tully",1,0)
# Tyrell <- ifelse(df$Allegiances=="Tyrell",1,0)
# Wildling <- ifelse(df$Allegiances=="Wildling",1,0)

df$first <- ifelse(df$Allegiances%in%c("Stark","Lannister","Targaryen"),1,0)
df$second <-ifelse(df$Allegiances%in%c("Arryn","Baratheon","Greyjoy",
                                    "Martell","Tully","Tyrell"),1,0)
# df$third <- ifelse(df$Allegiances%in%c("Night's Watch","None","Wildling"),1,0)

df$GxN <- df$Gender*df$Nobility # interactions

# prepare for cross-validation
dim(df)
sample.index <- sample(1:899,99,replace=F)
df.test <- df[sample.index,]
df <- df[-sample.index,]

# -------------Simple model--------------

# training
X <- cbind(rep(1,nrow(df)),
           df$Gender,df$Nobility,df$POV,df$first,df$second,df$GxN) # df$third
colnames(X) <- c("int","G","N","P","first","second","G:N") # ,"third"
y <- df$Life

# testing
X.test <- cbind(rep(1,nrow(df.test)),
           df.test$Gender,df.test$Nobility,df.test$POV,
           df.test$first,df.test$second,df.test$GxN) #df.test$third,
colnames(X.test) <- c("int","G","N","P","first","second","G:N") # ,"third"
y.test <- df.test$Life

index <- list(2,3,4,5:6,
              c(2,3),c(2,3,7),c(2,4),c(2,5:6),
              c(3,4),c(3,5:6),c(4,5:6),
              c(2,3,4,7),c(2,3,5:6,7),
              c(2,4,5:6),c(3,4,5:6),
              c(2,3,4,5:6,7))

z <- matrix(data=rep(c(1,rep(0,ncol(X)-1)),length(index)+1),ncol=ncol(X),byrow=T)

# G, N, P, allegiances, G:N
# 2, 3, 4, 5:6,   7

# z[1,] # null model
for (i in 1:length(index)) {
    z[1+i,index[[i]]] <- 1
}

# marginal probability
lpy.p <- NULL
for (i in 1:nrow(z)) {
    z.use <- z[i,]
    lpy.p <- c(lpy.p,lpy.X(y,X[,z.use==1,drop=FALSE]))
}
mprob <- data.frame(matrix(rep(NA,2*(length(index)+1)),ncol=2))
margin.prob <- round(exp(-mean(lpy.p)+lpy.p)/sum(exp(-mean(lpy.p)+lpy.p)),4)

# store model and marginal probabilities in a data frame
for(i in 1:nrow(z)){
    model <- "("
    for(j in 1:(ncol(z)-1)){
        model <- paste(model,z[i,j],",",sep="")
    }
    model <- paste(model,z[i,ncol(z)],")",sep="")
    mprob[i,1] <- model
    mprob[i,2] <- margin.prob[i]
}
colnames(mprob) <- c("model","MargProb")
mprob

# posterior
beta.post <- lm.gprior(y,X)$beta
beta.bar <- apply(beta.post,2,mean)
beta.post.ci <- apply(beta.post,2,function(x) quantile(x,c(0.025,0.975)))
beta.post.table <- cbind(beta.bar,t(beta.post.ci))
colnames(beta.post.table)[1] <- c("est")
beta.post.table

# model averaging with MCMC
z <- rep(1,ncol(X)) # initial values
S <- 10000 # number of simulations
BETA <- matrix(NA,S,ncol(X))
lpy.c <- lpy.X(y,X[,z==1,drop=FALSE])
Z <- matrix(NA,S,ncol(X))
BETA <- matrix(NA,S,ncol(X))

# Gibbs sampler
start.time <- Sys.time()
for(s in 1:S) {
    if (s%%100==0) {
    looptime <- Sys.time()-start.time
    cat(s," LOOPS SIMULATED... AND IT'S BEEN", 
        difftime(Sys.time(),start.time,units = "mins"), "MINS! \n")
    }
    for (j in sample(2:dim(X)[2])) {
        zp <- z; zp[j] <- 1-zp[j]
        lpy.p <- lpy.X(y,X[,zp==1,drop=FALSE])
        r <- (lpy.p-lpy.c)*(-1)^(zp[j]==0)
        z[j] <- rbinom(1,1,1/(1+exp(-r)))
        if (z[j]==zp[j]) {
            lpy.c <- lpy.p
        }
    }
    beta <- z
    if(sum(z)>0){beta[z==1] <- lm.gprior(y,X[,z==1,drop=FALSE],S=1)$beta}
    Z[s,] <- z
    BETA[s,] <- beta
}

p.not0 <- apply(BETA,2,function(x) mean(x!=0))
beta.bma <- apply(BETA,2,mean,na.rm=TRUE)
beta.bma.ci <- apply(BETA,2,function(x) quantile(x,probs=c(0.025,0.975)))
beta.bma.table <- cbind(p.not0,beta.bma,t(beta.bma.ci))
colnames(beta.bma.table)[1:2] <- c("pr(beta!=0)","est")
rownames(beta.bma.table) <- c("int","G","N","P","first","second","G:N")
beta.bma.table

# -------------MCMC diagnostics-------------

# Effective Sample Size 
ef.beta <- NULL
apply(BETA,2,effectiveSize)

# traceplot
my.mcmc <- mcmc(BETA)
plot(burnAndThin(my.mcmc,burn=1000,thin=10))

# acf
autocorr.plot(burnAndThin(my.mcmc,burn=1000,thin=10))

# recall model selection mariginal prob
which(mprob$MargProb>1/(length(index)+1))
# only model 10 greater than prior
mprob[c(10),]
sum(mprob$MargProb[c(10,16)]) #  0.9959

# --------------------Predictions---------------
# prediction test

# in testing set
alle <- rep(NA,nrow(X.test))
for (i in 1:nrow(X.test)) {
    if (X.test[i,5]==1) {
        alle[i] <- 1
    } else if (X.test[i,6]==1) {
        alle[i] <- 2
    } else {
        alle[i] <- 3
    }
}

pred.test2 <- data.frame(cbind(X.test%*%beta.bma,y.test,alle))
colnames(pred.test2) <- c("predicted","true","alle")
ggplot(pred.test2,aes(x=predicted,y=true))+
    geom_point(aes(color=cut(alle,c(0,1,2,3))),size=3,alpha=0.6)+
    scale_color_manual(name="Allegiance",
                       values=c("(0,1]"="blue","(1,2]"="green","(2,3]"="red"),
                       labels=c("first","second","third"))+
    geom_rug(alpha=0.5)+
    geom_abline(slope=1)+
    ggtitle("Observed Life Span vs Predicted Life Span",subtitle="in Testing Data")+
    labs(alle="Allegiance Group",x="Predicted Life Span",y="Observed Life Span")+
    theme_minimal()
    

# only main characters
pov.index <- c(which(df$POV!=0),which(df.test$POV!=0))
combine <- rbind(X,X.test)[pov.index,]
alle.main <- rep(NA,nrow(combine))
for (i in 1:nrow(combine)) {
    if (combine[i,5]==1) {
        alle.main[i] <- 1
    } else if (combine[i,6]==1) {
        alle.main[i] <- 2
    } else {
        alle.main[i] <- 3
    }
}
pred.main <- data.frame(cbind(combine%*%beta.bma,c(y,y.test)[pov.index],alle.main))
colnames(pred.main) <- c("predicted","true","alle")
ggplot(pred.main,aes(x=predicted,y=true))+
    geom_point(aes(color=cut(alle,c(0,1,2,3))),size=3,alpha=0.6)+
    scale_color_manual(name="Allegiance",
                       values=c("(0,1]"="blue","(1,2]"="green","(2,3]"="red"),
                       labels=c("first","second","third"))+
    geom_rug(alpha=0.5)+
    geom_abline(slope=1)+
    geom_abline(slope=1,intercept=mean(bookch))+
    geom_abline(slope=1,intercept=-mean(bookch))+
    ggtitle("Observed Life Span vs Predicted Life Span",
            subtitle="Characters with POV")+
    labs(x="Predicted Life Span",y="Observed Life Span")+
    theme_minimal()

# -------------------Survival Analysis-----------
# KM model

# add a marker
df.surv <- subset(death,select=c("Name","Life","Gender","Nobility","POV","Allegiances","Status"))

class <- rep(0,nrow(df.surv))
for (i in 1:nrow(df.surv)) {
    if (df.surv$Allegiances[i]%in%c("Lannister","Stark","Targaryen")) {
        class[i] <- "1st"
    } else if (df.surv$Allegiances[i]%in%c("Arryn","Baratheon","Greyjoy",
                                   "Martell","Tully","Tyrell")) {
        class[i] <- "2nd"
    } else if (df.surv$Allegiances[i]%in%c("Night's Watch","None","Wildling")) {
        class[i] <- "3rd"
    }
}
df.surv$class <- class

# ggsurvplot(survfit(Surv(Life,Status)~1,data=df),
           # ggtheme=theme_minimal())

ggsurvplot(survfit(Surv(Life,Status)~class,data=df.surv),
           ggtheme=theme_minimal(),title="Survival Curves by Allegiances")

ggsurvplot(survfit(Surv(Life,Status)~Gender,data=df.surv),
           ggtheme=theme_minimal(),title="Survival Curves by Gender")

ggsurvplot(survfit(Surv(Life,Status)~Nobility,data=df.surv),
           ggtheme=theme_minimal(),title="Survival Curves by Nobility")
