import core as c 
import pandas as pd 
import base as b 
import matplotlib.pyplot as plt 
import PlasmaBubbles as pb 
import numpy as np 
import datetime as dt 
import plotting as pl 

PATH_GAMMA = 'database/gamma/p1_saa.txt'

b.config_labels(blue = False, fontsize = 35)


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
    
    ax1.plot(ds.index, ds['eq_diff'],  color = 'red',
             lw = 1.5, markersize = 10, marker = 's')
    
    ax1.axhline(0, linestyle = '--')
    
    ax1.set(ylim = [-60, 60])
    
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    return ax1

def plot_epbs_rate(ax, translate = True):
    
    df = pb.sel_typing(
         b.load('events_class2'), 
         typing = 'sunset', 
         indexes = True, 
         year = 2022)
    
    df = df.loc[df['dst'] >= -30]
    
    df = df.rename(columns = {-50: 'epb'})
    
    ds = seasonal_by_year(df, parameter = 'epb')

    for offset, col in enumerate(names):
       
        width = 0.2  
        ax.bar(ds.index + (width * offset),
               ds[col], width, label=col)
    
    if translate: 
        ylabel = 'Rate of occurrence (\%)'
    else:
        ylabel = 'Taxa de ocorrência (\%)'
        
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
    
    df = df.loc[df['dst'] >= -30]
    
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
    

def set_data(file):
    
    df = b.load('database/FabryPerot/' + file)
    
    df['zon'] = df[['west', 'east']].mean(axis = 1)
    df['mer'] = df[['south', 'north']].mean(axis = 1)
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = (df.index.year + 
                 df.index.month / 12  +
                 df.index.day / 31)
    
    return df


def plot_annualy_quiet_time(translate = False):
    fig, ax = plt.subplots(
        figsize = (18, 14),
        nrows = 3,
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    plot_epbs_rate(ax[0], translate)
    plot_gamma(ax[1])
    # plot_vp(ax[1])
    pl.plot_f107(ax[2], mean = None)
    if translate:
        xlabel = 'Years'
        names1 = ['March',  'September', 'December']

    else:
        xlabel = 'Anos'
        names1 = ['Março',  'Setembro', 'Dezembro']
        
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
    if translate:
        label = "Equinox difference (\%)"
    else:
        label = 'Diferença equinocial (\%)'
        
    fig.text(
        0.96, 0.45, 
        label,
        rotation = 'vertical',
        fontsize = 40,
        color = 'red'
        )

    return fig


  
   
fig = plot_annualy_quiet_time()
  
FigureName = 'annual_quiet_time'
      
# fig.savefig(
#       b.LATEX(FigureName, folder = 'bars'),
#       dpi = 400
#       )

# df = set_data('mean')
# # 

# ds = df.loc[
#     (df.index.time >= dt.time(22, 0)) | 
#     (df.index.time <= dt.time(0, 0))]

# ds = ds.resample('1D').mean()


# ds = seasonal_by_year(ds, parameter = 'mer')


# # df.loc[df.index.year == 2016]

# ds
