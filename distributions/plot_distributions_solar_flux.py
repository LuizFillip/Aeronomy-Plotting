import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()



def plot_distributions_solar_flux(
        df, 
        col = 'gamma',
        level = 100
        ):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        sharey = True,
        figsize = (12, 6)
        )
        
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    if col == 'gamma':
        vmin, vmax, step = 0, 4, 0.2
        
    elif col == 'vp':
        vmin, vmax, step = 0, 90, 5
    else:
        vmin, vmax, step = 0, 1, 0.05
    
    solar_dfs =  ev.medium_solar_level(
        df, 
        level,
        flux_col = 'f107a'
        )
     
    total = []
    for i, ds in enumerate(solar_dfs):
    
        c = plot_distribution(
            ax, 
            ds,
            limits = (vmin, vmax, step),
            col = col,
            label = f'{labels[i]}'
            )
        
        total.append(c)
        
    ax.set(
        xlim = [vmin - step, vmax + step],
        xticks = np.arange(vmin, vmax + step, step * 2),
        ylim = [-0.2, 1.3],
        yticks = np.arange(0, 1.25, 0.25),
        )
        
    ax.legend(ncol = 2, loc = 'upper center')
    
    info = f' ({sum(total)} EPBs events)'
    
    if col == 'vp':
        xlabel = b.y_label('vp')
    else:
        xlabel = b.y_label('gamma')
      
    ax.set(
        title = df.columns.name + info,
        xlabel = xlabel, 
        ylabel = 'EPB occurrence probability'
        )
    
    return fig
 
 
df = ev.concat_results('saa')

df = df.dropna(subset = 'gamma')

fig = plot_distributions_solar_flux(
    df, 
    col = 'vp'
    )

# FigureName = 'PD_gamma_effects'

# fig.savefig(b.LATEX + FigureName, dpi = 400)



