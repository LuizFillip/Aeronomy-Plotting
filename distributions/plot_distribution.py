import core as c
import numpy as np


args = dict(
    capsize = 3,
    marker = 's'
    )


def plot_distribution(
        ax, 
        df, 
        col = 'gamma',
        label = '', 
        count = True,
        drop = 2
        ):

    ds = c.probability_distribuition(
        df,
        col
        )
    
    epbs = ds['epbs'].sum()
    
    ds = ds.loc[~(
        (ds['days'] == 1) & 
        (ds['epbs'] == 1))
        ]
        
 
    # if drop is not None:
    #     ds.drop(
    #         ds.tail(drop).index, 
    #         inplace = True
    #         )
    
    if count:
        LABEL = f'{label} ({epbs} events)'
    else:
        LABEL = label
    
    ax.errorbar(
        ds['mean'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_error'],
        label = LABEL,
        **args
        )
    
    vmin, vmax, step = c.limits(col)
    
    ax.set(
        xlim = [vmin, vmax],
        ylim = [-0.2, 1.4], 
        yticks = np.arange(0, 1.2, 0.25),
        xticks = np.arange(
            vmin, vmax + step, step*2
            )
        )
    

    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return epbs 



