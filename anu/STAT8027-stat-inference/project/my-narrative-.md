- data: [jokecamp/FootballData](https://github.com/jokecamp/FootballData/tree/master/football-data.co.uk) (raw data), wikipedia page (result table)
- tool: `pymc`
- setup for mcmc:
    - not specified
    - tried 200,000 iterations, 40,000 burn-in and 20 thinning interval (autocorrelation issue)
    - simplification in the model that assuming both mu attack and mu def follow a zero-mean normal.

## replication - 07-08 Serie A data

**diagnostics**

- diagnostics (- autocorrelation? 90% HDI (zero included)?)
    - home court effect
    - att mu and tau
    - def mu and tau
    - skipped diagnostics of att and def

- average def vs average attack

top teams with + att and - def (although counter-intuitive)

milan better att better def but lower ranking ;)

this is just the posterior mean, we can take a further look at highest posterior denstity interval for att

though not very obvious, some team in the middle tend to have similar HPD intervals. and the top 4 teams stand out. and this suggests the possbility of shrinkage.

next, we are going to simulate for 1 season and compare the results with real data

not very accurate right?

maybe this results are  just by chance, what about simulation for 1000 times?

still, actual goal they scored are higher than the simulated results
on the other hand, overestimate the goal for in bottom teams

this could be caused by our previous simplification in priors. 

just for fun, we 

> There's nothing inherently good or bad about shrinkage in hierarchical models. Shrinkage is just the mathematical consequence of the model choice. Just as you can choose to model a trend with a line or a quadratic or an exponential, you choose to model data with various hierarchies of parameters. We choose a model to achieve both descriptive adequacy and theoretical meaningfulness. If a particular choice of hierarchical model seems to produce too much shrinkage in some of the parameters, it means that somehow the hierarchy did not capture your prior knowledge because the posterior seems to violate your prior knowledge in ways unjustifiable from the data.
> Hierarchical models are supposed to express prior knowledge about how subsets of data are related. If the various subsets can truly be thought of as representing a higher level, then it makes perfect sense to put the subsets under a hierarchy and use all the the subsets to mutually inform the higher level and simultaneously constrain the lower-level estimates. The higher level estimate essentially constitutes a prior for each of the lower-level parameters.

- on premier league 2015-2016 when the leichester city won the title what a miracle!
- basically we did not change anything except the data but there is something extra i need to point out
- i know comparing different teams from differ years can cause some unhappiness especially among diehard sports fans, but we are trying to understand the football playing style from these data
- ok teams, mediocre attack and mediocre defense, survive the relegation, but you if  have bad D, you are in danger. best team have pretty good attack and defense. but for those team who go to europa league in the end, their playing style are pretty different: manUTd is good at defense but really bad at offence, liverpool and west ham are good at attacking style,  southampton is balanced.
- but if you take a look again at serie A data about ten years ago. you wil find out that most team are more densive-oriented, aggressive teams are so rare. only Inter in the bottom right corner might be the only one that count. but we cannot say those teams from Serie A ten years ago are worse than english teams nowadays. You know, time flies, lots of things changed in the past 10 years. the philosophy of football is different, attacking style is more popular, and counter-attack is considered as conservative.
- anyways, that's what we all have done.