import base as b
import os
import json 
import GEO as gg
import cartopy.crs as ccrs


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
    
    sites = ['saa',  'car', ] #'car', 'caj'
    names = ['Digisonde', 
             'Imager']  #'FPI', 'FPI'
    
    markers = ['o', 's']
    colors = ['g', 'b']
    for i, site in enumerate(sites):
    
        glat, glon = gg.sites[site]['coords']
        name =  names[i]
        marker = markers[i]
    
        ax.scatter(
            glon, glat,
            s = 200, 
            c = colors[i],
            label = name, 
            marker = marker
            )
        
        
def get_equator_distance(lon, lat, year):
    
    min_d = gg.distance_from_equator(
            lon, 
            lat, 
            year = year
                )
        
def plot_receivers_coords(
        ax, 
        year, 
        distance = None
        ):
    
    # infile = os.path.join(
    #     PATH_COORDS, 
    #     f'{year}.json'
    #     )
    # sites = json.load(open(infile))
    
    names, lons, lats = gg.arr_coords(
        year
        )
    
    x = []
    y = []
 
    lon_s = -40
    lon_e = -50
    lat_e = -13
    out = []

    for name, lon, lat in zip(names, lons, lats):
    
        if ((lon < lon_s) and 
            (lon > lon_e) and 
            (lat > lat_e)):
            
            ax.scatter(
                lon, 
                lat, 
                **args,
                )
            
            out.append(name)
        
    
    ax.axvline(lon_s, linestyle = '--')
    ax.axvline(lon_e, linestyle = '--')
    
    
    ax.scatter(
        x, y, **args,
        label = 'GNSS receivers'
       
        )
    plot_sites(ax)
    
    ax.legend(
        bbox_to_anchor = (.5, 1.12),
        ncol = 3, 
        loc = 'upper center'
        )
    
    return out

            

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
    
    
    out = plot_receivers_coords(
        ax, year, distance = None)
    
    glat, glon = gg.sites['saa']['coords']
    
    gg.circle_range(ax, glon, glat, radius = 500)
    
    
    return out

fig = plot_sites_and_receivers()

# fig.savefig(b.LATEX + 'sites_instrumentation', dpi = 400)


len(fig)