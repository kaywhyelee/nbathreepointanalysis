#!/usr/bin/env python
# coding: utf-8

# The purpose of this analysis is to examine and try and determine if Steph Curry, statistically speaking, had a transformative impact on the way the NBA game is played. The dataset being used has been obtained from Kaggle (https://www.kaggle.com/datasets/wyattowalsh/basketball/data) and represents game level data from 1946 through the end of the 2022 season.

# In[1]:


## Import the packages we will use to visualize and analyze the dataframe
import pandas as pd
import datetime as dt
import numpy as np
from datetime import date
import plotly as plty
import plotly.express as px


# In[2]:


## Set the base dataframe
nbagames = pd.read_csv('game.csv')


# In[3]:


nbagames.info()
## Examine the differnt data attributes to determine which ones we will keep for the analysis.
## We will want to keep the following attributes (1) season_id (2) game_date (3) fg3m_home (4) fg3a_home (5) fg3m_away 
## (6) fg3a_away (7) season_type


# In[4]:


len(nbagames), nbagames.game_id.nunique(), nbagames['game_id'].isna().sum(),nbagames[nbagames.game_id.duplicated()].season_type.unique()


# In[161]:


nba_three_point_analysis = nbagames[['season_id','game_date','fg3a_home','fg3m_home','fg3a_away','fg3m_away','season_type']]
## We need to address the posibility of dirty or incomplete data. How many, of the attributes we have kept show up as NA values? 
## There are ~18.7k and ~13.2k NA values for attempted and made 3pointers in the dataframe (~29%)
nba_three_point_analysis.isna().sum()


# In[162]:


nba_three_point_analysis


# In[163]:


## Since we are only looking at total three pointers we do not need home and away, we just want the total, 
## we will replace NAs with 0s to enable the ability to add home and away values
nba_three_point_analysis = nba_three_point_analysis.fillna(0)
nba_three_point_analysis['total_3p_a'] = nba_three_point_analysis.fg3a_home + nba_three_point_analysis.fg3a_away
nba_three_point_analysis['total_3p_m'] = nba_three_point_analysis.fg3m_home + nba_three_point_analysis.fg3m_away
nba_three_point_analysis


# In[164]:


nba_three_point_analysis.isna().sum()


# In[165]:


## We have removed columns we do not need for this analysis
## nba_three_point_analysis.drop(columns=['fg3a_home','fg3m_home','fg3a_away','fg3m_away'],inplace=True)
nba_three_point_analysis[nba_three_point_analysis['season_type']=='Regular Season']


# In[166]:


# Step 1: Convert the column values to strings
nba_three_point_analysis['season_id_str'] = nba_three_point_analysis['season_id'].astype(str)

# Step 2: Extract the 2nd, 3rd, 4th, and 5th characters
nba_three_point_analysis['year_str'] = nba_three_point_analysis['season_id_str'].str[1:5]

# Step 3: Convert the extracted substring to a number
nba_three_point_analysis['year'] = nba_three_point_analysis['year_str'].astype(int)

# Optional Step 4: Clean up the DataFrame
nba_three_point_analysis.drop(columns=['year_str', 'season_id_str'], inplace=True)

nba_three_point_analysis


# In[167]:


## It appears there were no three pointers made or attempted until the early 80s, with some additional google searching
## the three point shot was not introduced until 1979, unfortunately this data is missing the 2012 regular season
nba_three_point_analysis['year'].unique()

nba_three_point_analysis_regularszn = nba_three_point_analysis[nba_three_point_analysis['season_type']=='Regular Season']

fig = px.bar(nba_three_point_analysis_regularszn.groupby("year")[['total_3p_a','total_3p_m']].sum().reset_index(),\
             x="year", y=["total_3p_a", "total_3p_m"], barmode="group")
fig.show()


# In[168]:


## Looks like there might be an error in the data considering that you should not have made three point shots if you have no attempted shots
## we can drop every record where the year is before 1980 for the rest of this analysis
nba_three_point_analysis_regularszn = nba_three_point_analysis_regularszn.groupby('year').sum().reset_index()

nba_three_point_analysis_regularszn[nba_three_point_analysis_regularszn['total_3p_a']==0].drop(columns='season_id')


# In[169]:


nba_three_point_analysis_regularszn[nba_three_point_analysis_regularszn['total_3p_m']==0].drop(columns='season_id')


# In[170]:


## There appear to be some issues with the recording of three point shots early on in the data and years before 1985
## should be removed for further analysis.
nba_three_point_analysis_regularszn[(nba_three_point_analysis_regularszn['total_3p_m'] > nba_three_point_analysis_regularszn['total_3p_a'])]


# In[171]:


nba_three_point_analysis_regularszn = nba_three_point_analysis_regularszn[nba_three_point_analysis_regularszn['year']>=1986]


# In[172]:


