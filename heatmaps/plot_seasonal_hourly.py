import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import core as c 

b.config_labels()


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
        extent = [20, 32, 12, 0],
        cmap = 'magma'
        )
        
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
        xticklabels = xticklabels, 
        yticklabels = yticklabels
        )
    
    return 


def get_dusk(ds, col):
    
    df = pb.pivot_data(ds, values = 'dusk')
  
    df['day'] = (df.index.month + df.index.day / 31) - 1
    
    return df[[col, 'day']].rename(columns = {col: 'dusk'})


def plot_seasonal_hourly(df):
    
 
    fig, ax = plt.subplots(
          ncols = 3, 
          dpi = 300, 
          sharex = True, 
          sharey = True,
          figsize = (16, 8)
          )

    plt.subplots_adjust(hspace = 0.1)
    cond = [
        df['kp'] <= 3, 
        (df['kp'] > 3) & (df['kp'] <= 6), 
        df['kp'] > 6]
    
    for i, ax in enumerate(ax.flat):
        
        ds = pb.hourly_distribution(df.loc[cond[i]], step = 0.5)

        plot_heatmap(ax, ds, colorbar = False)
        
        df1 = df.loc[df.index.year == 2020]
        
        ax.plot(
            df1['dusk'], df1['day'],
            lw = 3, 
            color = 'w')
        
        
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = 'magma',
            fontsize = 25,
            step = 10,
            y = 0.97,
            label = 'Ocorrência (\%)'
            )
    return fig
    




def sel_epb_typing(col, typing):
    ds = b.load('events_class2')
    
    dusk = get_dusk(ds, col)
    
    epbs  = ds.loc[
        (ds['type'] == typing) &
        (ds['lon'] == col)  &
        (ds['drift'] == 'fresh'), ['start']
        ]
        
    idx = c.geo_index()
    
    return pd.concat([epbs, idx, dusk], axis = 1)

col = -70

typing = 'midnight'

df = sel_epb_typing(col, typing)

fig = plot_seasonal_hourly(df)




