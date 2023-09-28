import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import json 
import numpy as np
import os 
import base as b 
import datetime as dt
import PlasmaBubbles as pb

PATH_COORDS = 'database/GEO/coords/'


names = ['ceeu', 'ceft', 
         'rnna', 'pbjp']
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


def plot_terminator_lines(
        ax, 
        dn,
        angle = 18,
        glat = -7
        ):
 
      for long in np.arange(-80, -30, 10):
          long = long + 10
                            
          dusk = pb.dusk_time(dn, long)
         
          lon, lat = g.terminator(dusk, angle)
          
          line, = ax.plot(
              lon, 
              lat, 
              lw = 2, 
              linestyle = '--'
              )
        
          ax.axhline(glat, lw = 1.5, linestyle = '--')
        
          time = dusk.strftime('%H:%M')
        
          ax.text(long, 11, time, 
                transform = ax.transData,
                color = line.get_color()
                )
        
          ax.axvline(
              long,
            color = line.get_color()
            )
          
      return ax
      
     

def plot_receivers_coords(
        axs, 
        year, 
        distance = 7
        ):
    
    infile = os.path.join(
        PATH_COORDS, 
        f'{year}.json'
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
        dn,
        distance = 7,
        year = 2022
        ):
    
    fig, axs = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        subplot_kw={
            'projection': ccrs.PlateCarree()
            }
        )

    g.map_features(axs)

    lat = g.limits(
        min = -30.0, 
        max = 10, 
        stp = 10
        )
    lon = g.limits(
        min = -80, 
        max = -20, 
        stp = 10
        )    

    g.map_boundaries(axs, lon, lat)
    
    plot_receivers_coords(axs, year, distance)
    
    plot_terminator_lines(axs, dn)
        
    g.mag_equator(
            axs, 
            year = year, 
            degress = None
            )
    
    fig.suptitle(
        dn.strftime('%d/%m/%Y'), 
        y = 0.85
        )

    return 
    
dn = dt.datetime(2022, 1, 1, 0)
d = plot_receivers(dn, 5.1)



