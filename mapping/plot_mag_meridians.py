import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np

b.config_labels()

def plot_sites(ax, year = 2013):
    
    gg.mag_equator(ax,
                  year,
                  degress=None
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
        
        line, = ax.plot(x, y, color = color[i])

        ax.scatter(nx, ny,
            marker = "^", 
            s = 100, 
            c = color[i]
            )
        
        mlat = Apex(300).apex_lat_base(base = 75)

        rlat = np.degrees(mlat)

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
        figsize = (8, 8),
        subplot_kw = 
            {
            'projection': ccrs.PlateCarree()
            }
        )

    gg.map_features(ax)

    lat = gg.limits(
        min = -25, 
        max = 15, 
        stp = 10
        )
    lon = gg.limits(
        min = -85, 
        max = -30, 
        stp = 10
        )    

    gg.map_boundaries(ax, lon, lat)
    
    plot_sites(ax, year)
    
    ax.set(title = f"{year}")
    ax.legend(ncol = 1, loc = "upper right")
        
    return fig 


fig = plot_mag_meridians(
        year = 2013
        )


#save_plot(plot_mag_meridians)

 
