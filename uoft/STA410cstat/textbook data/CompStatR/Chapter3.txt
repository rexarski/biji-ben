#########################################################################
# COMPUTATIONAL STATISTICS
# by Geof Givens and Jennifer Hoeting
# CHAPTER 3 EXAMPLES (last update 10/1/12)
#########################################################################
### EXAMPLE 3.3 RANDOM STARTS LOCAL SEARCH
#########################################################################
# baseball.dat 	= entire data set
# baseball.sub 	= matrix of all predictors
# salary.log	= response, log salary
# n 		= number of observations in the data set
# m 		= number of predictors in the data set
# num.starts 	= number of random starts
# runs 		= matrix containing the random starts where each row is a
# 		  vector of the parameters included for the model
# 		  (1 = included, 0 = omitted)
# runs.aic	= AIC values for the best model found for each
# 		  of the random starts
# itr 		= number of iterations for each random start
#########################################################################

## INITIAL VALUES
baseball.dat = read.table(file.choose(),header=TRUE)
baseball.dat$freeagent = factor(baseball.dat$freeagent)
baseball.dat$arbitration = factor(baseball.dat$arbitration)
baseball.sub = baseball.dat[,-1]
salary.log = log(baseball.dat$salary)
n = length(salary.log)
m = length(baseball.sub[1,])
num.starts = 5
runs = matrix(0,num.starts,m)
itr = 15
runs.aic = matrix(0,num.starts,itr)

# INITIALIZES STARTING RUNS
set.seed(19676) 
for(i in 1:num.starts){runs[i,] = rbinom(m,1,.5)}

## MAIN
for(k in 1:num.starts){
	run.current = runs[k,]

	# ITERATES EACH RANDOM START
	for(j in 1:itr){
		run.vars = baseball.sub[,run.current==1]
		g = lm(salary.log~.,run.vars)
		run.aic = extractAIC(g)[2]
		run.next = run.current

		# TESTS ALL MODELS IN THE 1-NEIGHBORHOOD AND SELECTS THE
		# MODEL WITH THE LOWEST AIC
		for(i in 1:m){
			run.step = run.current
			run.step[i] = !run.current[i]
			run.vars = baseball.sub[,run.step==1]
			g = lm(salary.log~.,run.vars)
			run.step.aic = extractAIC(g)[2]
			if(run.step.aic < run.aic){
				run.next = run.step
				run.aic = run.step.aic
			}
		}
		run.current = run.next
		runs.aic[k,j]=run.aic
	}
	runs[k,] = run.current
}

## OUTPUT
runs 		# LISTS OF PREDICTORS
runs.aic 	# AIC VALUES

##PLOT
plot(1:(itr*num.starts),-c(t(runs.aic)),xlab="Cumulative Iterations",
  ylab="Negative AIC",ylim=c(360,420),type="n")
for(i in 1:num.starts) {
  lines((i-1)*itr+(1:itr),-runs.aic[i,]) }



#########################################################################
### EXAMPLE 3.4 SIMULATED ANNEALING
#########################################################################
# baseball.dat 	= entire data set
# baseball.sub 	= matrix of all predictors
# salary.log 	= response, log salary
# n 		= number of observations in the data set
# m 		= number of predictors in the data set
# run 		= vector of the parameters included in the best model found
# 		  (1 = included, 0 = omitted)
# best.aic 	= AIC value for the best model found
# aics 		= AIC values for the model at each step
# 		  (used for plotting)
# cooling 	= cooling schedule
# tau.start 	= initial temperature
# tau 		= temperature schedule
#########################################################################

## INITIAL VALUES
baseball.dat = read.table(file.choose(),header=TRUE)
baseball.dat$freeagent = factor(baseball.dat$freeagent)
baseball.dat$arbitration = factor(baseball.dat$arbitration)
baseball.sub = baseball.dat[,-1]
salary.log = log(baseball.dat$salary)
n = length(salary.log)
m = length(baseball.sub[1,])
cooling = c(rep(60,5),rep(120,5),rep(220,5))
tau.start = 10
tau = rep(tau.start,15)
aics = NULL

# INITIALIZES STARTING RUN, TEMPERATURE SCHEDULE
set.seed(1999)
run = rbinom(m,1,.5)
run.current = run
run.vars = baseball.sub[,run.current==1]
g = lm(salary.log~.,run.vars)
run.aic = extractAIC(g)[2]
best.aic = run.aic
aics = run.aic
for(j in 2:15){tau[j] = 0.9*tau[j-1]}

