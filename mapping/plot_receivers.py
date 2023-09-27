import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import json 
import numpy as np
import os 
import base as b 


PATH_COORDS = 'database/GEO/coords/'


names = ['ceeu', 'ceft', 'rnna', 'pbjp']
args = dict( 
    s = 40, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )


b.config_labels()


def distance_from_equator(
        lon, lat, year = 2013
        ):
    eq = g.load_equator(year)
    x, y = eq[:, 0], eq[:, 1]
    min_x, min_y, min_d = g.compute_distance(
        x, y, lon, lat
        )
    return min_d


def plot_receivers_coords(axs, year, distance = 7):
    
    infile = os.path.join(
        PATH_COORDS, f'{year}.json'
        )
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
                lon, lat, **args
               
                )
        
            out.append(name)
        
        elif any([name == c for c in names]):
            
            axs.scatter(
                lon, lat, **args
                )
        
            out.append(name)
            
            
    
    return out

def plot_receivers(
        distance = 7,
        year = 2022
        ):
    
    
    fig, axs = plt.subplots(
        dpi = 300,
        figsize = (6, 6),
        subplot_kw={
            'projection': ccrs.PlateCarree()}
        )

    g.map_features(axs)

    lat = g.limits(min = -40.0, max = 10, stp = 10)
    lon = g.limits(min = -90, max = -30, stp = 5)    

    g.map_boundaries(axs, lon, lat)
    
    plot_receivers_coords(axs, year, distance)
    
        
    for long in np.arange(-80, -20, 5):
        axs.axvline(long)
        
        
    g.mag_equator(
            axs, 
            year = year, 
            degress = None
            )
    
    return 
    

d = plot_receivers(5.1)

