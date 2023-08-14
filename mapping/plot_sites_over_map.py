from GEO import quick_map, sites
import json
import numpy as np
import base as s

s.config_labels(fontsize = 10)


def plot_meridian(ax, year = 2017):
    
    infile = f'database/GEO/meridians/saa_{year}.json'
    
    dat = json.load(open(infile))
    
    x = np.array(dat['mx'])
    y = np.array(dat['my'])
    
    ax.plot(x, y)
    
    ax.text(-47, 6, 'Magnetic\nmeridian')
    ax.text(-75, -15, 'Geomagnetic\nequator', color = 'red')
    



def plot_sites_map(year = 2017):
    
    lat_lims = dict(min = -40, max = 10, stp = 10)

    lon_lims = dict(min = -80, max = -30, stp = 10)    

    fig, ax = quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (5, 5), 
        year = year, 
        degress = None
        )
    
    
    plot_meridian(ax, year = year)
    
    ax.set(title = year)
    
    
# plot_sites_map(year = 2017)
