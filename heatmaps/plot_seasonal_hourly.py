import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import core as c 


PATH_INDEX = 'database/indices/omni_pro.txt'



def plot_heatmap(
        ax, 
        values, 
        percent = True, 
        colorbar = True,
        step = 1
        ):
  
    yticks = np.arange(1, 13, 1)
    xticks = np.arange(20, 32 + step, step)
     
    if percent:
        factor = 100
        units = ' (\%)'
    else:
        factor = 1
        units = ''
        
    ticks =  np.arange(0, 1.25 * factor, 0.25 * factor)
 
    
    img = ax.imshow(
        values,
        aspect = 'auto', 
        extent = [
            20, 32, 
            12, 0
            ],
        cmap = 'mako'
        )
    
    # ax.axes.invert_yaxis()
    
    xticklabels = np.where(xticks >= 24, xticks - 24, xticks)
    yticklabels = b.month_names(sort = True)
    
    if colorbar:
        b.colorbar(
            img, 
            ax,
            ticks = ticks, 
            label = f"Ocorrência{units}"
            )
   
   
    ax.set(
        xticks = xticks, 
        yticks = yticks - 0.5,
        # ylim = [yticks[-1], yticks[0]], 
        xticklabels = xticklabels, 
        yticklabels = yticklabels
        )
    
    # if not colorbar:
    #     ax.set(
    #         ylabel = 'Meses', 
    #         xlabel = 'Hora universal'
    #         )
    
    return 


def get_dusk(ds, col):
    
    df = pb.pivot_data(ds, values = 'dusk')
    
    df = df.loc[df.index.year == 2013, col]
    
    df = df.resample('30D').asfreq()
    
    df.index = df.index.month + df.index.day / 31
    
    return df


def plot_seasonal_hourly(df, dusk):
    
 
    fig, ax = plt.subplots(
          nrows = 3, 
          dpi = 300, 
          sharex = True, 
          sharey = True,
          figsize = (10, 16)
          )

    plt.subplots_adjust(hspace = 0.1)
    cond = [
        df['kp'] <= 3, 
        (df['kp'] > 3) & (df['kp'] <= 6), 
        df['kp'] > 6]
    
    for i, ax in enumerate(ax.flat):
        
        ds = pb.hourly_distribution(df.loc[cond[i]])

        plot_heatmap(ax, ds, colorbar = False)
        
        ax.plot(dusk.values, dusk.index - 1, lw = 3, 
                color = 'w')
    
    

col = -80

typing = 'midnight'

ds = b.load('events_class')

dusk = get_dusk(ds, col)

ds = ds.loc[(ds['type'] == typing) & 
            (ds['drift'] == 'fresh')]

epbs = ds.loc[ds['lon'] == col, ['start']]

idx = c.geo_index()

df = pd.concat([epbs, idx], axis = 1)


plot_seasonal_hourly(df, dusk)





