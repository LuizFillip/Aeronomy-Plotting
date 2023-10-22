import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



def plot_geomag_distribution(
        df, 
        quiet_level = 3 
        ):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        sharey = True,
        figsize = (12, 6)
        )
    
    vmin, vmax, step = 0, 3.2, 0.2
    
    labels = [f'$Kp \\leq$ {quiet_level}', 
              f'$Kp >$ {quiet_level}']
    
    datasets = ev.kp_levels(
        df, 
        level = quiet_level
        )
    
    for i, ds in enumerate(datasets):
                
        index = i + 1
       
        plot_distribution(
            ax, 
            ds,
            label = f'({index}) {labels[i]}'
            )
            
    ax.legend(ncol = 2, loc = 'upper left')
    
        
    ax.set(
        xlim = [vmin - step, vmax],
        xticks = np.arange(vmin, vmax, step * 2),
        ylim = [-0.2, 1.3],
        yticks = np.arange(0, 1.25, 0.25),
        )
    
    ax.set(
        title = df.columns.name, 
        xlabel =  b.y_label('gamma'), 
        ylabel = 'EPB occurrence probability'
        )
    
    return fig


df = ev.concat_results('saa', col_g = 'e_f')

fig = plot_geomag_distribution(
        df, 
        quiet_level = 3 
        )