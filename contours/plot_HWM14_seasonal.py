import matplotlib.pyplot as plt 
import base as b 
import datetime as dt 
import pandas as pd 
import core as c 



def mean_compose(df):
    ds = pd.pivot_table(
        df, 
        columns = 'day', 
        index = 'time', 
        values = 'zon'
        )
    
    data = {
        'mean': ds.mean(axis = 1), 
        'std': ds.std(axis = 1)
        }
    
    ds = pd.DataFrame(data, index = ds.index)
    ref = dt.datetime(2014, 1, 1)
    ds.index = b.new_index_by_ref(ref, ds.index)
    return ds 

def plot_curves(ax, df1, label):
    ax.errorbar(
        df1.index, 
        df1['mean'],
        yerr = df1['std'],
        capsize = 5, 
        lw = 1.5,
        marker = 's',
        markersize = 10,
        fillstyle =  'none',
        label = label
        )
    
  
    ax.set(
        ylim = [-50, 150], 
        yticks = [0, 50, 100, 150]
        )
    ax.axhline(0, linestyle = ':')
    ax.axhline(100, linestyle = ':')
    b.axes_hour_format(
            ax, 
            hour_locator = 2, 
            )
    return None 

def plot_site(ax, col, df, label):

    seasons = [
        'march', 
        'september', 
        'december'
        ]
    
    
    for i, season in enumerate(seasons):
        
        ds = c.SeasonsSplit(
            df, seasons[i], 
            translate = True)
        
        df1 = mean_compose(
            ds.sel_season
            ).resample('30min').asfreq()
        
        plot_curves(ax[i, col], df1, label)
        
        l = b.chars()[i]
        
        if col == 0:
            
            s = f'({l}) {ds.name}'
        else:
            s = f'{ds.name}'
        ax[i, col].text(
            0.02, 0.82, s, 
            transform = ax[i, col].transAxes
            
            )
            
    return None 

def set_data(infile):
    
    df = b.load(infile)
  

    df['doy'] = df.index.day_of_year 
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = (
        df.index.year + 
        df.index.month / 12  +
        df.index.day / 31
        )
    
    return df

def plot_HWM14_seasonal():
    
    fig, axes = plt.subplots(
        nrows = 3,
        ncols = 2,
        sharex = True, 
        sharey = True,
        dpi = 300, 
        figsize = (18, 12)
        )
    
    plt.subplots_adjust(
        wspace = 0.05, 
        hspace = 0.1
        )
    
    infile = 'database/winds/winds_caj'
    df = set_data(infile)
    
    plot_site(
        axes, 0, 
        df.loc[df.index.year <= 2017], 
        label = 'Cachoeira Paulista'
        )
    
    plot_site(
        axes, 1, 
        df.loc[df.index.year >= 2018], 
        label = 'Cachoeira Paulista'
        )
    
    
    infile = 'database/winds/winds_car'
    df = set_data(infile)
    
    plot_site(
        axes, 0, 
        df.loc[df.index.year <= 2017], 
        label = 'São João do Cariri'
        )
    
    plot_site(
        axes, 1, 
        df.loc[df.index.year >= 2018],
        label = 'São João do Cariri'
        )
    
    axes[0, 0].set(title = '2013 a 2017')
    axes[0, 1].set(title = '2018 a 2023')
    
    
    axes[0, 0].legend(
        ncol = 2, 
        loc = 'upper center',
        bbox_to_anchor = (1, 1.7),
        )
    
    
    fig.text(
          0.03, 0.3, 
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

fig = plot_HWM14_seasonal()

# FigureName = 'seasonal_hwm14'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'winds'),
#     dpi = 400
#     )