nba_three_point_analysis_regularszn


# In[173]:


new_row = {'year': 2012, 'total_3p_a': 1636*30, 'total_3p_m': 587*30}

nba_three_point_analysis_regularszn = nba_three_point_analysis_regularszn.append(new_row, ignore_index=True)

nba_three_point_analysis_regularszn


# In[174]:


nba_three_point_analysis_regularszn = nba_three_point_analysis_regularszn.sort_values(by='year')


# In[175]:


fig = px.line(nba_three_point_analysis_regularszn,x="year", y=['total_3p_a','total_3p_m'])
fig.show()
## In the regular season from 2010 to 2013 there was a large drop off in the total number of three point shots attempted and as a result made
## After 2013 through 2021, however (ignoring COVID in 2020) 


# In[176]:


nba_three_point_analysis_regularszn.dropna()


# In[177]:


## The largest year over year percentage changes in 3 pointers attempted all occured in the 90s (whether positive or negative)
## Since then, the year over year changes hvae not been that different. This is to say, of course, a 3 point shot is worth more than a 2 point
## shot so attempting more is a basic strategy to work into the game, assuming you have players who can shoot them efficiently (this is perhaps
## another more important stat to look at - get there in a minute)
nba_three_point_analysis_regularszn['3ptAtt_PctChng'] = nba_three_point_analysis_regularszn['total_3p_a'].pct_change()*100
nba_three_point_analysis_regularszn['3ptMade_PctChng'] = nba_three_point_analysis_regularszn['total_3p_m'].pct_change()*100
nba_three_point_analysis_regularszn[['year','3ptAtt_PctChng']].dropna()
nba_three_point_analysis_regularszn[['year','3ptMade_PctChng']].dropna()


fig = px.line(nba_three_point_analysis_regularszn[['year','3ptAtt_PctChng','3ptMade_PctChng']].dropna().sort_values(by='year'),\
              x='year', y=['3ptAtt_PctChng','3ptMade_PctChng'])
fig.update_layout(title="Percent Change in Total 3 Point Shots Attempted Y-o-Y", yaxis_title = 'Pct Change', xaxis_title="Season")
fig.show()


# In[178]:


## Both attempts and makes appear to be positively skewed on a game by game basis. The number of three-pointers made is heavily skewed positive
## relative to attempted shots. If Curry did transform the game we might expect to see a significant difference in the number 
## of three pointers attempted each game. If it is a league wide impact then it would not just be a change in his own team's
## games having higher 3 pointers attempted but all teams would be attempting more of these shots, thus for now we can 
## put aside the made three point shots
hist = nba_three_point_analysis[(nba_three_point_analysis['season_type']=='Regular Season') & (nba_three_point_analysis['year']>=1986)]
fig = px.histogram(hist, x='total_3p_a')
fig.show()
fig = px.histogram(hist, x='total_3p_m')
fig.show()


# In[179]:


import math
fig = px.histogram(hist, x=np.sqrt(hist['total_3p_a']))
fig.show()


# In[180]:


## Shooting more 3 pointers (attempts) appears to be much more a trend that was previously building
## and possibly just accelerating through time as players become better at these shots (again - more on this)
fig = px.line(pd.DataFrame(nba_three_point_analysis[(nba_three_point_analysis['season_type']=='Regular Season') & \
                                                    (nba_three_point_analysis['year']>=1986)].groupby('year')['total_3p_a'].agg(['median','mean']))\
              .reset_index(),x='year', y = ['mean', 'median'])
fig.update_layout(title="Average and Median 3 Point Attempts per Game", yaxis_title = 'Attempts per Game', xaxis_title="Season")

fig.show()


# In[181]:


stats.ttest_ind(nba_three_point_analysis[\
                         (nba_three_point_analysis['year']==2021)\
                         &(nba_three_point_analysis['season_type']=='Regular Season')]['total_3p_a'],
nba_three_point_analysis[\
                         (nba_three_point_analysis['year']==2022)\
                         &(nba_three_point_analysis['season_type']=='Regular Season')]['total_3p_a'],alternative='less')


# In[182]:


from scipy import stats

for yr in range(1987,2023):
    
    sample2 = nba_three_point_analysis[\
                         (nba_three_point_analysis['year']==yr)\
                         &(nba_three_point_analysis['season_type']=='Regular Season')]['total_3p_a']
    
    sample1 = nba_three_point_analysis[\
                         (nba_three_point_analysis['year']==(yr-1))\
                        & (nba_three_point_analysis['season_type']=='Regular Season')]['total_3p_a']
    
    t_stat, p_value = stats.ttest_ind(sample1, sample2, alternative="less")

    if p_value >0.05:
        print(f'{yr} T-Stat: {round(t_stat,2)} and P-Value: {p_value:.3e}')
    else:
        continue


# In[183]:


from scipy import stats

