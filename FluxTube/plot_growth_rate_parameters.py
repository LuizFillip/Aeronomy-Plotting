import pandas as pd
import matplotlib.pyplot as plt
import base as b 
import GEO as gg
import os
import datetime as dt 


b.config_labels()

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


# fig = plot_int_profiles()





def plot_single_parameters(ax, ds):
    

    cols = ['gr', 'K', 'mer_parl', 'ratio']
    ylabel = ['$g / \\nu_{eff}$', '$K^F$',
              '$U_L$', '$\Sigma_F$']
    
    
    for i, ax in enumerate(ax.flat):
        
        ax.plot(ds[cols[i]])
        
        ax.set(ylabel = ylabel[i])
        
        if i >= 2:
        
            b.axes_month_format(ax)

def set_dataset(
        year, 
        site, 
        time = dt.time(0, 0)
        ):

    infile  = os.path.join(
        PATH_FT,
        f'{site}/{year}.txt'
        )
    
    ds = b.load(infile)
    
    ds = ds.loc[ds.index.time == time]
    
    ds['gr'] = ds['ge'] / ds['nui']
    
    ds.column.name = gg.sites[site]['name']

    return ds
                             

fig, ax = plt.subplots(
    ncols = 2, 
    nrows = 2,
    figsize = (14, 8),
    sharex = True,
    dpi = 300
    )

plt.subplots_adjust(wspace = 0.2)



ds = set_dataset(2015, 'saa')

plot_single_parameters(ax, ds)

ds = set_dataset(2015, 'jic')

plot_single_parameters(ax, ds)



ax[0, 0].legend(bbox_to_anchor = (.5, 1.2), 
loc = "upper center", ncol = 2)