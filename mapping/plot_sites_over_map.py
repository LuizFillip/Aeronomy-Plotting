from GEO import quick_map, sites
import PlasmaBubbles as pb 
import base as s

s.config_labels()

def plot_sites(ax):
    
    for site in ['saa', 'jic', 'boa',
                 'car', 'for']:
    
        glat, glon = sites[site]['coords']
        name =  sites[site]['name']
        ax.scatter(
            glon, glat,
            s = 100, 
            label = name)
        
        ax.legend()

def plot_sites_map():
    
    lat_lims = dict(
        min = -40, 
        max = 10, 
        stp = 10
        )

    lon_lims = dict(
        min = -90,
        max = -30, 
        stp = 10
        )    

    fig, ax = quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (8,8), 
        year = 2013, 
        degress = None
        )
    
    plot_sites(ax)
        
    for long in pb.longitudes():

        ax.axvline(long)
    
    
plot_sites_map()
