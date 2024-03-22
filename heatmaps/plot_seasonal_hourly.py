import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

def change_format():
    ds = b.load('events_class')
    
    df = pb.pivot_data(ds, values = 'dusk')
    
    df = df.loc[df.index.year == 2013, -60]
    
    df = df.resample('1M').asfreq()
    
    df.index = df.index.month 
    
    return df

def plot_heatmap(
        ax, 
        ds, 
        col = '-50', 
        percent = True, 
        colorbar = True
        ):
  
    yticks = np.arange(1, 13, 1)
    xticks = np.arange(20, 35, 1)
 
    
    if percent:
        factor = 100
        units = ' (\%)'
    else:
        factor = 1
        units = ''
        
    ticks =  np.arange(0, 1.25 * factor, 0.25 * factor)
 
    
    img = ax.imshow(
        ds.to_numpy() * factor,
        aspect = 'auto', 
        extent = [
            xticks[0], xticks[-1], 
            yticks[0], yticks[-1]],
        cmap = 'mako', 
        vmax = 1 *factor, 
        vmin = 0
        )
    
    ax.axes.invert_yaxis()
    
    # xticks = np.where(xticks >= 24, xticks - 24, xticks)
    # yticks = b.month_names(sort = True)
    
    if colorbar:
        b.colorbar(
            img, 
            ax,
            ticks = ticks, 
            label = f"Ocorrência{units}"
            )
    df = change_format()

    ax.plot(df.values, df.index , lw = 3, color = 'w')
   
    ax.set(
        xticks = xticks, 
        yticks = yticks[::-1],
       
        )
    
    if not colorbar:
        ax.set(
            ylabel = 'Meses', 
            xlabel = 'Hora universal'
            )
    
    return 


def indices():
    PATH_INDEX = 'database/indices/omni_hourly.txt'

    ds = b.load(PATH_INDEX)[['kp', 'dst']]
    
    ds = ds.loc[(ds.index.year >= 2013) & 
                (ds.index.year <= 2023)]
    
    return ds.resample('60s').asfreq().interpolate()



def plot_seasonal_hourly(col = '-60'):
    
 
    fig, ax = plt.subplots(
        ncols = 2, 
        dpi = 300, 
        sharex = True, 
        sharey = True,
        figsize = (16, 6)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    df = pd.concat(
        [b.load('test'), indices()], axis = 1).dropna()
    
    ds = pb.concat_months(df.loc[df['kp'] <= 3], col)
    
    plot_heatmap(ax[0], ds, col = col, colorbar=False)
    
    ds = pb.concat_months(df.loc[df['kp'] > 3], col)

    plot_heatmap(ax[1], ds, col = col)
    
    

# plot_seasonal_hourly()

# df = pd.concat(
#      [b.load('test'),   indices()], axis = 1).dropna()

col = '-60'


# ds = pb.concat_months(df.loc[df['kp'] > 3], col)


# plt.imshow(ds.values )


ds = b.load('events_class')

df = pb.pivot_data(ds, values = 'start')

PATH_INDEX = 'database/indices/omni_hourly.txt'

ds = b.load(PATH_INDEX)[['kp', 'dst']]

df