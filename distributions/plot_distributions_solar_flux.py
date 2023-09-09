import numpy as np
import matplotlib.pyplot as plt
from math import floor, ceil
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()

def plot_distributions_solar_flux(
        ax,
        df, 
        geomag = 'quiet', 
        step = 0.2, 
        col_gamma = 'all',
        col_epbs = '-40'
        ):
    
    
    
    vmin, vmax = df[col_gamma].min(), df[col_gamma].max()
    
    vmin, vmax = floor(vmin), ceil(vmax)
    
        
    labels = ['$Kp \\leq 3$', '$Kp > 3$']
    
    datasets = [df[df['kp_max'] <= 3], 
                df[df['kp_max'] > 3]
                ]
    count = []

    for i, ds in enumerate(datasets):
        
        index = i + 1

        c = plot_distribution(
            ax, 
            ds,
            label = f'({index}) {labels[i]}',
            step = step, 
            col_gamma = col_gamma,
            col_epbs = col_epbs
            )
        

        count.append(f'({index}) {c} events')
        

    infos = 'EPB occurrence\n' + '\n'.join(count)
        
    ax.text(0.77, 0.3, infos, transform = ax.transAxes)
        
    ax.set(
              xlim = [vmin - step, vmax + step],
              xticks = np.arange(vmin, vmax, step * 2),
              ylim = [-0.2, 1.2],
              yticks = np.arange(0, 1.25, 0.25),
              )

   



    
    
   

fig, ax = plt.subplots(
    dpi = 300, 
    nrows = 3,
    sharex = True,
    sharey = True,
    figsize = (12, 12)
    )


df = b.load('all_results.txt')

df = df.loc[~(df['all'] > 3.5)]

names = ['$F_{10.7} < 100$',
         '$100 < F_{10.7} < 150$', 
         '$F_{10.7} > 150$']


for i, ds in enumerate(ev.solar_flux_cycles(df)):
    

    plot_distributions_solar_flux(
         ax[i],
         ds, 
         )
     
    ax[i].set(title = names[i])
    
    
ax[0].legend(ncol = 3, 
          bbox_to_anchor = (.5, 1.5),
          loc = "upper center"
          )

ax[2].set(xlabel = "$\\gamma_{FT}~$ ($\\times 10^{-3}~s^{-1}$)")
ax[1].set( ylabel = 'EPB occurrence probability')
#  fig.suptitle(title, y = 1.05)
 
 