## MAIN
for(j in 1:15){

	# RANDOMLY SELECTS A PREDICTOR TO ADD/REMOVE FROM THE MODEL
	# AND ACCEPTS THE NEW MODEL IF IT IS BETTER OR WITH PROBABILITY p
	for(i in 1:cooling[j]){
		pos = sample(1:m,1)
		run.step = run.current
		run.step[pos] = !run.current[pos]
		run.vars = baseball.sub[,run.step==1]
		g = lm(salary.log~.,run.vars)
		run.step.aic = extractAIC(g)[2]
		p = min(1,exp((run.aic-extractAIC(g)[2])/tau[j]))
		if(run.step.aic < run.aic){
			run.current = run.step
			run.aic = run.step.aic}
		if(rbinom(1,1,p)){
			run.current = run.step
			run.aic = run.step.aic}
		if(run.step.aic < best.aic){
			run = run.step
			best.aic = run.step.aic}
		aics = c(aics,run.aic)
	}
}

## OUTPUT
run 		# BEST LIST OF PREDICTORS FOUND
best.aic 	# AIC VALUE
aics		# VECTOR OF AIC VALUES

## PLOT OF AIC VALUES
plot(aics,ylim=c(-420,-360),type="n",ylab="AIC", xlab="Iteration")
lines(aics)

(1:2001)[aics==min(aics)]


#########################################################################
### EXAMPLE 3.5 -- GENETIC ALGORITHM
#########################################################################
# baseball.dat 	= entire data set
# baseball.sub 	= matrix of all predictors
# salary.log 	= response, log salary
# n 		= number of observations in the data set
# m 		= number of predictors in the data set
# runs 		= matrix of P individuals for a generation where each row
# 		  is a vector of the parameters included for the model
# 		  (1 = included, 0 = omitted)
# runs.next 	= matrix of P individuals for the new generation where each
# 		  row is a vector of the parameters included for the model
# 		  (1 = included, 0 = omitted)
# runs.aic 	= AIC values for the models of each generation
# P 		= size of each generation
# itr 		= number of generations to run
# m.rate 	= mutation rate
# r 		= ranks of AICs for a generation
# phi 		= fitness values for a generation
# run 		= vector of the parameters included in the best model found
# 		  (1 = included, 0 = omitted)
# best.aic 	= AIC value for the best model found
# aics 		= AIC values for the models at each step
# 		  (used for plotting)
#########################################################################

## INITIAL VALUES
baseball.dat = read.table(file.choose(),header=TRUE)
baseball.dat$freeagent = factor(baseball.dat$freeagent)
baseball.dat$arbitration = factor(baseball.dat$arbitration)
baseball.sub = baseball.dat[,-1]
salary.log = log(baseball.dat$salary)
n = length(salary.log)
m = length(baseball.sub[1,])
P = 20
itr = 100
m.rate = .01
r = matrix(0,P,1)
phi = matrix(0,P,1)
runs = matrix(0,P,m)
runs.next = matrix(0,P,m)
runs.aic = matrix(0,P,1)
aics = matrix(0,P,itr)
run = NULL
best.aic = 0
best.aic.gen = rep(0,itr)

# INITIALIZES STARTING GENERATION, FITNESS VALUES
set.seed(3219553) 
for(i in 1:P){
	runs[i,] = rbinom(m,1,.5)
	run.vars = baseball.sub[,runs[i,]==1]
	g = lm(salary.log~.,run.vars)
	runs.aic[i] = extractAIC(g)[2]
	aics[i,1] = runs.aic[i]
	if(runs.aic[i] < best.aic){
		run = runs[i,]
		best.aic = runs.aic[i]
	}
}
r = rank(-runs.aic)
phi = 2*r/(P*(P+1))
best.aic.gen[1]=best.aic

## MAIN
for(j in 1:itr-1){

	# BUILDS THE NEW GENERATION, SELECTING FIRST PARENT BASED ON
	# FITNESS AND THE SECOND PARENT AT RANDOM
	for(i in 1:10){
		parent.1 = runs[sample(1:P,1,prob=phi),]
		parent.2 = runs[sample(1:P,1),]
		pos = sample(1:(m-1),1)
		mutate = rbinom(m,1,m.rate)
		runs.next[i,] = c(parent.1[1:pos],parent.2[(pos+1):m])
		runs.next[i,] = (runs.next[i,]+mutate)%%2
		mutate = rbinom(m,1,m.rate)
		runs.next[P+1-i,] = c(parent.2[1:pos],parent.1[(pos+1):m])
		runs.next[P+1-i,] = (runs.next[P+1-i,]+mutate)%%2
	}
	runs = runs.next

	# UPDATES AIC VALUES, FITNESS VALUES FOR NEW GENERATION
	for(i in 1:P){
		run.vars = baseball.sub[,runs[i,]==1]
		g = lm(salary.log~.,run.vars)
		runs.aic[i] = extractAIC(g)[2]
		aics[i,j+1] = runs.aic[i]
		if(runs.aic[i] < best.aic){
			run = runs[i,]
			best.aic = runs.aic[i]
		}
	}
	best.aic.gen[j+1]=best.aic
	r = rank(-runs.aic)
	phi = 2*r/(P*(P+1))
}

