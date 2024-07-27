import core as c 
import pandas as pd 
import base as b 
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import numpy as np 
import datetime as dt 

PATH_GAMMA = 'database/gamma/p1_saa.txt'

b.config_labels(blue = False, fontsize = 30)


names = ['march',  'september', 'december']

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


def sel_season(df, season):
    
    if season == 'march':
        num = [3, 4]
    elif season == 'september':
        num = [9, 10]
    else:
        num = [12, 11]
        
        
    return df.loc[(df.index.month == num[0]) |
           (df.index.month == num[1])]


def run_by_season(df, year, parameter = 'gamma'):
    df['doy'] = df.index.day_of_year
    
    
    out = {name: [] for name in names}
    
    for season in names:
        ss = c.SeasonsSplit(
            df, season, translate = True
            )
        
        
        ss = sel_season(df, season)
        
        if parameter == 'epb':
            sel_s = ss[parameter]
            
            percent = sel_s.sum() #/ len(sel_s) * 100
            # print(percent)
            out[season].append(percent)
        else:
            sel_s = ss[parameter]
            out[season].append(sel_s.mean())
    # print(out)
    return pd.DataFrame(out, index = [year])
     
def seasonal_by_year(df, parameter = 'gamma'):
    
    out_year = []
    for year in range(2013, 2023, 1):
            
        df1 = df.loc[df.index.year == year]
        ds = run_by_season(
            df1, year, parameter)
        
        if parameter == 'epb':
            total = ds.sum(axis = 1).item()
            ds = (ds / total) * 100
        out_year.append(ds)
        
    return pd.concat(out_year)

def plot_epbs_rate(ax):
    
    df = pb.sel_typing(
         b.load('events_class2'), 
         typing = 'sunset', 
         indexes = True, 
         year = 2022)
    
    df = df.loc[df['dst'] >= -30]
    
    df = df.rename(columns = {-50: 'epb'})
    
    ds = seasonal_by_year(df, parameter = 'epb')
    
    for offset, col in enumerate(names):
       
        width = 0.2  # the width of the bars
        ax.bar(ds.index + (width * offset),
               ds[col], width, label=col)
    
    ds['eq_diff'] = ds['september']-  ds['march']  
    
    ax1 = ax.twinx()
    
    ax1.plot(ds.index, ds['eq_diff'], 
             lw = 1.5, markersize = 10, marker = 's')
    ax1.axhline(0, linestyle = '--')
    ax1.set(ylim = [-40, 40], 
            ylabel = 'Diferença equinócial (\%)')
    ax.set(
        ylim = [0, 100],
        ylabel = 'Taxa de ocorrência (\%)'
        )
    
   
    return None
    
def plot_gamma(ax):
    df = c.load_results()
    
    df = df.loc[df['dst'] >= -30]
    
    df = df.loc[df.index.year < 2023]
    
    ds = seasonal_by_year(df, parameter = 'gamma')
    
    for offset, col in enumerate(names):
        
        width = 0.2  # the width of the bars
        ax.bar(ds.index + (width * offset),
               ds[col], width, label=col)
    
    # plt.xticks(rotation = 0)
    
    ax.set(
        xlim = [ds.index[0] - 0.5, ds.index[-1] + 1],
        xticks = np.arange(2013, 2023, 1),
        ylim = [0, 3],
        xlabel = 'Anos', 
        ylabel = '$\gamma_{RT}~(10^{-3}~s^{-1})$'
            )
    
    return None

def plot_annualy_quiet_time():
    fig, ax = plt.subplots(
        figsize = (18, 12),
        nrows = 2,
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    plot_epbs_rate(ax[0])
    plot_gamma(ax[1])
    
    names1 = ['Março',  'Setembro', 'Dezembro']
  
    ax[0].legend(
         names1,
         ncol = 5, 
         bbox_to_anchor = (.5, 1.2), 
         loc = "upper center", 
         columnspacing = 0.3
         )
    plt.xticks(rotation = 0)
    
    b.plot_letters(
        ax, 
        y = 0.85, 
        x = 0.03, fontsize = 40)

    return fig


  
   
fig = plot_annualy_quiet_time()
  
FigureName = 'annual_quiet_time'
      
fig.savefig(
      b.LATEX(FigureName, folder = 'bars'),
      dpi = 400
      )

