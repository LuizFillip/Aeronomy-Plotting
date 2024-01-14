import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 

b.config_labels(fontsize = 30)

args = dict( 
    s = 40, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )


def plot_regions_over_map(year = 2013):
    
    """
    Plot only the regions (squares) pver the map
    
    """
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year, degress = 5)
    gg.plot_rectangles_regions(ax)
    
    
    sites = gg.stations_near_of_equator(
        year,
        distance = 5
        )
    
    for (lon, lat) in sites.values():
        
        ax.scatter(lon, lat, **args)
    
    
    return fig
    
fig = plot_regions_over_map(year = 2013)

# plt.show()