## OUTPUT
run 		# BEST LIST OF PREDICTORS FOUND
best.aic 	# AIC VALUE

## PLOT OF AIC VALUES
plot(-aics,xlim=c(0,itr),ylim=c(50,425),type="n",ylab="Negative AIC",
	xlab="Generation",main="AIC Values For Genetic Algorithm")
for(i in 1:itr){points(rep(i,P),-aics[,i],pch=20)}


#########################################################################
### EXAMPLE 3.7 TABU SEARCH
#########################################################################
# baseball.dat 	= entire data set
# baseball.sub 	= matrix of all predictors
# salary.log 	= response, log salary
# n 		= number of observations in the data set
# m 		= number of predictors in the data set
# run 		= vector of the parameters included in the best model found
# 		  (1 = included, 0 = omitted)
# best.aic 	= AIC value for the best model found
# aics 		= AIC values for the model at each step
# 		  (used for plotting)
# itr 		= number of iterations
# tabu 		= vector containing tabu terms for each parameter
# tabu.term 	= default length of term for tabu moves
#########################################################################

## INITIAL VALUES
baseball.dat = read.table(file.choose(),header=TRUE)
baseball.dat$freeagent = factor(baseball.dat$freeagent)
baseball.dat$arbitration = factor(baseball.dat$arbitration)
baseball.sub = baseball.dat[,-1]
salary.log = log(baseball.dat$salary)
n = length(salary.log)
m = length(baseball.sub[1,])
tabu = rep(0,m)
tabu.term = 5
itr = 75
aics = rep(0,itr+1)

# INITIALIZES STARTING RUN
set.seed(139992)
run = rbinom(m,1,.5)
run.current = run
run.vars = baseball.sub[,run.current==1]
g = lm(salary.log~.,run.vars)
run.aic = extractAIC(g)[2]
best.aic = run.aic
aics[1] = run.aic

## MAIN
for(j in 1:itr){
	run.aic = 0

	# TESTS ALL MODELS IN THE 1-NEIGHBORHOOD AND CHOOSES THE BEST
	# MODEL IF THE MODEL IS NOT TABU, OTHERWISE IT SELECTS THE
	# LEAST UNFAVORABLE UNLESS THE MODEL IS THE BEST SEEN OVERALL
	for(i in 1:m){
		run.step = run.current
		run.step[i] = !run.current[i]
		run.vars = baseball.sub[,run.step==1]
		g = lm(salary.log~.,run.vars)
		run.step.aic = extractAIC(g)[2]
		if(run.step.aic < run.aic && tabu[i]==0){
		run.next = run.step
		run.aic = run.step.aic
		pos = i
	}
	if(run.step.aic < run.aic && tabu[i]!=0 &&
	run.step.aic < best.aic){
	run.next = run.step
	run.aic = run.step.aic
	pos = i
	}

	# DECREMENT TABU TERMS
	if(tabu[i]!=0){tabu[i]=tabu[i]-1}
	}
	tabu[pos] = tabu.term
	run.current = run.next
	if(run.aic < best.aic){
		best.aic = run.aic
		run = run.current
	}
	aics[j+1] = run.aic
}

## OUTPUT
run 		# BEST LIST OF PREDICTORS FOUND
best.aic 	# AIC VALUE
aics		# VECTOR OF AIC VALUES	

## PLOT OF AIC VALUES
par(mfrow=c(1,2))
plot(-aics,type="n",ylab="Negative AIC",xlab="Iteration",
	main="AIC Values For Tabu Search",ylim=c(360,420))
lines(-aics)

plot(-aics[2:itr],type="n",ylab="Negative AIC",xlab="Iteration",
	main="AIC Values For Tabu Search")
lines(-aics)

sort(aics)
(1:76)[aics==min(aics)]


#########################################################################
### END OF FILE
