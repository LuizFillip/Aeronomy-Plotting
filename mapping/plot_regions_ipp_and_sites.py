import cartopy.crs as ccrs
import GEO as gg
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb
import datetime as dt
import numpy as np 
import os 


b.config_labels(fontsize = 35)

def load_data(dn, root = 'D:\\'):
    
    df = pb.concat_files(dn, root)
    
    return b.sel_times(df, dn, hours = 0.5)
    
sites = ['car',  'for', 'saa'] 
names = [ 'Imageador (Cariri)', 
          'Ionossonda (Fortaleza)', 
          'Ionossonda (São Luis)'   ]  

def load_dataw(dn, file):
    
 
    df = pb.load_filter(file)
    
    
    return b.sel_times(df, dn, hours = 0.01)


def plot_regions_ipp_and_sites(dn):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    
    gg.map_attrs(ax, dn.year, grid = False)
    
    infile = 'D:\\database\\GNSS\\001\\'
    
    for fn in  os.listdir(infile):
    
        file = os.path.join(infile, fn)
        
        ds = load_dataw(dn, file)
         
        img = ax.scatter(
                ds['lon'],
                ds['lat'],
                c = ds['roti'],
                s = 50,
                cmap = 'jet',
                vmin = 0,
                vmax = 2
            )       
    
    ticks = np.arange(0, 2, 0.5)
    b.colorbar(img, ax, ticks)
    fmt = dn.strftime('%Hh00 - %Hh01 UT') 
    
    c = ['red', 'green', 'magenta']
    for i, site in enumerate(sites):
        
        glat, glon = gg.sites[site]['coords']
        
        ax.scatter(glon, glat, s = 250,
                   c = c[i], marker = 's', 
                   label = names[i])
    
    
    ax.set(title = fmt)
    
    lon, lat = gg.terminator2(dn, 18)
    
    ax.plot(lon, lat, color = 'k', lw = 4, linestyle = '--')
   
    gg.plot_square_area(
            ax, 
            lat_min = -12, 
            lon_min = -42,
            lat_max = None, 
            lon_max = None, 
            radius = 10, 
            )
    plt.show()
    return fig

def main():
    
    dn = dt.datetime(2013, 12, 24, 23)
    
    fig = plot_regions_ipp_and_sites(dn)
    
    FigureName = 'regions_and_ipp'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'maps'),
        dpi = 400
        )

# dn = dt.datetime(2021, 1, 1, 7)

# fig = plot_regions_ipp_and_sites(dn)


