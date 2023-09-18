import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import json 
import numpy as np

def plot_annotate(
        axs, 
        name, 
        lon, 
        lat
        ):
 
     axs.annotate(
         name, 
         xy=(lon, lat),  
         xycoords='data',
         xytext=(lon - 100, lat + 10), 
         textcoords='offset points',
         arrowprops = dict(
             facecolor='black', arrowstyle="->"), 
         horizontalalignment='right',
         verticalalignment='top',
         transform = ccrs.Geodetic()
         )

def distance_from_equator(
        lon, lat, year = 2013
        ):
    eq = g.load_equator(year)
    x, y = eq[:, 0], eq[:, 1]
    min_x, min_y, min_d = g.compute_distance(
        x, y, lon, lat)
    return min_d

def plot_receivers(
        distance = 7,
        year = 2013
        ):
    
    
    fig, axs = plt.subplots(
        dpi = 300,
        figsize = (6, 6),
        subplot_kw={
            'projection': ccrs.PlateCarree()}
        )

    g.map_features(axs)

    lat = g.limits(min = -40.0, max = 10, stp = 10)
    lon = g.limits(min = -85, max = -30, stp = 10)    

    g.map_boundaries(axs, lon, lat)

    infile = f'database/GEO/coords/{year}.json'
    sites = json.load(open(infile))
    
    out = []

    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        min_d = distance_from_equator(
                lon, 
                lat, 
                year = year
                )
        
        if min_d < distance:
        
            axs.scatter(
                lon, lat, 
                s = 20, 
                color = 'k', 
                transform = ccrs.PlateCarree(), 
                label = name
                )
            
            # axs.text(lon, lat, name)
            
            out.append(name)
    
        
    for long in np.arange(-80, -20, 10):
        axs.axvline(long)
        
        
    g.mag_equator(
            axs, 
            year = year, 
            degress = 7
            )
    
    return out
    

# d = plot_receivers(5.1)