for yr in range(1987,2022):
    
    sample2 = nba_three_point_analysis[\
                         (nba_three_point_analysis['year']==yr)\
                         &(nba_three_point_analysis['season_type']=='Regular Season')]['total_3p_a']
    
    sample1 = nba_three_point_analysis[\
                         (nba_three_point_analysis['year']<yr)\
                         & (nba_three_point_analysis['year']>=1986)\
                        & (nba_three_point_analysis['season_type']=='Regular Season')]['total_3p_a']
    
    t_stat, p_value = stats.ttest_ind(sample1, sample2, alternative="less")

    print(f'{yr} T-Stat: {round(t_stat,2)} and P-Value: {p_value:.3e}')


# In[184]:


nba_three_point_analysis.fillna(0)
nba_three_point_analysis['3ptpct'] = nba_three_point_analysis.total_3p_m / nba_three_point_analysis.total_3p_a
nba_three_point_analysis

nba_three_point_analysis[nba_three_point_analysis['3ptpct'].isna()]['year'].unique()


# In[185]:


nba_three_point_analysis_regularszn['3ptpct'] = nba_three_point_analysis_regularszn.total_3p_m / nba_three_point_analysis_regularszn.total_3p_a
nba_three_point_analysis_regularszn


# In[186]:


fig = px.line(nba_three_point_analysis_regularszn, x = 'year', y=nba_three_point_analysis_regularszn['3ptpct']*100)

fig.update_layout(title='League Total 3-pt Pct by Season',
                   xaxis_title='Season',
                   yaxis_title='3 point shooting pct')


# In[187]:


nba_three_point_analysis[(nba_three_point_analysis['year']>=1986) &\
                        (nba_three_point_analysis['season_type']=='Regular Season')]


for yr in range(1992,2022):
    
    sample2 = nba_three_point_analysis[\
                         (nba_three_point_analysis['year']==yr)\
                         &(nba_three_point_analysis['season_type']=='Regular Season')]['3ptpct']
    
    sample1 = nba_three_point_analysis[\
                         (nba_three_point_analysis['year']<yr)\
                         & (nba_three_point_analysis['year']>=1991)\
                        & (nba_three_point_analysis['season_type']>='Regular Season')]['3ptpct']
    
    t_stat, p_value = stats.ttest_ind(sample1, sample2, alternative="less")

    print(f'{yr} T-Stat: {round(t_stat,2)} and P-Value: {p_value:.3e}')


# In[209]:


## the 1998 season was only 50 games, to "normalize" it we have divided by 50 and multiplied by 82 (a full season)
## also adjusted the 2011 season to divided by 66 and multiply by 82 since only 66 games we played that seaons
nba_three_point_analysis_regularszn.iloc[11:13,6:8], nba_three_point_analysis_regularszn.iloc[24:26,6:8]


# In[189]:


nba_three_point_analysis_regularszn_adj = nba_three_point_analysis_regularszn.copy()
nba_three_point_analysis_regularszn_adj.iloc[12:13,6] = nba_three_point_analysis_regularszn_adj.iloc[11:12,6]/50*82
nba_three_point_analysis_regularszn_adj.iloc[12:13,7] = nba_three_point_analysis_regularszn_adj.iloc[11:12,7]/50*82
nba_three_point_analysis_regularszn_adj.iloc[25:26,6] = nba_three_point_analysis_regularszn_adj.iloc[25:26,6]/66*82
nba_three_point_analysis_regularszn_adj.iloc[25:26,7] = nba_three_point_analysis_regularszn_adj.iloc[25:26,7]/66*82
nba_three_point_analysis_regularszn_adj ## adjusted the 1998 and the 2011 (66 game season) numbers in the same manner


# In[190]:


nba_three_point_analysis_regularszn


# In[191]:


nba_three_point_analysis_regularszn_adj['3ptAtt_PctChng'] = nba_three_point_analysis_regularszn_adj['total_3p_a'].pct_change()*100
nba_three_point_analysis_regularszn_adj['3ptMade_PctChng'] = nba_three_point_analysis_regularszn_adj['total_3p_m'].pct_change()*100
nba_three_point_analysis_regularszn_adj[['year','3ptAtt_PctChng']].dropna()
nba_three_point_analysis_regularszn_adj[['year','3ptMade_PctChng']].dropna()


fig = px.line(nba_three_point_analysis_regularszn_adj[['year','3ptAtt_PctChng','3ptMade_PctChng']].dropna().sort_values(by='year'),\
              x='year', y=['3ptAtt_PctChng','3ptMade_PctChng'])
fig.update_layout(title="Percent Change in Total (Adjusted) 3 Point Shots Attempted Y-o-Y", yaxis_title = 'Pct Change', xaxis_title="Season")
fig.show()


# In[159]:


nba_three_point_analysis_regularszn_adj

