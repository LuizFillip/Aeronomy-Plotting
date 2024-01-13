import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 

b.config_labels()


def plot_regions_over_map(year = 2013):
    
    """
    Plot only the regions (squares) pver the map
    
    """
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10,10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year)
    gg.plot_rectangles_regions(ax)
    

    
    return fig
    
fig = plot_regions_over_map(year = 2013)

# plt.show()