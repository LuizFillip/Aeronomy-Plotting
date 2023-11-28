import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import GEO as gg
import GNSS as gs 
import os 
import PlasmaBubbles as pb 
import base as b 

b.config_labels()
def mapping(year = 2013):
    
    
    
    lat_lims = dict(
        min = -25, 
        max = 15, 
        stp = 5
        )
    
    lon_lims = dict(
        min = -90,
        max = -30, 
        stp = 10
        )    
    
    fig, ax = gg.quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (9, 9), 
        year = year, 
        degress = None
        )
    
    return ax
     



def plot_corners(
        ax,
        year
        ):
    
    coords = gg.corner_coords(
            year, 
            radius = 5, 
            angle = 45
            )

    x_limits, y_limits = coords[0], coords[1]

    for i in range(len(x_limits)):
        xlim, ylim = x_limits[i], y_limits[i]
            

        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )
        


year = 2013
ax = mapping(year)


plot_corners(
        ax,
        year
        )