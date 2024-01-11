import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np
# from plotting import (
#     plot_receivers_coords
#     )
b.config_labels()

def plot_meridian(
        ax, 
        year = 2013
        ):
    
    mlat = Apex(300).apex_lat_base(base = 75)

    rlat = np.degrees(mlat)
    

    for i, site in enumerate([ "saa"]): #"jic",
          
        nx, ny, x, y = gg.load_meridian(year, site)
        
        x = sorted(x)
        
        x, y = gg.interpolate(
             x, y, 
             points = 50
             )
        
        line, = ax.plot(x, y, color = 'k')

        ax.scatter(nx, ny,
            marker = "^", 
            s = 300, 
            c = 'k',
            label = 'Equator intersection'
            )
        
        
        x1, y1 = gg.limit_hemisphere(
                x, y, nx, ny, rlat, 
                hemisphere = 'both'
                )
        
        ax.plot(
            x1, y1, 
            linestyle = '--', 
            lw = 3, 
            color = line.get_color(), 
            label = 'Magnetic meridian'
            )
        
    ax.legend()
        


def plot_mag_meridians(
        ax,
        year = 2013
        ):


    gg.map_features(ax, grid = False)

    lat = gg.limits(
        min = -15, 
        max = 10, 
        stp = 10
        )
    lon = gg.limits(
        min = -60, 
        max = -20, 
        stp = 10
        )    

    gg.map_boundaries(ax, lon, lat)
    
    plot_meridian(ax, year)
    
    gg.mag_equator(
        ax,
        year,
        degress = None
        )
    
   
    ax.legend(
        bbox_to_anchor = (.5, 1.2),
        ncol = 1, 
        loc = "upper right"
        )

    return ax

def main():
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (9, 9),
        subplot_kw = 
            {
            'projection': ccrs.PlateCarree()
            }
        )
    
    year = 2013
    ax = plot_mag_meridians(ax, year)
    
    # rec = plot_receivers_coords(
    #         ax, 
    #         year, 
    #         distance = None,
    #         text = True
    #         )