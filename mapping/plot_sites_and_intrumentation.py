import PlasmaBubbles as pb 
import base as s
import os
import json 
import GEO as gg
import cartopy.crs as ccrs

PATH_COORDS = 'database/GEO/coords/'


s.config_labels()

def plot_sites(ax):
    
    for site in ['saa', 'jic', 'boa',
                 'car', 'for', 'str']:
    
        glat, glon = gg.sites[site]['coords']
        name =  gg.sites[site]['name']
        ax.scatter(
            glon, glat,
            s = 100, 
            label = name)
        
        ax.legend(
            bbox_to_anchor = (.5, 1.2),
            ncol = 3, 
            loc = 'upper center'
            )
        
        
def distance_from_equator(
        lon, lat, year = 2013
        ):
    eq = gg.load_equator(year)
    x, y = eq[:, 0], eq[:, 1]
    min_x, min_y, min_d = gg.compute_distance(
        x, y, lon, lat
        )
    return min_d

args = dict( 
    s = 40, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )



        
def plot_receivers_coords(
        axs, 
        year, 
        distance = 100
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
        
        if lat > distance:
        
            axs.scatter(
                lon, lat, **args
               
                )
        
            out.append(name)

            
    return out

def plot_sites_and_intrumentation(
        year = 2021,
        glat = -22
        ):
    
    lat_lims = dict(
        min = -30, 
        max = 5, 
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
    
    plot_sites(ax)
    
    receivers = plot_receivers_coords(
        ax, year, distance = glat)
    
    ax.axhline(glat, linestyle = '--')
    ax.axhline(glat * -1, linestyle = '--')
    
    for long in pb.longitudes():

        ax.axvline(long, linestyle = '--')
    
    return receivers

r = plot_sites_and_intrumentation()

