import cartopy.crs as ccrs
import GEO as gg
import base as b 
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import datetime as dt 

b.config_labels()

     

def plot_rectangle(ax, longitudes, latitudes):
    
    square = Polygon(zip(longitudes, latitudes))
    
    x, y = square.exterior.xy
    
    # Plot the square on the map
    ax.add_patch(plt.Polygon(
        list(zip(x, y)),
        transform=ccrs.PlateCarree(), 
        color='red', alpha=0.5))
    
    
def middle_point(xlim, ylim):
     clat = sum(list(set(ylim))) / 2
     clon = sum(list(set(xlim))) / 2
     
     return clon, clat

    

def plot_corners(
        ax,
        year,
        radius = 10
        ):
    
    coords = gg.corner_coords(
            year, 
            radius, 
            angle = 45
            )

    x_limits, y_limits = coords[0], coords[1]
    
    out = {}

    for i in range(len(x_limits)):
        
        xlim, ylim = x_limits[i], y_limits[i]
        
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )
        
        clon, clat = middle_point(xlim, ylim)
        
        out[clon] = (xlim, ylim)
    
    return out
        
def find_closest(arr, val):
   return arr[np.abs(arr - val).argmin()]


def intersect_point( eq_lon, eq_lat, term_lon, term_lat):
    inter_lon, inter_lat = gg.intersection(
        eq_lon, eq_lat, term_lon, term_lat)
  
    
    return inter_lon, inter_lat





# df = b.load(
#     pb.epb_path(
#         year, path = 'events'
#         )
#     )

# ds = b.sel_times(df, dn)




def mappping(year):
    fig, ax = plt.subplots(
        dpi=300,
        figsize=(12,12),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )
    
    
    coords = plot_corners(ax, year, radius=5)
    gg.map_attrs(ax, year)
    
    return ax, coords

import numpy as np 

year = 2014

dn = dt.datetime(year, 1, 1, 7)
twilight = 18



ax, coords = mappping(year)
 
eq_lon, eq_lat  = gg.load_equator(year, values = True)

term_lon, term_lat = gg.terminator(dn, twilight)
ax.plot(term_lon, term_lat, lw = 2, linestyle = '--')

inter_lon, inter_lat = intersect_point(
    eq_lon, eq_lat, term_lon, term_lat)



inter_lat = inter_lat[:2]
inter_lon = inter_lon[:2]

# dusk = gg.dusk_time(
#         dn,  
#         lat = inter_lat[0], 
#         lon = inter_lon[0], 
#         twilight = twilight
#         )


ax.scatter(inter_lon, inter_lat, s = 80)


# clon = find_closest(list(coords.keys()), inter_lon)

# is_night = gg.is_night(inter_lon, inter_lat, dusk)

# ax.set(title = dusk.strftime("%H:%M:%S (UT)"))


# if is_night:
#     for lon in list(coords.keys()):
            
#         longitudes, latitudes = coords[lon]
        
#         clon, clat = middle_point(longitudes, latitudes)
        
#         if clon >= inter_lon:
#             plot_rectangle(ax, longitudes, latitudes)
            
# inter_lon