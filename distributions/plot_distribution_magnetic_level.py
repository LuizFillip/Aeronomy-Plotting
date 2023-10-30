import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



def plot_geomag_distribution(
        df, 
        col = 'gamma',
        quiet_level = 3 
        ):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        sharey = True,
        figsize = (12, 6)
        )
    
    
    if col == 'gamma':
        vmin, vmax, step = 0, 4, 0.2
        
    elif col == 'vp':
        vmin, vmax, step = 0, 85, 5
    else:
        vmin, vmax, step = 0, 1, 0.05
        
    labels = [f'$Kp \\leq$ {quiet_level}', 
              f'$Kp >$ {quiet_level}']
    
    datasets = ev.kp_levels(
        df, 
        level = quiet_level
        )
    
    total = []
    
    for i, ds in enumerate(datasets):
                       
        c = plot_distribution(
            ax, 
            ds, 
            limits = (vmin, vmax, step),
            col = col,
            label = f'{labels[i]}'
            )
        
        total.append(c)
        
    ax.legend(ncol = 2, loc = 'upper center')
    
    ax.set(
        xlim = [vmin, vmax],
        xticks = np.arange(vmin, vmax, step * 2),
        ylim = [-0.2, 1.3],
        yticks = np.arange(0, 1.25, 0.25),
        )
    
    infos = f' ({sum(total)} EPBs events)'
    ax.set(
        title = df.columns.name + infos, 
        xlabel =  b.y_label('gamma'), 
        ylabel = 'EPB occurrence probability'
        )
    
    return fig


df = ev.concat_results('saa')

col = 'vp'
fig = plot_geomag_distribution(df, col)