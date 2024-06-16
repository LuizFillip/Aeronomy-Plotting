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
            ss = c.SeasonsSplit(df1, season, translate = True)
                
            out[season].append(ss.sel_season[parameter].mean())
        
        out_year.append(pd.DataFrame(out, index = [year]))
        
    return pd.concat(out_year)

PATH_GAMMA = 'database/gamma/p1_saa.txt'

df = b.load(PATH_GAMMA)

df = df.loc[(df.index.time == dt.time(22, 0)) ]

df = c.load_results()
df['K'] = df['K'] * 1e5 

ds = df.resample('1M').mean()
ds = seasonal_mean(df)
ds.plot(kind = 'bar') 
    