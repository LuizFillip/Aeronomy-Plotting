import numpy as np
import matplotlib.pyplot as plt
from math import floor, ceil
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()

def plot_single_distribution(
        ax,
        df, 
        geomag = 'quiet', 
        step = 0.2, 
        gamma = 'all',
        epbs = '-40', 
        quiet_level = 4
        ):
    

    vmin, vmax = df[gamma].min(), df[gamma].max()
    
    vmin, vmax = floor(vmin), ceil(vmax)
    
        
    labels = [f'$Kp \\leq$ {quiet_level}', 
              f'$Kp >$ {quiet_level}']
    
    datasets = ev.kp_levels(
        df, 
        quiet_level = quiet_level
        )
    count = []

    for i, ds in enumerate(datasets):
        
        index = i + 1

        c = plot_distribution(
            ax, 
            ds,
            label = f'({index}) {labels[i]}',
            step = step, 
            col_gamma = gamma,
            col_epbs = epbs
            )
        
        count.append(f'({index}) {c} events')
        

    infos = ('EPB occurrence\n' +
             '\n'.join(count))
        
    ax.text(0.79, 0.3, infos, 
            transform = ax.transAxes)
        
    ax.set(
            xlim = [vmin - step, vmax],
            xticks = np.arange(vmin, vmax, step * 2),
            ylim = [-0.2, 1.2],
            yticks = np.arange(0, 1.25, 0.25),
            )

    return ax


def plot_distributions_solar_flux(
        df, fontsize = 30 
        ):
    

    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3,
        sharex = True,
        sharey = True,
        figsize = (12, 12)
        )
    
    cycles = ['$F_{10.7} < 100$',
             '$100 < F_{10.7} < 150$', 
             '$F_{10.7} > 150$']
    
    
    for i, ds in enumerate(
            ev.solar_flux_cycles(df)
            ):
        
        plot_single_distribution(ax[i], ds)
         
        ax[i].set(title = cycles[i])
        
        
    ax[0].legend(
            ncol = 3, 
            bbox_to_anchor = (.5, 1.5),
            loc = "upper center"
            )
    
    fig.text(
        0.03, 0.32, 
        'EPB occurrence probability',
        rotation = "vertical", 
        fontsize = fontsize
        )
    
    fig.text(
        0.4, 0.07, 
        "$\\gamma_{FT}~$ ($\\times 10^{-3}~s^{-1}$)", 
        rotation = "horizontal", 
        fontsize = fontsize
        )
    
    
    return fig
 
 
df = b.load('all_results.txt')

# fig = plot_distributions_solar_flux(df)

# df = df.loc[(df['f107'] < 100) &
#             (df['kp_max'] <= 3)]

# ds = ev.probability_distribuition(
#     df,
#     step = 0.2, 
#     col_gamma = 'all',
#     col_epbs = '-40'
#     )

# ds


df['drift'] = df['drift'] *1e3
# df['gravity'] = df['gravity'] *1e3

