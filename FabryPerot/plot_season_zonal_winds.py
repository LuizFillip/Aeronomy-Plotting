import base as b 
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 
import datetime as dt 
import numpy as np

b.config_labels(fontsize = 30)

def ones_data(dn):
    start = dn.replace(hour = 21)
    end = start + dt.timedelta(hours = 10)
    # df_source = c.geo_index()
    # df['dst'] = df.index.map(df_source['dst'])
    
    
    index = pd.date_range(start, end, freq = '10min')
    
    return pd.DataFrame({'epb': np.ones(len(index))}, index = index)


def adding_epb_occurrence(df):
    
    ds = b.load('events_class2')
    ds = ds.loc[
        (ds['type'] == 'sunset') &
        (ds['drift'] == 'fresh') &
        (ds['lon'] == -50)]

    out = []
    for dn in ds.index:
        out.append(ones_data(dn))
        
    ds1 = pd.concat(out)
    
    df['epb'] = df.index.map(ds1['epb'])
    
    df['epb'] = df['epb'].replace(float('nan'), 0)
    
    return df 


def mean_compose(ds, direction = 'zonal'):
    
    if direction == 'zonal':
        dirs = ['east', 'west']
    else:
        dirs = ['north', 'south']
    
    
    df1 = pd.pivot_table(
        ds, 
        values = dirs[0], 
        index = 'time', 
        columns = 'day')
    
    df2 = pd.pivot_table(
        ds, 
        values = dirs[1], 
        index = 'time', 
        columns = 'day'
        )
    
    data  = {
        'west': df2.mean(axis = 1), 
        'east': df1.mean(axis = 1), 
        'seast': df1.std(axis = 1), 
        'swest': df2.std(axis = 1)
        }
    
    df = pd.DataFrame(data, index = df1.index)
   
    df['mean'] = df[['west', 'east']].mean(axis = 1)
    df['std'] = df[['swest', 'seast']].mean(axis = 1)
    ref = dt.datetime(2014, 1, 1)
    df.index = b.new_index_by_ref(ref, df.index)
    
    return df 

 
def plot_curves(ax, df1, label):
    
    ax.errorbar(
        df1.index, 
        df1['mean'],
        yerr = df1['std'],
        capsize = 5, 
        lw = 1.5,
        marker = 's',
        markersize = 10,
        fillstyle=  'none',
        label = label
        )
    
  
    ax.set(ylim = [-50, 250],
           yticks = [0, 50, 100, 150, 200])
    ax.axhline(0, linestyle = ':')
    ax.axhline(100, linestyle = ':')
    b.axes_hour_format(
            ax, 
            hour_locator = 2, 
            )
    
    return None 

def plot_season_zonal_winds(
        axes, 
        col, df, 
        direction = 'zonal',
        label = 'With EPBs'
        ):
    
    seasons = [
        'march', 
        # 'june', 
        'september', 
        'december'
        ]
    

    for i, season in enumerate(seasons):
        
        # try:
        ds = c.SeasonsSplit(
            df, season, 
            translate = True
            )
        
        df1 = mean_compose(
            ds.sel_season, 
            direction = direction
            ).resample('1H').asfreq()
        
        plot_curves(axes[i, col], df1, label)
        
        l = b.chars()[i]
        if col == 0:
            s = f'({l}) {ds.name}'
        else:
            s = f'{ds.name}'
        axes[i, col].text(
            0.02, 0.82, s, 
            transform = axes[i, col].transAxes
            
            )

    return None

def plot_with_without_epbs(
        df, 
        ax, 
        col,
        direction = 'zonal'
        ):

    plot_season_zonal_winds(
        ax, col, df.loc[df['epb'] == 0], 
        direction= direction,
        label = 'EPBs ausentes')
    
    plot_season_zonal_winds(
        ax, col, df.loc[df['epb'] == 1], 
        direction= direction,
        label = 'EPBs presentes')
    
    return None


def set_data(file):
    
    df = b.load('database/FabryPerot/' + file)
    
    # df = df.loc[df.index.year < 2022]
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = (df.index.year + 
                 df.index.month / 12  +
                 df.index.day / 31)
    
    return adding_epb_occurrence(df)

# title = 'Cachoeira Paulista'
def plot_FPI_seasonal_winds():
    
    fig, ax = plt.subplots(
        nrows = 3,
        ncols = 2,
        sharex = True, 
        sharey = True,
        dpi = 300, 
        figsize = (18, 12)
        )
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.05
        )
    
    df = set_data('mean')
    
    plot_with_without_epbs(df,  ax, 0)
    
    df = set_data('mean_ch')
    
    df = df.loc[df.index.year == 2019]
    
    # print(df)
    plot_with_without_epbs(df, ax, 1)
    
    
    ax[0, 0].legend(
         ncol = 2, 
         loc = 'upper center',
         bbox_to_anchor = (1., 1.6),
         )
    
    
    ax[0, 0].set(title = 'São João do Cariri')
    ax[0, 1].set(title =  'Cachoeira Paulista')
    
    
    fig.text(
          0.02, 0.3, 
          'Velocidade zonal (m/s)', 
          fontsize = 40, 
          rotation = 'vertical'
          )
    
    fig.text(
          0.42 , 0.03, 
          'Hora universal', 
          fontsize = 40, 
          )
    
    return fig 

# fig = plot_FPI_seasonal_winds()

# FigureName = 'seasonsal_analysis'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'FPI'),
#     dpi = 400
#     )


df = set_data('mean_ch')
 
df = df.loc[df.index.year == 2020]

df