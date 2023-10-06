import os
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import GEO as gg
import base as b 

b.config_labels(fontsize = 25)


    
def plot_colorbar(
        fig,
        rainbow = "rainbow",
        fontsize = 40
        ):
    
    norm = mpl.colors.Normalize(
        vmin = 0, vmax=80
        )
   
    cax = plt.axes([0.2, 1.001, 0.6, 0.02])
         
    cb = fig.colorbar(
        mpl.cm.ScalarMappable(
            norm = norm, 
            cmap = rainbow
            ),
        ticks = np.arange(0, 80, 10),
        cax = cax, 
        orientation = "horizontal", 
        )
    cb.set_label(r'TEC ($10^{16} / m^2$)', fontsize = fontsize)
    


    
    


def plot_tec_map():

    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (9, 9),
        subplot_kw = 
            {
            'projection': ccrs.PlateCarree()
            }
        )

    gg.map_features(ax)

    lat = gg.limits(
        min = -40, 
        max = 10, 
        stp = 10
        )
    lon = gg.limits(
        min = -80, 
        max = -30, 
        stp = 10
        )    

    gg.map_boundaries(ax, lon, lat)
        
    gg.mag_equator(
        ax,
        2021,
        degress =  None
        )
                
    return ax







    
ax = plot_tec_map()

x = (-60, -50)
y = (2, -10)

ax.scatter(x[0], y[0], s = 100, c = 'k')

ax.scatter(x[1], y[1], s = 100, c = 'k')

m = (y[1] - y[0]) / (x[1] - x[0]) 

ax.annotate(
    '', 
    xy = (x[0], y[0]), 
    xytext = (x[1], y[1]), 
    arrowprops = dict(arrowstyle='<->', lw = 2)
    )


ax.scatter(x[0], y[0], s = 100, c = 'k')

ax.scatter(m*x[0], m*y[0], s = 100, c = 'k')

m*x[0], m*y[0]