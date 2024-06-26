import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np


b.config_labels(fontsize = 35)

def total_B(ax, xy, xytext):

    ax.annotate(
        '$\\vec{B}$', xy=xy, 
        xytext=xytext,
        arrowprops=dict(
            color = 'red',
            lw = 4,
            arrowstyle='<-'), 
        transform = ax.transData, 
        fontsize = 40, 
        color = 'red')
    return None 

def vectors(ax, xy):
    arrowprops=dict(
        color = 'blue',
        lw = 4,
        arrowstyle='<-')
    
    x, y = xy[0] - 1, xy[1] - 1
    offset = 12
    xe = x + offset
    ye = y + offset
    
    ax.annotate(
        '$\\vec{U}_\\theta$'
        , xy=xy, 
        xytext=(x, ye),
        arrowprops=arrowprops, 
        transform = ax.transData, 
        fontsize = 40, 
        color = 'blue'
        )
    
    
    
    ax.annotate(
        '$\\vec{U}_\phi$', 
        xy=xy, 
        xytext=(xe, y),
        arrowprops=arrowprops, 
        transform = ax.transData, 
        fontsize = 40, 
        color = 'blue'
        )
    
    
    
    ax.annotate(
        '$\\vec{H}$', 
        xy=xy, 
        xytext=(xe, ye),
        arrowprops=dict(
            color = 'orange',
            lw = 4,
            arrowstyle='<-'), 
        transform = ax.transData, 
        fontsize = 40, 
        color = 'orange'
        )
    
    ax.legend()
    
    return None 

def plot_meridian(
        ax, 
        year = 2013
        ):
    
    mlat = Apex(300).apex_lat_base(base = 75)

    rlat = np.degrees(mlat)
    

    # for i, site in enumerate([ "saa"]): 
    site = 'saa'
    
    glat, glon = gg.sites[site]['coords']  
 
    ax.scatter(glon, glat,  s = 400, 
                marker = 's', c = 'red', 
                label = 'São Luís')
        
    nx, ny, x, y = gg.load_meridian(year, site)
    
    x = sorted(x)
    
    
    
    x, y = gg.interpolate(
         x, y, 
         points = 50
         )
    
    line, = ax.plot(x, y, color = 'k', 
                    lw = 2,
    label = 'Meridiano magnético')

    
    x1, y1 = gg.limit_hemisphere(
            x, y, nx, ny, rlat, 
            hemisphere = 'both'
            )
    
    total_B(ax, (nx, ny), (min(x1) - 1.2, max(y1) + 2))
    vectors(ax, (glon, glat))
    # ax.plot(
    #     x1, y1, 
    #     linestyle = '--', 
    #     lw = 3, 
    #     color = line.get_color()
    #     )
        
    return None        


def plot_mag_meridians(
        ax = None, 
        year = 2013
        ):
    
    if ax is None:
        fig, ax = plt.subplots(
            dpi = 300,
            figsize = (14, 14),
            subplot_kw = {'projection': ccrs.PlateCarree()}
            )
    
    lat_lims = dict(min = -20, max = 20, stp = 5)
    lon_lims = dict(min = -60, max = -25, stp = 5) 

    gg.map_attrs(
        ax, year, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims,
        grid = False,
        degress = None
        )
    
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
    if ax is None:
        return fig

fig = plot_mag_meridians( year = 2013)


fig.savefig(b.LATEX(
    'WindProjections2', folder = 'modeling'), dpi = 400)
plt.show()