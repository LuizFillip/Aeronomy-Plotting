import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np
import pandas as pd 
import datetime as dt

b.config_labels(fontsize = 25)


def limit_hemisphere(
        x, 
        y, 
        nx, ny, 
        rlat = 0, 
        hemisphere = 'both'
        ):
    
    """
    Get range limits in each hemisphere by 
    radius (in degrees)
    
    """    
    # find meridian indexes (x and y) 
    # where cross the equator and upper limit
    eq_x = gg.find_closest(x, nx)  
    eq_y = gg.find_closest(y, ny)  

    # create a line above of intersection point 
    # with radius from apex latitude 
    if hemisphere == "south":
        end = gg.find_closest(y, ny - rlat)
        set_x = x[eq_x: end + 2]
        set_y = y[eq_y: end + 2]
    
    elif hemisphere == "north":
        start = gg.find_closest(y, ny + rlat)
        set_x = x[start: eq_x + 1]
        set_y = y[start: eq_y + 1]
        
    else:
        end = gg.find_closest(y, ny - rlat) - 1
        start = gg.find_closest(y, ny + rlat) + 3
      
        set_x = x[start: end]
        set_y = y[start: end]
        
    return set_x, set_y

def plot_meridian_range(
        ax,x, y, nx, ny, rlat = 12):

    x1, y1 = limit_hemisphere(
            x, y, nx, ny, rlat, 
            hemisphere = 'north'
            )
    
    ax.plot(
        x1, y1, 
        linestyle = '--', 
        lw = 3, 
        color = 'k'
        )
    
    x1, y1 = limit_hemisphere(
            x, y, nx, ny, rlat, 
            hemisphere = 'south'
            )
    
    ax.plot(
        x1, y1, 
        linestyle = '--', 
        lw = 3, 
        label = 'Alcance em 300 km'
        )
    
def plot_all_meridians(ax, year):
    
    dn = dt.datetime(year, 1, 1)
    mer = gg.meridians(dn, delta = 5)
    
    glat, glon = gg.sites['saa']['coords']
    
    meridian = mer.range_meridians()
    
    for num in range(meridian.shape[0]):
        
        x, y = meridian[num][0], meridian[num][1]
        
        ax.plot(x - 0.1, y - 1.8, lw = 1, color = 'k')

def plot_meridian(
        ax, 
        year = 2013
        ):
    
    mlat = Apex(300).apex_lat_base(base = 75)

    rlat = np.degrees(mlat)
    
    plot_all_meridians(ax, year)
    
    for i, site in enumerate([ "saa"]): 
    
        glat, glon = gg.sites[site]['coords']  

        ax.scatter(glon, glat,  s = 300, 
                    marker = 's', c = 'r')
            
        nx, ny, x, y = gg.load_meridian(year, site)
        
        x = sorted(x)
        
        x, y = gg.interpolate(
             x, y, 
             points = 50
             )
        
        line, = ax.plot(x, y, color = 'r', lw = 2)
        
        plot_meridian_range(
                ax,x, y, nx, ny, rlat)

        ax.scatter(nx, ny,
            marker = "^", 
            s = 300, 
            c = 'r',
            label = 'Intersecção com o Equador'
            )
    
    return None        

def plot_electron_density(ax):
    
    df = pd.read_csv('models/temp/map_iri.txt', index_col = 0)

    df = pd.pivot_table(
        df, 
        columns = '0', 
        index = '1', 
        values = '2')

    vls = df.values *1e-12
    
    img = ax.contourf(
        df.columns, 
        df.index, 
        vls, 50,
        cmap = 'rainbow'     
        )
    
    ticks = np.arange(0, 2, 0.01)
    
    b.colorbar(img, ax, ticks, 
               label = '$N_e (\\times 10^{12}~ m^{-3})$')
    
    return 
def plot_mag_meridians(
        year = 2013
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    lat_lims = dict(min = -30, max = 15, stp =  5)
    lon_lims = dict(min = -80, max = -30, stp = 10) 

    gg.map_attrs(
        ax, year, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims,
        grid = False,
        degress = None
        )
    
    plot_electron_density(ax)
    
    # gg.plot_rectangles_regions(ax, year)
    
    plot_meridian(ax, year)
    
    gg.mag_equator(
        ax,
        year,
        degress = None
        )
    
    ax.legend(
        ncol = 2, 
        loc = "upper right",
        columnspacing = 0.5,
        bbox_to_anchor = (1.2, 1.1)
        )

    return fig

# fig = plot_mag_meridians(year = 2013)

# fig.savefig(
#     b.LATEX(FigureName, folder = 'profiles'),
#     dpi = 400
#     )


