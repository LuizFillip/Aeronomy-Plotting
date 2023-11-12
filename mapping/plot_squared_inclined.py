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
        x_limits, y_limits
        ):
    

    ax.plot(
        x_limits,
        y_limits,
        color = 'black', 
        linewidth = 2, 
        transform = ccrs.PlateCarree() 
        )
    


# ax.scatter(ds.lon, ds.lat, c = ds.roti, s = 3)


# mapping(year = 2013)