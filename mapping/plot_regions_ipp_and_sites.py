import cartopy.crs as ccrs
import GEO as gg
import base as b 
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import PlasmaBubbles as pb
import datetime as dt
import plotting as pl 


b.config_labels()

def load_data(dn, root = 'D:\\'):
    
    df = pb.concat_files(dn, root)
    
    return b.sel_times(df, dn, hours = 0.5)
    

def rectangle(ax, longitudes, latitudes):
    
    square = Polygon(zip(longitudes, latitudes))
    
    x, y = square.exterior.xy
    
    ax.add_patch(plt.Polygon(
        list(zip(x, y)),
        transform = ccrs.PlateCarree(), 
        color = 'red', 
        alpha = 0.5)
        )

def plot_corners(
        ax,
        year,
        radius = 10,
        label = False
        ):
    
    coords = gg.corner_coords(
            year, 
            radius, 
            angle = 45
            )

    x_limits, y_limits = coords[0][::-1], coords[1][::-1]
    
    out = {}

    for i in range(len(x_limits)):
        index = i + 1
        
        xlim, ylim = x_limits[i], y_limits[i]
        
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )
                
        if label:
            
            clon = sum(list(set(xlim))) / 2
            
            ax.text(clon, max(ylim) + 1, index, 
                    transform = ax.transData)
        
        x_values = sorted(list(set(xlim)))
        y_values = sorted(list(set(ylim)))
        
        out[index] = (x_values, y_values)
    
    return out
        

def mappping():
    fig, ax = plt.subplots(
        dpi = 300,
        ncols = 2, 
        sharex = True, 
        figsize = (12, 12),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    plt.subplots_adjust(wspace = 0.1)
    
    return fig, ax

def plot_terminator_and_equator(
        ax, dn, twilight = 18):
 
    eq_lon, eq_lat  = gg.load_equator(
        dn.year, values = True)
    
    term_lon, term_lat = gg.terminator2(
        dn, twilight)
    
    ax.scatter(term_lon, term_lat, s = 10)
    
    inter_lon, inter_lat = gg.intersection(
        eq_lon, eq_lat, term_lon, term_lat)
    
    
    ax.scatter(inter_lon, inter_lat, s = 100, 
               marker = 'X', color = 'k')
    
    return eq_lon, eq_lat


def plot_regions_ipp_and_sites(dn):
    
    fig, ax = mappping()
    
    
    sites = ['saa', 'car', 'jic'] 
    names = ['Digisonde (São Luis)',  
             'Imager (Cariri)', 
             'Digisonde (Jicamarca)']  
    
    df = load_data(dn)
    
    for i in range(2):
        
       gg.map_attrs(ax[i], dn.year)
       
       corners = plot_corners(
               ax[i],
               dn.year,
               radius = 10,
               label = False 
               )
    
       gg.plot_sites_markers(ax[i], sites, names)
       
       l = b.chars()[i]
       ax[i].text(0.05, 0.9, f'({l})', fontsize = 20,
                  transform = ax[i].transAxes)
       
    pl.plot_ipp_on_map(ax[1], df, corners)
       
    gg.stations_near_of_equator(
        ax[0],
         dn.year,
         distance = 5, 
         extra_sts = [])
        
    ax[1].set(ylabel = '', 
           yticklabels = [])
    
    
    ax[0].legend(loc = 'upper center',
                 ncol = 3, 
                 bbox_to_anchor = (1.05, 1.2), 
                 columnspacing = 0.2)
    
    plt.show()
    
    return fig


dn = dt.datetime(2013, 1, 14, 23)

fig = plot_regions_ipp_and_sites(dn)

FigureName = 'regions_and_ipp'

fig.savefig(
    b.LATEX(FigureName, folder = 'maps'),
    dpi = 400
    )