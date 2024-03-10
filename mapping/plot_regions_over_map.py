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
    
    lon, lat = gg.stations_coordinates(year, distance = 5)
    
    ax.scatter(lon, lat, **args, label = 'Receptores GNSS')
    
    c = ['red', 'blue']
    n  = ['São Luis', 'Jicamarca']
    
    for i, site in enumerate(['saa', 'jic']):
        
        glat, glon = gg.sites[site]['coords']
        
        ax.scatter(glon, glat, s = 150,
                   c = c[i], marker = 's', 
                   label = n[i])

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
    
    gg.map_attrs(ax, year, degress = 5, grid = False)
    gg.plot_rectangles_regions(ax)
    plot_sites(ax, year)
    
    ax.legend(
        loc = 'lower right',
        ncol = 1, 
        # bbox_to_anchor = (0.5, 1.1), 
        columnspacing = 0.2
        )
    
    return fig
    
fig = plot_regions_over_map(year = 2013)

# fig.savefig(
#     b.LATEX(FigureName, folder = 'maps'),
#     dpi = 400
#     )

