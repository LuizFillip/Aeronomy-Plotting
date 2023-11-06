import base as b
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
    
    sites = ['saa', 'car'] 
    names = ['Digisonde (São Luis)',  'Imager (Cariri)']  
    
    markers = ['*', 's']
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
        distance = None, 
        text = True
        ):
    
    
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
            if text:
                ax.text(
                    lon - 1.5, lat - 1, 
                    name.upper(), 
                    transform = ax.transData,
                    fontsize = 15
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
        bbox_to_anchor = (1.85, 0.5),
        ncol = 1, 
        loc = 'right'
        )
    
    return out

            

def plot_sites_and_receivers(
        year = 2013,
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
    
    
    return fig, out

# fig, rec = plot_sites_and_receivers()

# FigureName = 'sites_instrumentation'

# fig.savefig(b.LATEX(FigureName), dpi = 400)


