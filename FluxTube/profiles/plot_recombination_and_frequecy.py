# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:46:28 2024

@author: Luiz
"""

import plotting as pl 
import base as b
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import models as m 


b.config_labels(fontsize = 25)

lb = b.Labels().infos


names = ['Norte', 'Sul', 'Total']

def plot_collision_freq(ax, ds, col = 'nui'):
    
    symbol = lb[ col]['symbol']
    units = lb[col]['units']
    
    K = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col,  'nui'] 
         
        K.append(df)
        ax.plot(b.smooth2(df, 3), df.index, 
                label = names[i])
    
    total = pd.concat(K, axis = 1).dropna().sum(axis = 1)

    ax.plot(total, total.index, label = 'Total')
    
    ax.set(
        xlim = [-1, 13], 
        xlabel = f'{symbol} ({units})', 
        xticks = np.arange(0, 14, 2)
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')
    
    ax.legend(loc = 'upper right')
    return 


def plot_recombination(ax, ds):
    
    out = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col, 'R']
        out.append(df)
        ax.plot(df, df.index, 
                label = names[i])
    
    total = pd.concat(out, axis = 1).dropna().sum(axis = 1)

    ax.plot(total, total.index, 
            label  = names[-1])
    
    ax.set(
        ylabel = 'Altura de Apex',
        # xlim = [15, 20], 
        # xticks = np.arange(15, 21, 1),
        xlabel = "$N_0$ ($cm^{-2}$)"
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')
    
    
    # ax.legend(
    #     ncol = 3,
    #     # bbox_to_anchor = (1., 1.15),
    #     loc = "upper center"
    #     )



def plot_local_profiles(ax, ds):
    

    dn = ds['dn'].values[0]
   
    df = m.Equator_profiles(pd.to_datetime(dn))
    ax1 = ax[0].twiny()
    
    ax1.plot(
        df['ne'],
        df.index, 
        lw = 2,
        color = 'k', 
        linestyle = '--', 
        label = 'Perfil local no equador')
    
    ax1.set(xlabel = b.y_label('ne'))
    
    # 
    ax1.axvline(0, lw = 1, linestyle = ':')
    
    ax1 = ax[1].twiny()
    
    ax1.plot(
        df['L'] * 1e5,
        df.index, 
        color = 'k', 
        linestyle = '--', 
        lw = 2,
        label = 'Perfil local \nno equador')

    ax1.set(xlabel = b.y_label('L'), 
            ylim = [150, 500])
    
    ax1.axvline(0, lw = 1, linestyle = ':')
    ax1.legend(loc = 'center right')
    return 


def plot_ft_density_profiles(ds):
    '''
    This plot can be found in the subsection .. 
    in the chapter .. of the thesis
    
    '''
    fig, ax = plt.subplots(
        figsize = (12, 10),
        sharey = True,
        ncols = 2, 
        dpi = 300,
        
        )

    plt.subplots_adjust(wspace = 0.05)
    
    # plot_local_profiles(ax, ds)
    
    plot_recombination(ax[0], ds)
    
    plot_collision_freq(ax[1], ds)
    
    
    
    b.plot_letters(ax, y = 1.02, x = 0.01)
    return fig

ds = pl.load_fluxtube()

fig = plot_ft_density_profiles(ds)

# FigureName = 'electron_density_and_gradient'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'profiles'),
#     dpi = 400
#     )


