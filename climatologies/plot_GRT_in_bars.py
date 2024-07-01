import core as c 
import pandas as pd 
import base as b 
import datetime as dt 
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 



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
        
        
    return pd.DataFrame(out, index = range(1, 13, 1))

def run_by_season(df, year, parameter = 'gamma'):
    df['doy'] = df.index.day_of_year
    
    names = ['march', 'june', 'september', 'december']
    out = {name: [] for name in names}
    
    for season in names:
        ss = c.SeasonsSplit(
            df, season, translate = True)
        
        if parameter == 'epb':
            out[season].append(
                ss.sel_season[parameter].sum())
        else:
            out[season].append(
                ss.sel_season[parameter].mean())
    return pd.DataFrame(out, index = [year])
     
def seasonal_by_year(df, parameter = 'gamma'):
    
    

    out_year = []
    for year in range(2013, 2024, 1):
            
        df1 = df.loc[df.index.year == year]
        
        out_year.append(
            run_by_season(
                df1, year, parameter = 'gamma')
            )
        
    return pd.concat(out_year)

PATH_GAMMA = 'database/gamma/p1_saa.txt'

# df = b.load(PATH_GAMMA)

# df = df.loc[(df.index.time == dt.time(22, 0)) ]

# df = c.load_results()
# df['K'] = df['K'] * 1e5 

# ds = df.resample('1M').mean()



def plot_seasonal_count(ds):
    
    b.config_labels()
    
    fig, ax = plt.subplots(
                figsize = (12, 8),
                dpi = 300,
                sharex = True,
                nrows = 2
                )
            
    plt.subplots_adjust(hspace = 0.1)
      
    ds = seasonal_mean(ds, parameter = 'epb')
   
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
        
   
    return fig 

df = pb.sel_typing(
    b.load('events_class2'), 
    typing = 'sunset', indexes = True)

ds = df.loc[df['dst'] >= -30]

# ds = df.loc[df['kp'] <= 3]

ds = ds.rename(columns = {-50: 'epb'})

year = 'min'

run_by_season(df, year, parameter = 'gamma')