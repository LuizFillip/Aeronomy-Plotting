import core as c
import numpy as np
import base as b 

args = dict( capsize = 3, marker = 's')


def plot_distribution(
        ax, 
        df, 
        col = 'gamma',
        label = '', 
        count = False,
        drop = 2
        ):

    ds = c.probability_distribuition(
        df,
        col
        )
    
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



