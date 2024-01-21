import os
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import plotting as pl
import matplotlib.pyplot as plt
import matplotlib as mpl



def plot_colorbar(
        fig,
        vmin, 
        vmax, 
        rainbow = "jet",
        fontsize = 25,
        step = 10):
    
    norm = mpl.colors.Normalize(
        vmin = vmin, vmax=vmax
        )
    
    label = r'TEC ($10^{16} / m^2$)'
    cax = plt.axes([0.2, 1.001, 0.6, 0.02])
   
    cb = fig.colorbar(
        mpl.cm.ScalarMappable(
            norm = norm, 
            cmap = rainbow
            ),
        ticks = np.arange(vmin, vmax + step, step),
        cax = cax, 
        orientation = "horizontal", 
        )
    cb.set_label(label, fontsize = fontsize)



def plot_multiple_tec_maps(start):
    

    fig, ax = plt.subplots(
         figsize = (17, 12), 
         dpi = 300, 
         ncols = 3, 
         nrows = 2,
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(
        wspace = 0.1, 
        hspace = 0.3
        )
        
    for hour, ax in enumerate(ax.flat):
        
        dn = start + dt.timedelta(hours = hour)
        
        pl.plot_tec_map(
            dn, ax = ax, vmax = 100, 
            colorbar = False)
        
        ax.set(title = dn.strftime('%Hh%M UT'))
        
        if hour != 0:
            ax.set(xticklabels = [], 
                   yticklabels = [], 
                   xlabel = '', 
                   ylabel = '')
    
    
    plot_colorbar(
            fig,
            vmin = 0, 
            vmax = 60
            )
    return fig 


start =  dt.datetime(2014, 2, 9, 23, 0)