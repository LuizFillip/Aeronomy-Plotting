import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np

b.config_labels()

def plot_sites_and_meridians(
        ax, 
        year = 2013
        ):
    
    mlat = Apex(300).apex_lat_base(base = 75)

    rlat = np.degrees(mlat)
    
    gg.mag_equator(
        ax,
        year,
        degress = None
        )
    
    color = ['blue', 'g']

    for i, site in enumerate(["jic", "saa"]):
        
        glat, glon = gg.sites[site]["coords"]
        name = gg.sites[site]["name"]
        
        ax.scatter(glon, glat,
            marker = "o", 
            s = 100,
            label = name,
            c = color[i]
            )
    
        nx, ny, x, y = gg.load_meridian(year, site)
        
        x = sorted(x)
        
        x, y = gg.interpolate(
             x, y, 
             points = 50
             )
        
        line, = ax.plot(x, y, color = color[i])

        ax.scatter(nx, ny,
            marker = "^", 
            s = 100, 
            c = color[i]
            )
        
        
        x1, y1 = gg.limit_hemisphere(
                x, y, nx, ny, rlat, 
                hemisphere = 'both'
                )
        
        ax.plot(x1, y1, linestyle = '--', lw = 3, 
                color = line.get_color())
        
        

def plot_mag_meridians(
        year = 2021
        ):
    
 
    
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
        max = 5, 
        stp = 10
        )
    lon = gg.limits(
        min = -90, 
        max = -30, 
        stp = 10
        )    

    gg.map_boundaries(ax, lon, lat)
    
    plot_sites_and_meridians(ax, year)
    
    # ax.axhline(0, lw = 2, color = 'r', linestyle = '--')
    
    ax.legend(
        bbox_to_anchor = (.5, 1.1),
        ncol = 2, 
        loc = "upper center"
        )
        
    return fig 


fig = plot_mag_meridians(
        year = 2013
        )



 
