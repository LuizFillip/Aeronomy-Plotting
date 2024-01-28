import pandas as pd
import matplotlib.pyplot as plt
import base as b 
import GEO as gg
import os
import datetime as dt 
import RayleighTaylor as rt

b.config_labels(fontsize = 25)

PATH_FT = 'FluxTube/data/reduced/'

def plot_growth_rate_parameters():

    
   
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
    
    for i, ax in enumerate(ax.flat):
        ax.axhline(300)
        ax.axvline(0)
        ax.set(ylim = [200, 550], 
               xlim = [-30, 30])
    
        letter = b.chars()[i]
        ax.text(
            0.04, 0.95, f"({letter}) ", 
            transform = ax.transAxes
            )
    
    fig.suptitle('Comparação entre os perfis locais e integrados')

    return fig

def plot_single_parameters(ax, ds):
    

    cols = ['gr', 'K', 'mer_parl', 'ratio']
    ylabel = ['$g / \\nu_{eff}$', '$K^F$',
              '$U_L$', '$\Sigma_F$']
    
    
    for i, ax in enumerate(ax.flat):
        
        ax.plot(ds[cols[i]])
        
        ax.set(ylabel = ylabel[i])
        
        if i >= 2:
        
            b.axes_month_format(ax)


                             

fig, ax = plt.subplots(
    nrows = 5,
    figsize = (14, 8),
    sharex = True,
    dpi = 300
    )

plt.subplots_adjust(wspace = 0.2)


df = b.load('20131224tlt.txt')

df['vp'] = 25
ds = rt.gammas_integrated(df)

ds