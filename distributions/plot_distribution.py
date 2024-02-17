import core as c
import numpy as np
import base as b 
import matplotlib.pyplot as plt 

args = dict(capsize = 3, marker = 's')

def plot_cumullative(ax, ds, color):
     
     ax1 = ax.twinx()

     ax1.plot(ds['start'], 
               np.cumsum(ds['days']),
               lw = 2,
               color = color
               )
     
     ax1.set(ylim = [0, 1.2], 
             yticks = np.arange(0, 1.2, 0.25), 
             ylabel = 'Cumulated frequency')
     
     
def plot_histogram(
        ax, 
        dataset, 
        index, 
        label, 
        col = 'gamma',
        width = 0.07,
        axis_label = False
        ):
    
    if col == 'vp':
        xlabel = b.y_label('vp')
        width = 1.7
    elif col == 'gravity':
        xlabel = b.y_label('gamma')
        width = 0.015
    else:
        xlabel = b.y_label('gamma')
        width = 0.07
        
    ds = c.probability_distribution(
        dataset,
        col
        )
    
    days = int(ds['days'].sum())
    
    offset = width * index
    
    ax.bar(
        ds['start'] + offset,
        ds['days'], 
        width = width, 
        label = label
        )
     
    if axis_label:

        ax.set(
            xlabel = xlabel, 
            ylabel = 'Frequency of occurrence'
            )
    
    plt.xticks(rotation = 0)
    
    vmin, vmax, step = c.limits(col)
    
    ax.set(
        xlim = [vmin, vmax],
        xticks = np.arange(
            vmin, vmax + step, step*2
            )
        )
    
    
    return days

def plot_distribution(
        ax, 
        df, 
        col = 'gamma',
        label = '', 
        count = False,
        axis_label = False
        ):

    ds = c.probability_distribution(df, col)    
    
    ds = ds.loc[~((ds['days'] == 1) & 
                  (ds['epbs'] == 1))].dropna()
    
    # ds['std'] = ds['std'].replace(np.nan, 0)
    
    epbs = ds['epbs'].sum()
    
    if count:
        LABEL = f'{label} ({epbs} events)'
    else:
        LABEL = label
    
    ax.errorbar(
        ds['start'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_error'],
        label = LABEL,
        **args
        )
    
    vmin, vmax, step = c.limits(col)
    
    if col == 'vp':
        xlabel = b.y_label('vp')
    else:
        xlabel = b.y_label('gamma')
    
    ax.set(
        xlim = [vmin, vmax],
        ylim = [-0.2, 1.4], 
        yticks = np.arange(0, 1.2, 0.25),
        xticks = np.arange(
            vmin, vmax + step, step*2
            ),
       
        )
    
    if axis_label:
        ax.set(
            xlabel = xlabel, 
            ylabel = 'EPB occurrence probability'
            )
    
    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return ds, epbs 



