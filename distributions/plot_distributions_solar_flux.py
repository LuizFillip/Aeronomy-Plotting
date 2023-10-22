import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()



def plot_distributions_solar_flux(
        df, 
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
    
    
    vmin, vmax, step = 0, 3.2, 0.2
    
    solar_dfs =  ev.medium_solar_level(df, level)
      
    for i, ds in enumerate(solar_dfs):
    
        plot_distribution(
            ax, 
            ds,
            label = f'{labels[i]}'
            )
        
    ax.set(
        xlim = [vmin - step, vmax + step],
        xticks = np.arange(vmin, vmax, step * 2),
        ylim = [-0.2, 1.3],
        yticks = np.arange(0, 1.25, 0.25),
        )
        
        
    ax.legend(
            ncol = 3, 
            loc = "upper center"
            )
      
    ax.set(
        title = df.columns.name,
        xlabel =  b.y_label('gamma'), 
        ylabel = 'EPB occurrence probability'
        )
    
    
    return fig
 
 
df = ev.concat_results('saa', col_g = 'e_f')

df = df.loc[df['kp'] <= 3]

fig = plot_distributions_solar_flux(df, level = 100)

# fig.savefig(b.LATEX + 'paper1//probability_distribution', dpi = 400)

