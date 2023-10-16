import PlasmaBubbles as pb 
import base as s
import os
import json 
import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 


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
        
        


args = dict( 
    s = 40, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )



        
def plot_receivers_coords(
        axs, 
        year, 
        distance = None
        ):
    
    infile = os.path.join(
        PATH_COORDS, 
        f'{year}.json'
        )
    sites = json.load(open(infile))
    
    out = []
 
    
    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        if distance is not None:
            min_d = gg.distance_from_equator(
                    lon, 
                    lat, 
                    year = year
                    )
                    
            if min_d < distance:
            
                axs.scatter(
                    lon, lat, **args
                   
                    )
            
                out.append(name)
        else:
            axs.scatter(
                lon, lat, **args
               
                )

            
    return out

def plot_sites_and_receivers(
        year = 2021,
        distance = 5
        ):
    
    lat_lims = dict(
        min = -30, 
        max = 10, 
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
        degress = distance
        )
    
    # plot_sites(ax)
    
    receivers = plot_receivers_coords(
        ax, year)
    
    
    for long in pb.longitudes():

        ax.axvline(long, linestyle = '--')
    
    return receivers

r = plot_sites_and_receivers()

plt.show()