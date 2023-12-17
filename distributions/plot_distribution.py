import core as c
import numpy as np
import base as b 
import matplotlib.pyplot as plt 

args = dict(capsize = 3, marker = 's')

def plot_histogram(
        ax, 
        dataset, 
        index, 
        label, 
        col = 'gamma',
        width = 0.07,
        axis_label = False
        ):
    
    ds = c.probability_distribuition(
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
        if col == 'vp':
            xlabel = b.y_label('vp')
        else:
            xlabel = b.y_label('gamma')
            
        ax.set(xlabel = xlabel, 
               ylabel = 'Frequency of occurrence')
    
    plt.xticks(rotation = 0)
    
    vmin, vmax, step = c.limits(col)
    
    
    
    ax.set(
        xlim = [vmin, vmax],
        xticks = np.arange(
            vmin, vmax + step, step*2
            ),
       
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

    ds = c.probability_distribuition(df, col)
    
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
        
    return epbs 



