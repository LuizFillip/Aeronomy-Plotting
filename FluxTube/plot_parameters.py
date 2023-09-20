import pandas as pd
import matplotlib.pyplot as plt
import base as b 


def plot_int_profiles():
    
    fig, ax = plt.subplots(
        ncols = 2, 
        figsize = (10, 8),
        sharey = True,
        dpi = 300
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    
   
    ax[0].legend(   
        bbox_to_anchor = (1., 1.1), 
        ncol = 3, 
        loc = 'upper center'
        )
    
    ax[0].set(
        xlabel = '$\gamma_{FT} ~(10^{-4}~s^{-1})$', 
        ylabel = 'Altura de apex (km)'
        )
    
    ax[1].set(
        ylabel = 'Altura local (km)',
        xlabel = '$\gamma_{RT} ~(10^{-4}~s^{-1})$'
        )
    
    integrated = rt.EquationsFT().complete()
    
    names = [integrated, local_l]
    for i, ax in enumerate(ax.flat):
        ax.axhline(300)
        ax.axvline(0)
        ax.set(ylim = [200, 550], 
               xlim = [-30, 30])
    
        letter = s.chars()[i]
        ax.text(
            0.04, 0.95, f"({letter}) {names[i]}", 
            transform = ax.transAxes
            )
    
    fig.suptitle('Comparação entre os perfis locais e integrados')

    return fig


# fig = plot_int_profiles()



fig, ax = plt.subplots(
    ncols = 2, 
    nrows = 2,
    figsize = (14, 8),
    sharex = True,
    dpi = 300
    )

plt.subplots_adjust(wspace = 0.1)


site = 'saa'

def plot_site(ax, site):
    
    infile  = f'database/tests/{site}.txt'
    
    ds = b.load(infile)
    
    ds['gr'] = ds['ge'] / ds['nui']
    
    #['F', 'E']
    cols = ['gr', 'K', 'mer_parl', 'ratio']
    
    for i, ax in enumerate(ax.flat):
        
        ax.plot(ds[cols[i]])
        
        if i >= 2:
        
            b.format_time_axes(ax)


plot_site(ax, 'saa')

plot_site(ax, 'jic')