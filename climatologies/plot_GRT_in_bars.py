import core as c 
import pandas as pd 
import base as b 
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import numpy as np 
import datetime as dt 

def declination(doy):
    return  np.sin(-np.radians(360 / 365 * (275 + doy)))
names = ['march', 'june', 'september', 'december']

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
                df1, year, parameter)
            )
        
    return pd.concat(out_year)

PATH_GAMMA = 'database/gamma/p1_saa.txt'



        
        
b.config_labels(blue = False)



def plot_annualy_quiet_time():
    fig, ax = plt.subplots(
        figsize = (16, 10),
        nrows = 2,
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    plt.subplots_adjust(hspace=0.1)
    df = pb.sel_typing(
        b.load('events_class2'), 
        typing = 'sunset', 
        indexes = True, 
        year = 2023)
    
    
    df = df.loc[df['dst'] >= -30]
    
    df = df.rename(columns = {-50: 'epb'})
    
    
    ds = seasonal_by_year(df, parameter = 'epb')
    
    
    ds.plot(ax = ax[0], kind = 'bar', legend = False)
    names1 = ['Março', 'Junho', 'Setembro', 'Dezembro']
    t = [f'{name} ({vl})' for name, vl in 
          zip(names1, ds.sum().values)]
     
    ax[0].legend(
         t,
         ncol = 5, 
         bbox_to_anchor = (.5, 1.2), 
         loc = "upper center", 
         columnspacing = 0.6
         )
    
    
    df = c.load_results()
    
    df = df.loc[df['dst'] >= -30]
    
    ds = seasonal_by_year(df, parameter = 'gamma')
    
    ds.plot(ax = ax[1], kind = 'bar', legend = False)
    
    plt.xticks(rotation = 0)
    
    ax[1].set(
        ylim = [0, 3],
        xlabel = 'Anos', 
        ylabel = '$\gamma_{RT}~(10^{-3}~s^{-1})$'
        )
    
    ax[0].set(
        ylim = [0, 100],
        ylabel = 'Número de eventos'
        )
    

    b.plot_letters(ax, y = 0.85, x = 0.03)
    
    
      
    FigureName = 'annual_quiet_time'
      
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'bars'),
    #       dpi = 400
    #       )
    
    return fig