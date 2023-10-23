import base as b
import os
import json 
import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 


PATH_COORDS = 'database/GEO/coords/'


args = dict( 
    s = 40, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )


b.config_labels()

def plot_sites(ax):
    sites = ['saa', 'jic', 'boa',
             'car', 'for', 'str']
    
    sites = ['saa',  'car', 'car', 'caj']
    names = ['Digisonde', 
             'Imager', 'FPI', 'FPI']
    
    for i, site in enumerate(sites):
    
        glat, glon = gg.sites[site]['coords']
        name =  names[i]
        
        if name == 'FPI':
            marker = 's'
        elif name == 'Imager':
            marker = 'o'
        elif name == 'Digisonde':
            marker = '*'
        
        ax.scatter(
            glon, glat,
            s = 200, 
            label = name, 
            marker = marker
            )
        
        
def plot_receivers_coords(
        axs, 
        year, 
        distance = 5
        ):
    
    infile = os.path.join(
        PATH_COORDS, 
        f'{year}.json'
        )
    sites = json.load(open(infile))
    
    x = []
    y = []
 
    
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
                    lon, lat, **args,
                    label = 'GNSS receivers'
                    )
            
                # out.append(name)
        else:
            x.append(lon)
            y.append(lat)
            
           
    
    axs.scatter(
        x, y, **args,
        label = 'GNSS receivers'
       
        )
    plot_sites(axs)
    
    axs.legend(
        bbox_to_anchor = (.5, 1.15),
        ncol = 3, 
        loc = 'upper center'
        )

            

def plot_sites_and_receivers(
        year = 2021,
        distance = 5
        ):
    
    lat_lims = dict(
        min = -15, 
        max = 10, 
        stp = 5
        )

    lon_lims = dict(
        min = -60,
        max = -30, 
        stp = 5
        )    

    fig, ax = gg.quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (9, 9), 
        year = year, 
        degress = None
        )
    
    
    plot_receivers_coords(
        ax, year, distance = None)
    
    glat, glon = gg.sites['saa']['coords']
    gg.circle_range(ax, glon, glat, radius = 500)
    
    
    return fig

fig = plot_sites_and_receivers()

# fig.savefig(b.LATEX + 'paper1/sites_instrumentation', dpi = 400)