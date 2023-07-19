import pandas as pd
import matplotlib.pyplot as plt
import settings as s
from common import load_by_alt_time
import RayleighTaylor as rt

fig, ax = plt.subplots(
    dpi = 300, 
    ncols = 3,
    nrows = 3,
    sharey = True, 
    sharex = 'col',
    figsize = (16, 10)
    )

plt.subplots_adjust(
    hspace = 0.3, 
    wspace = 0.05
    )

markers = ['^', 's', 'o']

rt_labels = [
       rt.EquationsRT().gravity(), 
       rt.EquationsRT().winds(), 
       rt.EquationsRT().drift()
       ]

dates = pd.date_range("2013-3-16 22:00", freq = "1D", periods = 3)

alt = 300

names = ['gravity', 'wind', 'drift']

for j, dn in enumerate(dates):
    

    local = rt.gamma_forms(
        load_by_alt_time(
            'gamma_perp_mer.txt', alt, dn
                         ), dn
        )
    
    mean1 = local.resample('1H').mean()
    
    for i, col in enumerate(names):
        
        mean1[col] = mean1[col] / mean1['all']
        
        ax[i, j].plot(
            mean1[col] * 100, 
            marker = markers[i], 
            label = rt_labels[i], 
            )
        
        ax[i, j].set( 
               ylim = [-20 , 120], 
               xlim = [local.index[0], 
                       local.index[-1]])
        
        

fig.text(0.07, 0.3, 
         'Weighted parameters percent (\%)', 
         rotation = 'vertical', 
         fontsize = 25)

for i in range(3):
    ax[i, 1].legend(
        bbox_to_anchor = (.5, 1.3), 
        ncol = 2, 
        loc = 'upper center')
    s.format_time_axes(ax[2, i], hour_locator = 2)
    
    
for i, ax in enumerate(ax.flat):
    letter = s.chars()[i]
    ax.axhline(0, linestyle = '--')
    ax.axhline(100, linestyle = '--')
    ax.text(
        0.04, 0.85, f"({letter})", 
        transform = ax.transAxes
        )
    