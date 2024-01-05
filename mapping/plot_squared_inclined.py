import cartopy.crs as ccrs
import GEO as gg
import base as b 
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import PlasmaBubbles as pb
import datetime as dt

b.config_labels()

     

def rectangle(ax, longitudes, latitudes):
    
    square = Polygon(zip(longitudes, latitudes))
    
    x, y = square.exterior.xy
    
    ax.add_patch(plt.Polygon(
        list(zip(x, y)),
        transform=ccrs.PlateCarree(), 
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
        

def mappping(year = 2014):
    fig, ax = plt.subplots(
        dpi = 300,
        figsize=(8, 8),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )
    
    plt.subplots_adjust(wspace = 0.1)
    
    gg.map_attrs(ax, year)
   
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


year = 2014

fig, ax = mappping(year = 2014)


plot_corners(
        ax,
        year,
        radius = 10,
        label = False
        )


dn = dt.datetime(2013, 1, 14, 23)

df = pb.concat_files(dn, root = 'D:\\')

ds = b.sel_times(df, dn, hours = 1)

img = ax.scatter(
    ds['lon'],
    ds['lat'],
    c = ds['roti'],
    s = 10,
    cmap = 'jet',
    vmin = 0,
    vmax = 3
)    