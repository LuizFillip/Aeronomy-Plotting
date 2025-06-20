import core as c 
import pandas as pd 
import base as b 
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import numpy as np 


PATH_GAMMA = 'database/gamma/p1_saa.txt'

names = ['march',  'september', 'december']

def mean_compose(ds, direction = 'zonal'):
    
 
    df1 = pd.pivot_table(
        ds, 
        values = direction, 
        index = 'time', 
        columns = 'day')

    data  = {
        'mean': df1.mean(axis = 1), 
        'std': df1.std(axis = 1), 
        }
    
    df = pd.DataFrame(data, index = df1.index)

    # ref = dt.datetime(2014, 1, 1)
    # df.index = b.new_index_by_ref(ref, df.index)
    
    return df 

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
        
        
    return df.loc[
        (df.index.month == num[0]) |
        (df.index.month == num[1])]


def run_by_season(df, year, parameter = 'gamma'):
    df['doy'] = df.index.day_of_year
    
    
    out = {name: [] for name in names}
    
    for season in names:
        # ss = c.SeasonsSplit(
        #     df, season, translate = True
        #     )
        
        
        ss = sel_season(df, season)
        
        if parameter == 'epb':
            sel_s = ss[parameter]
            
            percent = sel_s.sum() / len(sel_s) * 100
           
            out[season].append(percent)
        else:
            sel_s = ss[parameter]
            out[season].append(sel_s.mean())
   
    return pd.DataFrame(out, index = [year])
     
def seasonal_by_year(df, parameter = 'gamma'):
    
    out_year = []
    for year in range(2013, 2023, 1):
            
        df1 = df.loc[df.index.year == year]
        ds = run_by_season(
            df1, year, parameter)
        
        out_year.append(ds)
        
    return pd.concat(out_year)

def plot_equinox_difference(ax, ds):
    
    ds['eq_diff'] = 100 *(
        ds['september']- ds['march']) / ds['september']
    
    ax1 = ax.twinx()
    
    ax1.plot(
        ds.index, 
        ds['eq_diff'], 
        color = 'red',
        lw = 1.5, 
        markersize = 10, marker = 's')
    
    ax1.axhline(0, linestyle = '--')
    
    ax1.set(
        ylim = [-60, 60], 
        yticks = np.arange(-60, 80, 20)
        )
    
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    return ax1

def plot_epbs_rate(ax, translate = True):
    
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.3, 
        storm = 'quiet'
        )

    df = p.sel_type('sunset')

    # df = df.rename(columns = {-50: 'epb'})
    
    ds = seasonal_by_year(df, parameter = 'epb')

    for offset, col in enumerate(names):
       
        width = 0.2  
        ax.bar(ds.index + (width * offset),
               ds[col], width, label=col)
    
    if translate: 
        ylabel = 'Rate of occurrence (\%)'
    else:
        ylabel = 'Taxa de \nocorrência (\%)'
        
    ax.set(
        ylim = [0, 120],
        ylabel = ylabel
        )
    plot_equinox_difference(ax, ds)
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
        
    ax.set(
        xlim = [ds.index[0] - 0.5, ds.index[-1] + 1],
        xticks = np.arange(2013, 2023, 1),
        ylim = [0, 3],
        
        ylabel = '$\gamma_{RT}~(10^{-3}~s^{-1})$'
            )
    
    plot_equinox_difference(ax, ds)
    return None


def plot_vp(ax, translate = False):
    df = c.load_results()
    
    df = df.loc[df['dst'] > -30]
    
    df = df.loc[df.index.year < 2023]
    
    ds = seasonal_by_year(df, parameter = 'vp')
    
    ds['eq_diff'] = 100 *(ds['september']- ds['march']) / ds['september'] 
    
    for offset, col in enumerate(names):
        
        width = 0.2  # the width of the bars
        ax.bar(ds.index + (width * offset),
               ds[col], width, label=col)
    
    ax.set(
        xlim = [ds.index[0] - 0.5, ds.index[-1] + 1],
        xticks = np.arange(2013, 2023, 1),
        ylim = [0, 80],
        
        ylabel = '$V_P$ (m/s)'
            )
    
    plot_equinox_difference(ax, ds)
    return 
    

def plot_seasonal_assimetry(translate = False):
    
    fig, ax = plt.subplots(
        figsize = (18, 12),
        nrows = 2,
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    plot_epbs_rate(ax[0], translate)
    plot_gamma(ax[1])
  
    
    if translate:
        xlabel = 'Years'
        names1 = ['March',  'September', 'December']
        label = "Equinox difference (\%)"

    else:
        xlabel = 'Anos'
        names1 = ['Março',  'Setembro', 'Dezembro']
        label = 'Diferença equinocial (\%)'
        
        
    ax[-1].set_xlabel(xlabel)
    
    ax[0].legend(
         names1,
         ncol = 5, 
         bbox_to_anchor = (.5, 1.3), 
         loc = "upper center", 
         columnspacing = 0.3
         )
    
    plt.xticks(rotation = 0)
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        fontsize = 40
        )

        
    fig.text(
        0.96, 0.3, 
        label,
        rotation = 'vertical',
        fontsize = 40,
        color = 'red'
        )
    
    fig.align_ylabels()
    return fig


  
   
# fig = plot_seasonal_assimetry(translate= True)
  
# FigureName = 'annual_quiet_time'
      
# fig.savefig(
#       b.LATEX(FigureName, folder = 'bars'),
#       dpi = 400
#       )

    
p = pb.BubblesPipe(
    'events_5', 
    drop_lim = 0.3, 
    storm = 'quiet'
    )

df = p.sel_type('sunset')

df 