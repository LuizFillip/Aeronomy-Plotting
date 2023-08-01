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
         arrowprops=dict(facecolor='black', arrowstyle="->"), 
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

def plot_receivers():
    fig, axs = plt.subplots(
        dpi = 300,
        subplot_kw={
            'projection': ccrs.PlateCarree()}
        )

    g.map_features(axs)

    lat = g.limits(min = -40.0, max = 10, stp = 10)
    lon = g.limits(min = -80, max = -30, stp = 10)    

    g.map_boundaries(axs, lon, lat)

    infile = 'database/GEO/coords_receivers.json'
    sites = json.load(open(infile))

    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        min_d = distance_from_equator(
                lon, lat, year = 2013
                )
        
        if min_d < 7:
        
            axs.scatter(
                lon, lat, 
                s = 20, 
                color = 'k', 
                transform = ccrs.PlateCarree(), 
                label = name
                )
        
    for long in np.arange(-70, -30, 10):
        axs.axvline(long)
        
        
    g.mag_equator(
            axs, 
            year = 2013, 
            color = 'r'
            )
    

# plot_mapping_with_sites_locations()

