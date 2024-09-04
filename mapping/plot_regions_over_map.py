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
    sites = ['jic', 'saa', 'bvj', 'ca']
    for i, site in enumerate(sites):
        
        site = gg.sites[site]
        
        name = site['name']
        glat, glon = site['coords']
        
        ax.scatter(glon, glat, s = 150,
                   marker = 's', label = name)
        
        # ax.text(glon - 3, glat + 1, name)
        
    return None

def plot_GNSS(ax, year):

    lon, lat = gg.stations_coordinates(year, distance = 10)
    
    ax.scatter(lon, lat, **args, label = 'Receptores GNSS')
    
    # ax.annotate(
    #     'Receptores GNSS', xy=(lon[1], lat[1]), 
    #     xytext=(lon[1] - 5, lat[1] + 15),
    #     arrowprops=dict(lw = 2, arrowstyle='->'), 
    #     transform = ax.transData, 
    #     fontsize = 25
    #     )

lat_lims = dict(min = -20, max = 10, stp = 10)

def plot_regions_over_map(year = 2013):
    
    """
    Plot only the regions (squares) over the map
    
    """
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (13, 6),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(
        ax, year,
        degress = None, 
        grid = False, 
        lat_lims = lat_lims,
)
    gg.plot_rectangles_regions(ax)
    # plot_sites(ax, year)
    # plot_GNSS(ax, year)
    
    ax.legend(
        loc = 'upper center',
        ncol = 3, 
        # bbox_to_anchor = (1., 1.0), 
        columnspacing = 0, 
        fontsize = 20
        
        )
    
    
    return fig

def main():
    fig = plot_regions_over_map(year = 2013)
    FigureName = 'regions_and_ipp'
    # fig.savefig(
    #     b.LATEX(FigureName, folder = 'maps'),
    #     dpi = 400
    #     )
    
main()