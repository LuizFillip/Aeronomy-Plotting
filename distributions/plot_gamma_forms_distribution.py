import RayleighTaylor as rt

import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()




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




def plot_gamma_forms(ax, df):
    

    lb = rt.EquationsFT()
    
    steps = [0.1, 0.1, 0.1]
    cols = ['gravity', 'winds', 'drift']
    
    lbs = [lb.gravity, lb.winds, lb.drift]

    for i, gamma in enumerate(cols):
    
        step = steps[i]
        c = plot_distribution(
            ax, 
            df,
            label = lbs[i],
            step = step, 
            col_gamma = gamma,
            col_epbs = '-50'
            )
        
    infos = ('EPB occurrence\n' +
              f'{c} events')
         
    ax.text(0.79, 0.3, infos, 
             transform = ax.transAxes)
    
    
    ax.set(
           ylim = [-0.2, 1.2],
           yticks = np.arange(0, 1.25, 0.25)
           )
    
for i, ds in enumerate(
        ev.solar_flux_cycles(df)
        ):
    
    plot_gamma_forms(ax[i], ds)
    
    ax[i].set(title = cycles[i])
    

ax[0].legend(
        ncol = 3, 
        bbox_to_anchor = (.5, 1.5),
        loc = "upper center"
        )

fontsize = 25
fig.text(
    0.03, 0.35, 
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

fig.suptitle(f'$Kp > ${kp}', y = 1.01)