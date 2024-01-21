import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import base as b
from FluxTube import Apex
import numpy as np
import pandas as pd 


b.config_labels(fontsize = 25)

def plot_meridian_range(
        ax,x, y, nx, ny, rlat = 12):

    x1, y1 = gg.limit_hemisphere(
            x, y, nx, ny, rlat, 
            hemisphere = 'both'
            )
    
    ax.plot(
        x1, y1, 
        linestyle = '--', 
        lw = 3, 
        label = 'Meridiano magnético'
        )

def plot_meridian(
        ax, 
        year = 2013
        ):
    
    mlat = Apex(300).apex_lat_base(base = 75)

    rlat = np.degrees(mlat)
    

    for i, site in enumerate([ "saa"]): #"jic",
    
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
        
        
        
    return None        

def plot_electron_density(ax):
    
    df = pd.read_csv('models/temp/map_iri.txt', index_col = 0)

    df = pd.pivot_table(
        df, 
        columns = '0', 
        index = '1', 
        values = '2')

    vls = df.values *1e-12
    
    
    ticks = np.linspace(
    np.nanmax(vls), 
    np.nanmin(vls), 10)
    
    
    
    img = ax.contourf(
        df.columns, 
        df.index, 
        vls, 50,
        cmap = 'jet'     
        )
    
    
    b.colorbar(img, ax, ticks, label = '$N_e (\\times 10^{12}~ m^{-3})$')
    
    return 
def plot_mag_meridians(
        year = 2013
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    lat_lims = dict(min = -30, max = 18, stp = 10)
    lon_lims = dict(min = -80, max = -30, stp = 10) 

    gg.map_attrs(
        ax, year, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims,
        grid = False,
        degress = None)
    
    plot_electron_density(ax)
    
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

fig = plot_mag_meridians(year = 2013 )

# fig.savefig(
#     b.LATEX(FigureName, folder = 'profiles'),
#     dpi = 400
#     )


