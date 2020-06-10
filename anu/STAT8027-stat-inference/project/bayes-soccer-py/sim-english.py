import sys
import math
import warnings
warnings.filterwarnings('ignore')
import pymc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image, HTML
from matplotlib.animation import FuncAnimation

df = pd.read_csv('E0-2015.csv', sep=',')
df = df[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
df = df.rename(index=str,columns={"HomeTeam":"home", "AwayTeam":"away", "FTHG":"home_score", "FTAG":"away_score"})
df.head()

teams = df.home.unique()
teams = pd.DataFrame(teams, columns=['team'])
teams['i'] = teams.index
teams.head()


df = pd.merge(df, teams, left_on='home', right_on='team', how='left')
df = df.rename(columns = {'i': 'i_home'}).drop('team', 1)
df = pd.merge(df, teams, left_on='away', right_on='team', how='left')
df = df.rename(columns = {'i': 'i_away'}).drop('team', 1)
df.head()

# extract data into arrays for pymc

observed_home_goals = df.home_score.values
observed_away_goals = df.away_score.values
home_team = df.i_home.values
away_team = df.i_away.values
num_teams = len(df.i_home.unique())
num_games = len(home_team)

g = df.groupby('i_away')
att_starting_points = np.log(g.away_score.mean())
g = df.groupby('i_home')
def_starting_points = np.log(g.home_score.mean())

# hyperpriors
home = pymc.Normal('home', 0, .0001, value=0)
tau_att = pymc.Gamma('tau_att', .1, .1, value=10)
tau_def = pymc.Gamma('tau_def', .1, .1, value=10)
# intercept = pymc.Normal('intercept', 0, .0001, value=0)

# team-specific parameters
atts_star = pymc.Normal("atts_star", 
                        mu=0, 
                        tau=tau_att, 
                        size=num_teams, 
                        value=att_starting_points.values)
defs_star = pymc.Normal("defs_star", 
                        mu=0, 
                        tau=tau_def, 
                        size=num_teams, 
                        value=def_starting_points.values) 


# trick to code the sum to zero contraint
@pymc.deterministic
def atts(atts_star=atts_star):
    atts = atts_star.copy()
    atts = atts - np.mean(atts_star)
    return atts


@pymc.deterministic
def defs(defs_star=defs_star):
    defs = defs_star.copy()
    defs = defs - np.mean(defs_star)
    return defs


@pymc.deterministic
def home_theta(home_team=home_team, 
               away_team=away_team, 
               home=home, 
               atts=atts, 
               defs=defs):
               # defs=defs, 
               # intercept=intercept): 

    # return np.exp(intercept + 
    return np.exp( 
                  home + 
                  atts[home_team] + 
                  defs[away_team])


@pymc.deterministic
def away_theta(home_team=home_team, 
               away_team=away_team, 
               home=home, 
               atts=atts, 
               # defs=defs, 
               # intercept=intercept): 
               defs=defs):
    # return np.exp(intercept +
    return np.exp( 
                  atts[away_team] + 
                  defs[home_team])   


home_goals = pymc.Poisson('home_goals', 
                          mu=home_theta, 
                          value=observed_home_goals, 
                          observed=True)
away_goals = pymc.Poisson('away_goals', 
                          mu=away_theta, 
                          value=observed_away_goals, 
                          observed=True)

# mcmc = pymc.MCMC([home, intercept, tau_att, tau_def, 
#                   home_theta, away_theta, 
#                   atts_star, defs_star, atts, defs, 
#                   home_goals, away_goals])
mcmc = pymc.MCMC([home, tau_att, tau_def, 
                  home_theta, away_theta, 
                  atts_star, defs_star, atts, defs, 
                  home_goals, away_goals])
map_ = pymc.MAP(mcmc)
map_.fit()
mcmc.sample(200000, 40000, 20)

# diagnostics
pymc.Matplot.plot(home)
# pymc.Matplot.plot(intercept)
pymc.Matplot.plot(tau_att)
pymc.Matplot.plot(tau_def)

# pymc.Matplot.plot(atts)

# Highest Posterior Density intervals for the attack parameters

df_hpd = pd.DataFrame(np.transpose(atts.stats()['95% HPD interval']), 
                      columns=['hpd_low', 'hpd_high'], 
                      index=teams.team.values)
df_median = pd.DataFrame(atts.stats()['quantiles'][50], 
                         columns=['hpd_median'], 
                         index=teams.team.values)
df_hpd = df_hpd.join(df_median)
df_hpd['relative_lower'] = df_hpd.hpd_median - df_hpd.hpd_low
df_hpd['relative_upper'] = df_hpd.hpd_high - df_hpd.hpd_median
df_hpd = df_hpd.sort_index(by='hpd_median')
df_hpd = df_hpd.reset_index()
df_hpd['x'] = df_hpd.index + .5


fig, axs = plt.subplots(figsize=(10,7))
axs.errorbar(df_hpd.x, df_hpd.hpd_median, 
             yerr=(df_hpd[['relative_lower', 'relative_upper']].values).T, 
             fmt='o')
axs.set_title('HPD of Attack Strength, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Posterior Attack Strength')
_= axs.set_xticks(df_hpd.index + .5)
_= axs.set_xticklabels(df_hpd['index'].values, rotation=45)
fig.savefig('E0-2015-image/95hpd-att.png')

# VISUALIZATION of average defense effect vs average attack effect

df_observed = pd.read_csv('E0_2015_results.csv')
df_observed.loc[df_observed.QR.isnull(), 'QR'] = ''

df_avg = pd.DataFrame({'avg_att': atts.stats()['mean'], 'avg_def': defs.stats()['mean']},
    index=teams.team.values)
df_avg = pd.merge(df_avg, df_observed, left_index=True, right_on='team', how='left')

fig, ax = plt.subplots(figsize=(8,6))
for outcome in ['champs_league', 'relegation', 'europa_league', '']:
    ax.plot(df_avg.avg_att[df_avg.QR == outcome],
        df_avg.avg_def[df_avg.QR == outcome], 'o', label=outcome)

for label, x, y, in zip(df_avg.team.values, df_avg.avg_att.values, df_avg.avg_def.values):
    ax.annotate(label, xy=(x,y), xytext=(-5,5), textcoords='offset points')
ax.set_title('Attack vs Defense avg effect: 15-16 Premier League')
ax.set_xlabel('Avg attack effect')
ax.set_ylabel('Avg defense effect')
ax.legend()
fig.savefig('E0-2015-image/att-vs-def.png')


# simulations
def simulate_season():
    num_samples = atts.trace().shape[0]
    draw = np.random.randint(0, num_samples)
    atts_draw = pd.DataFrame({'att': atts.trace()[draw, :], })
    defs_draw = pd.DataFrame({'def': defs.trace()[draw, :], })
    home_draw = home.trace()[draw]
    # intercept_draw = intercept.trace()[draw]
    season = df.copy()
    season = pd.merge(season, atts_draw, left_on='i_home', right_index=True)
    season = pd.merge(season, defs_draw, left_on='i_home', right_index=True)
    season = season.rename(columns={'att': 'att_home', 'def': 'def_home'})
    season = pd.merge(season, atts_draw, left_on='i_away', right_index=True)
    season = pd.merge(season, defs_draw, left_on='i_away', right_index=True)
    season = season.rename(columns={'att': 'att_away', 'def': 'def_away'})
    season['home'] = home_draw
    # season['intercept'] = intercept_draw
    # season['home_theta'] = season.apply(lambda x: math.exp(x['intercept'] +
    season['home_theta'] = season.apply(lambda x: math.exp(
                                                           x['home'] +
                                                           x['att_home'] +
                                                           x['def_away']),
                                        axis=1)
    # season['away_theta'] = season.apply(lambda x: math.exp(x['intercept'] +
    season['away_theta'] = season.apply(lambda x: math.exp(
                                                           x['att_away'] +
                                                           x['def_home']),
                                        axis=1)
    season['home_goals'] = season.apply(
        lambda x: np.random.poisson(x['home_theta']), axis=1)
    season['away_goals'] = season.apply(
        lambda x: np.random.poisson(x['away_theta']), axis=1)
    season['home_outcome'] = season.apply(
        lambda x: 'win' if x['home_goals'] > x['away_goals'] else
        'loss' if x['home_goals'] < x['away_goals'] else 'draw', axis=1)
    season['away_outcome'] = season.apply(
        lambda x: 'win' if x['home_goals'] < x['away_goals'] else
        'loss' if x['home_goals'] > x['away_goals'] else 'draw', axis=1)
    season = season.join(pd.get_dummies(season.home_outcome, prefix='home'))
    season = season.join(pd.get_dummies(season.away_outcome, prefix='away'))
    return season


def create_season_table(season):
    """
    Using a season dataframe output by simulate_season(), create a summary
    dataframe with wins, losses, goals for, etc.

    """
    g = season.groupby('i_home')
    home = pd.DataFrame({'home_goals': g.home_goals.sum(),
                         'home_goals_against': g.away_goals.sum(),
                         'home_wins': g.home_win.sum(),
                         'home_draws': g.home_draw.sum(),
                         'home_losses': g.home_loss.sum()
                         })
    g = season.groupby('i_away')
    away = pd.DataFrame({'away_goals': g.away_goals.sum(),
                         'away_goals_against': g.home_goals.sum(),
                         'away_wins': g.away_win.sum(),
                         'away_draws': g.away_draw.sum(),
                         'away_losses': g.away_loss.sum()
                         })
    df = home.join(away)
    df['wins'] = df.home_wins + df.away_wins
    df['draws'] = df.home_draws + df.away_draws
    df['losses'] = df.home_losses + df.away_losses
    df['points'] = df.wins * 3 + df.draws
    df['gf'] = df.home_goals + df.away_goals
    df['ga'] = df.home_goals_against + df.away_goals_against
    df['gd'] = df.gf - df.ga
    df = pd.merge(teams, df, left_on='i', right_index=True)
    df = df.sort_index(by='points', ascending=False)
    df = df.reset_index()
    df['position'] = df.index + 1
    df['champion'] = (df.position == 1).astype(int)
    df['qualified_for_CL'] = (df.position < 5).astype(int)
    df['relegated'] = (df.position > 17).astype(int)
    return df


def simulate_seasons(n=100):
    dfs = []
    for i in range(n):
        s = simulate_season()
        t = create_season_table(s)
        t['iteration'] = i
        dfs.append(t)
    return pd.concat(dfs, ignore_index=True)

# print(create_season_table(simulate_season()))
simuls = simulate_seasons(1000)

fig, ax = plt.subplots()
ax = simuls.points[simuls.team == 'Leicester'].hist(figsize=(7,5))
median = simuls.points[simuls.team == 'Leicester'].median()
ax.set_title('Leicester City: 2015-16 points, 1000 simulations')
ax.plot([median, median], ax.get_ylim())
plt.annotate('Median: %s' % median, xy=(median + 1, ax.get_ylim()[1]-10))
fig.savefig('E0-2015-image/med-pts.png')

fig, ax = plt.subplots()
ax = simuls.gf[simuls.team == 'Leicester'].hist(figsize=(7,5))
median = simuls.gf[simuls.team == 'Leicester'].median()
ax.set_title('Leicester City: 2015-16 goals for, 1000 simulations')
ax.plot([median, median], ax.get_ylim())
plt.annotate('Median: %s' % median, xy=(median + 1, ax.get_ylim()[1]-10))
fig.savefig('E0-2015-image/med-gf.png')

g = simuls.groupby('team')
season_hdis = pd.DataFrame({'points_lower': g.points.quantile(.05),
                            'points_upper': g.points.quantile(.95),
                            'goals_for_lower': g.gf.quantile(.05),
                            'goals_for_median': g.gf.median(),
                            'goals_for_upper': g.gf.quantile(.95),
                            'goals_against_lower': g.ga.quantile(.05),
                            'goals_against_upper': g.ga.quantile(.95),
                            })
season_hdis = pd.merge(season_hdis, df_observed, left_index=True, right_on='team')
column_order = ['team', 'points_lower', 'Pts', 'points_upper',
                'goals_for_lower', 'GF', 'goals_for_median', 'goals_for_upper',
                'goals_against_lower', 'GA', 'goals_against_upper',]
season_hdis = season_hdis[column_order]
season_hdis['relative_goals_upper'] = season_hdis.goals_for_upper - season_hdis.goals_for_median
season_hdis['relative_goals_lower'] = season_hdis.goals_for_median - season_hdis.goals_for_lower
season_hdis = season_hdis.sort_index(by='GF')
season_hdis = season_hdis.reset_index()
season_hdis['x'] = season_hdis.index + .5
season_hdis

fig, axs = plt.subplots(figsize=(10,7))
axs.scatter(season_hdis.x, season_hdis.GF, c=sns.palettes.color_palette()[4], zorder = 10, label='Actual Goals For')
axs.errorbar(season_hdis.x, season_hdis.goals_for_median,
             yerr=(season_hdis[['relative_goals_lower', 'relative_goals_upper']].values).T,
             fmt='s', c=sns.palettes.color_palette()[5], label='Simulations')
axs.set_title('Actual Goals For, and 90% Interval from Simulations, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Goals Scored')
axs.set_xlim(0, 20)
axs.legend()
_= axs.set_xticks(season_hdis.index + .5)
_= axs.set_xticklabels(season_hdis['team'].values, rotation=45)
fig.savefig('E0-2015-image/90CI-gf.png')


