import core as c 
import pandas as pd 
import base as b 
import datetime as dt 
import matplotlib.pyplot as plt 



# ds.index = ds.index.year 

def plot():
    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 6, 
        figsize = (12, 18), 
        )
    
    
    cols = ['ratio', 'vp', 'mer_perp', 'K', 
            'gr', 'gamma']
    
    limits = [
        
        ]
    for i, col in enumerate(cols):
        
        ax[i].bar(ds.index, ds[col], width = 1)
    

# ds['ratio']
# 
# df = ds.groupby(pd.Grouper(freq='M')).mean()

# df['gamma'].plot()


def simple_avg(df):

    out = {
           'gamma':[], 
           'zon':[], 
           'mer': []
           }
    for month in range(1, 13, 1):
        ds = df.resample('1M').mean()
        
        su = ds.loc[ds.index.month == month]
        
        out['gamma'].append(su['gamma'].mean())
        out['zon'].append(su['zon'].mean())
        out['mer'].append(su['mer'].mean())
        
        
    df = pd.DataFrame(out, index = range(1, 13, 1))

# df['gamma'].plot(kind = 'bar')

def seasonal_mean(df, parameter = 'gamma'):
    
    df['doy'] = df.index.day_of_year
    
    names = ['march', 'june', 'september', 'december']
    
    out_year = []
    for year in range(2013, 2023, 1):
            
        df1 = df.loc[df.index.year == year]
        
        out = {name: [] for name in names}
        
        for season in names:
            ss = c.SeasonsSplit(
                df1, season, translate = True)
            
            if parameter == 'epb':
                out[season].append(
                    ss.sel_season[parameter].sum())
            else:
                out[season].append(
                    ss.sel_season[parameter].mean())
        
        out_year.append(pd.DataFrame(out, index = [year]))
        
    return pd.concat(out_year)

PATH_GAMMA = 'database/gamma/p1_saa.txt'

df = b.load(PATH_GAMMA)

df = df.loc[(df.index.time == dt.time(22, 0)) ]

df = c.load_results()
df['K'] = df['K'] * 1e5 

ds = df.resample('1M').mean()

b.config_labels()

def plot_seasonal_count():
    
 
    names = ['epb']
    
    for i, name in enumerate(names):
        
        ds = seasonal_mean(df, name)
        
        ds.plot(
            ax= ax[i], 
            kind = 'bar', 
            legend = False
            )
        
        ax[i].set(ylabel = name)
        
   
    
    return fig 

fig, ax = plt.subplots(
       figsize = (12, 8),
       dpi = 300,
       sharex = True,
       nrows = 2
       )
   
   
plt.subplots_adjust(hspace = 0.1)

df1 = df.loc[df['kp'] <= 3]

ds = seasonal_mean(df1, parameter = 'epb')

ds.plot(
    ax= ax[0], 
    kind = 'bar', 
    legend = False
    ) 


df2 = df.loc[df['kp'] > 3]

ds = seasonal_mean(df2, parameter = 'epb')

ds.plot(
    ax= ax[1], 
    kind = 'bar', 
    legend = False
    ) 

ax[0].legend(
     bbox_to_anchor = (0.5, 1.3), 
     ncol = 4, 
     loc = 'upper center'
     )
 
ax[-1].set(xlabel = 'Years')
 
plt.xticks(rotation = 0)