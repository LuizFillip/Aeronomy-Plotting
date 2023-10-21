import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()



def plot_distributions_solar_flux(
        df, 
        fontsize = 25,
        level = 100, 
        step = 0.2
        ):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        sharey = True,
        figsize = (12, 6)
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    
    vmin, vmax = 0, 3.4
    
    solar_dfs =  ev.medium_solar_level(df, level)
      
    for i, ds in enumerate(solar_dfs):
    
        c = plot_distribution(
            ax, 
            ds,
            label = f'{labels[i]}',
            step = 0.2
            )
        

        ax.set(
            xlim = [vmin - step, vmax],
            xticks = np.arange(vmin, vmax, step * 2),
            ylim = [-0.2, 1.3],
            yticks = np.arange(0, 1.25, 0.25),
            )
            
        
    ax.legend(
            ncol = 3, 
            loc = "upper center"
            )
    
    xlabel = "$\\gamma_{FT}~$ ($\\times 10^{-3}~s^{-1}$)"
   
    ylabel = 'EPB occurrence probability'
    
    ax.set(xlabel = xlabel, ylabel = ylabel)
    
    fig.suptitle(df.columns.name)
    
    return fig
 
 
# df = ev.concat_results('saa', col_g = 'e_f')

#df = df.loc[df['kp'] > 3 ]

#fig = plot_distributions_solar_flux(df, level = 100)

# fig.savefig(b.LATEX + 'paper1//probability_distribution', dpi = 400)

