import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import json 
import numpy as np
import os 
import base as b 
import datetime as dt


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
        long = None, 
        angle = 18
        ):
 
      dn = dt.datetime(2022, 1, 1, 0)
     
      dusk = g.dawn_dusk(
              dn,  
              lat = 0, 
              lon = long, 
              twilightAngle = angle
              )
     
      delta_day = dt.timedelta(days = 1)
     
      if dusk < dn:
          dusk += delta_day
          
    
      lon, lat = g.terminator(dusk, angle)
    
      line, = ax.plot(
            lon, 
            lat, 
            lw = 2, 
            linestyle = '--'
            )
      
      time = dusk.strftime('%H:%M')
      
      ax.text(long, 11, time, 
              transform = ax.transData,
              color = line.get_color()
              )
      
     
    
         


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
        distance = 7,
        year = 2022
        ):
    
    
    fig, axs = plt.subplots(
        dpi = 300,
        figsize = (8, 8),
        subplot_kw={
            'projection': ccrs.PlateCarree()}
        )

    g.map_features(axs)

    lat = g.limits(
        min = -40.0, 
        max = 10, 
        stp = 10
        )
    lon = g.limits(
        min = -90, 
        max = -20, 
        stp = 10
        )    

    g.map_boundaries(axs, lon, lat)
    
    plot_receivers_coords(axs, year, distance)
    
        
    for long in np.arange(-80, -20, 10):
        
        axs.axvline(long )
        
        lon = long - 10
        
        if lon != - 90:
        
            plot_terminator_lines(axs, lon)
        
    g.mag_equator(
            axs, 
            year = year, 
            degress = None
            )
    
   
    
    
    return 
    

d = plot_receivers(5.1)



