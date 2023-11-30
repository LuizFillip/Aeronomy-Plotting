import cartopy.crs as ccrs
import GEO as gg
import base as b 
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import datetime as dt 
b.config_labels()


def mapping(year = 2013):
    
    lat_lims = dict(
        min = -25, 
        max = 15, 
        stp = 5
        )
    
    lon_lims = dict(
        min = -90,
        max = -30, 
        stp = 10
        )    
    
    fig, ax = gg.quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (9, 9), 
        year = year, 
        degress = None
        )
    
    
    return ax
     

def plot_rectangle(ax, longitudes, latitudes):
    
    square = Polygon(zip(longitudes, latitudes))
    
    x, y = square.exterior.xy
    
    # Plot the square on the map
    ax.add_patch(plt.Polygon(
        list(zip(x, y)),
        transform=ccrs.PlateCarree(), 
        color='red', alpha=0.5))

def plot_corners(
        ax,
        year,
        ilon, 
        radius = 10
        ):
    
    coords = gg.corner_coords(
            year, 
            radius, 
            angle = 45
            )

    x_limits, y_limits = coords[0], coords[1]

    for i in range(len(x_limits)):
        
        xlim, ylim = x_limits[i], y_limits[i]
        
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )
        
        
        
        clat = sum(list(set(ylim))) / 2
        clon = sum(list(set(xlim))) / 2
        
        ax.scatter(clon, clat, s = 50, color = 'k')
        if clon > ilon:
            plot_rectangle(ax, xlim, ylim)
        
        




def map_attrs(ax, year):
    
    gg.map_features(ax)
    
    lat = gg.limits(
        min = -30, 
        max = 20, 
        stp = 10
        )
    
    lon = gg.limits(
        min = -90, 
        max = -20, 
        stp = 10
        )    
    
    gg.map_boundaries(ax, lon, lat)
    
    
    x, y = gg.mag_equator(
        ax,
        year,
        degress = None
        )
    
    return x, y


def plot_terminator(ax, dn, elon, elat):    
    lon, lat = gg.terminator(dn, 18)
    
    ilon, ilat = gg.intersection(elon, elat, lon, lat)
    
    ax.plot(lon, lat, lw = 2, linestyle = '--')
    
    return ilon

fig, ax = plt.subplots(
    dpi = 300,
    figsize = (9, 9),
    subplot_kw = 
        {
        'projection': ccrs.PlateCarree()
        }
    )



dn = dt.datetime(2014, 1, 1, 23)


df = b.load(
    pb.epb_path(
        dn.year, 
        path = 'events'
        )
    )

ds = b.sel_times(df, dn)

elon, elat = map_attrs(ax, dn.year)


ilon = plot_terminator(ax, dn, elon, elat)

plot_corners(ax, dn.year, ilon[0], radius = 5)