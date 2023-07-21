from GEO import quick_map, sites
import json
import numpy as np
from GEO import circle_range

def plot_meridian(ax):
    
    infile = 'database/GEO/meridian.json'
    
    dat = json.load(open(infile))
    
    x = np.array(dat['mx'])
    y = np.array(dat['my'])
    
    ax.plot(x, y)
    
    ax.text(-47, 6, 'Magnetic\nmeridian')
    ax.text(-37, 2, 'Geomagnetic\nequator', color = 'red')
    
lat_lims = dict(min = -20, max = 10, stp = 5)

lon_lims = dict(min = -60, max = -30, stp = 5)    


def plot_sites_map():
    fig, ax = quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (10, 10)
        )
    
    markers = ['s', '^', 'o']
    
    instrs = ['All-Sky imager and FPI', 
              'Digisonde and GNSS receiver', 
              'FPI']
    
    radius = [500, 215, 0]
    colors = ['red',  'blue', 'white']
    
    
    for i, site in enumerate(["car", "saa", 'caj']):
        s = sites[site]
        clat, clon = s["coords"]
        ax.scatter(
            clon, clat, s = 200, 
            marker = markers[i], 
            label = f'{s["name"]} ({instrs[i]})'
            )
       
            
        circle_range(
            ax, 
            clon, 
            clat, 
            radius = radius[i], 
            color = colors[i]
            )
    
    ax.text(-37, -13, 'All-Sky range', color = 'red')
    ax.text(-42.5, -2, 'Digisonde range', color = 'blue')
    
    
    plot_meridian(ax)
    ax.legend(bbox_to_anchor = (.5, 1.2), 
              ncol = 1,
              loc = 'upper center')