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
        step = 0.2, 
        gamma = 'night',
        quiet_level = 4
        ):
    

    vmin, vmax = df[gamma].min(), df[gamma].max()
    
    vmin, vmax = floor(vmin), ceil(vmax)
    
        
    labels = [f'$Kp \\leq$ {quiet_level}', 
              f'$Kp >$ {quiet_level}']
    
    datasets = ev.kp_levels(
        df, 
        level = quiet_level
        )
    
    
    count = []
    nums = []
    for i, ds in enumerate(datasets):
                
        index = i + 1

        c = plot_distribution(
            ax, 
            ds,
            label = f'({index}) {labels[i]}',
            step = step, 
            col_gamma = 'night',
            col_epbs = 'epb'
            )
        
        nums.append(c)
        
        count.append(f'({index}) {c} events')
        
    
    infos = ('EPB occurrence\n' +
             '\n'.join(count))
        
    ax.text(
        0.79, 0.2, infos, 
        transform = ax.transAxes
        )
        
    ax.set(
        xlim = [vmin - step, vmax],
        xticks = np.arange(vmin, vmax, step * 2),
        ylim = [-0.2, 1.3],
        yticks = np.arange(0, 1.25, 0.25),
        )

    return sum(nums)


def plot_distributions_solar_flux(
        df, 
        fontsize = 25,
        level = 100
        ):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        sharey = True,
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    titles = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    solar_dfs =  ev.medium_solar_level(df, level)
    
    for i, ds in enumerate(solar_dfs):
        
        total = plot_single_distribution(ax[i], ds)
        
        letter = b.chars()[i]
        
        ax[i].text(
            0.02, 0.87, 
            f"({letter}) {titles[i]} ({total} events)", 
            transform = ax[i].transAxes
            )
        
    ax[0].legend(
            ncol = 3, 
            bbox_to_anchor = (.5, 1.2),
            loc = "upper center"
            )
    
    fig.text(
        0.03, 0.32, 
        'EPB occurrence probability',
        rotation = "vertical", 
        fontsize = fontsize
        )
    
    xlabel = "$\\gamma_{FT}~$ ($\\times 10^{-3}~s^{-1}$)"
   
    
    ax[1].set(xlabel = xlabel)
    
    fig.suptitle(df.columns.name)
    
    return fig
 
 
df = ev.concat_results('saa')

# df = df.loc[~((df.index.year == 2017) |
#               (df.index.year == 2018) |
#               (df.index.year == 2022))]


fig = plot_distributions_solar_flux(df, level = 100)

fig.savefig(b.LATEX + 'paper1//probability_distribution', dpi = 400)

