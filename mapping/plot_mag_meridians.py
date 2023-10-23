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
    
   
    
    color = ['k'] #'blue', 

    for i, site in enumerate([ "saa"]): #"jic",
        
        glat, glon = gg.sites[site]["coords"]
        name = gg.sites[site]["name"]
        
        ax.scatter(glon, glat,
            marker = "*", 
            s = 300,
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
            s = 300, 
            c = color[i],
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
            color = line.get_color()
            )
        
        # ax.legend(ncol = 2)
        
        

def plot_mag_meridians(
        ax,
        year = 2021
        ):

 
    # ax = plt.axes(projection =  ccrs.PlateCarree())

    gg.map_features(ax)

    lat = gg.limits(
        min = -15, 
        max = 10, 
        stp = 5
        )
    lon = gg.limits(
        min = -60, 
        max = -30, 
        stp = 5
        )    

    gg.map_boundaries(ax, lon, lat)
    
    plot_sites_and_meridians(ax, year)
    
    gg.mag_equator(
        ax,
        year,
        degress = None
        )
    
   
    ax.legend(
        bbox_to_anchor = (.5, 1.15),
        ncol = 2, 
        loc = "upper center"
        )

    return ax


# fig, ax = plt.subplots(
#     dpi = 400,
#     figsize = (7,7),
#     subplot_kw = 
#         {
#         'projection': ccrs.PlateCarree()
#         }
#     )
# fig = plot_mag_meridians(ax, year = 2013)