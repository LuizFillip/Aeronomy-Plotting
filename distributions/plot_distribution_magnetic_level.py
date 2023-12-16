import numpy as np
import matplotlib.pyplot as plt
import base as b
import core as c
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
        
    labels = [f'$Kp \\leq$ {quiet_level}', 
              f'$Kp >$ {quiet_level}']
    
    datasets = c.kp_levels(
        df, 
        level = quiet_level
        )
    
    total = []
    
    for i, ds in enumerate(datasets):
                       
        count = plot_distribution(
            ax, 
            ds, 
            col = col,
            label = f'{labels[i]}'
            )
        
        total.append(count)
        
    ax.legend(ncol = 2, loc = 'upper center')
    
    ax.set(
        xlabel =  b.y_label('gamma'), 
        ylabel = 'EPB occurrence probability'
        )
    
    return fig


df = c.concat_results('saa')

col = 'gamma'
fig = plot_geomag_distribution(df, col)

df