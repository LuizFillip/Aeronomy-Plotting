import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 

b.config_labels(fontsize = 30)

args = dict( 
    s = 50, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )

def plot_sites(ax, year):
        
    sites  = ['jic', 'saa', 'bvj', 'ca', 'cp', 'bjl']
    
    for i, site in enumerate(sites):
        
        site = gg.sites[site]
        
        name = site['name']
        glat, glon = site['coords']
        
        ax.scatter(glon, glat, s = 150,
                   marker = 's', label = name)
        
        # ax.text(glon, glat - 4, name)
    

def plot_regions_over_map(year = 2013):
    
    """
    Plot only the regions (squares) over the map
    
    """
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year, degress = None, grid = False)
    gg.plot_rectangles_regions(ax)
    plot_sites(ax, year)
    
    ax.legend(
        loc = 'lower right',
        ncol = 3, 
        bbox_to_anchor = (1., 1.01), 
        columnspacing = 0, 
        fontsize = 22
        
        )
    
    lon, lat = gg.stations_coordinates(year, distance = 10)
    
    ax.scatter(lon, lat, **args)
    
    ax.annotate(
        'Receptores GNSS', xy=(lon[1], lat[1]), 
        xytext=(lon[1] - 5, lat[1] + 15),
        arrowprops=dict(lw = 2, arrowstyle='->'), 
        transform = ax.transData, 
        fontsize = 25)
    return fig
    
# fig = plot_regions_over_map(year = 2013)
# FigureName = 'regions_and_ipp'
# fig.savefig(
#     b.LATEX(FigureName, folder = 'maps'),
#     dpi = 400
#     )

