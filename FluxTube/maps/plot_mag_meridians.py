import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np


b.config_labels(fontsize = 25)

def plot_meridian(
        ax, 
        year = 2013
        ):
    
    mlat = Apex(300).apex_lat_base(base = 75)

    rlat = np.degrees(mlat)
    

    for i, site in enumerate([ "saa"]): 
    
        glat, glon = gg.sites[site]['coords']  
        # print(glat, glon)
        ax.scatter(glon, glat,  s = 300, 
                   marker = '^', c = 'b', 
                   label = 'São Luís')
            
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
            c = 'r',
            label = 'Intersecção com o Equador'
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
            label = 'Meridiano magnético'
            )
        
    return None        


def plot_mag_meridians(
        year = 2013
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    lat_lims = dict(min = -20, max = 20, stp = 10)
    lon_lims = dict(min = -55, max = -30, stp = 10) 

    gg.map_attrs(
        ax, year, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims,
        grid = False,
                 degress = None)
    
    plot_meridian(ax, year)
    
    gg.mag_equator(
        ax,
        year,
        degress = None
        )
    
   
    ax.legend(
        ncol = 1, 
        loc = "upper right"
        )

    return fig

fig = plot_mag_meridians(
        year = 2013
        )