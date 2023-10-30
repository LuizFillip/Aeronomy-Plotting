import RayleighTaylor as rt
import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels()

# letter = b.chars()[i]

# ax[i].text(
#     0.02, 0.87, 
#     f"({letter}) {titles[i]} ({c} events)", 
#     transform = ax[i].transAxes
#     )




fig, ax = plt.subplots(
    dpi = 300, 
    sharex = True,
    sharey = True,
    figsize = (12, 6)
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
    
