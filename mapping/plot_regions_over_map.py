import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 

b.config_labels(fontsize = 40)

args = dict( 
    s = 50, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )

def plot_sites(ax, year):
        
    sites  = ['jic', 'saa', 'bvj', 'ca', 'cp', 'bjl']
    sites = ['saa', 'fza', 'ca', 'bvj']
    for i, site in enumerate(sites):
        
        site = gg.sites[site]
        
        name = site['name']
        glat, glon = site['coords']
        
        ax.scatter(
            glon, glat, 
            s = 150,
            marker = 's', 
            label = name
            )
        
        # ax.text(glon - 3, glat + 1, name)
        
    return None

def plot_GNSS(ax, year, translate = False):

    lon, lat = gg.stations_coordinates(year, distance = 100)
    if translate:
        label = 'Receptores GNSS'
    else:
        label = 'GNSS receivers'
        
    sits, lon, lat = gg.arr_coords(year = 2021)
    ax.scatter(lon, lat, **args, label = label)
    
    # ax.annotate(
    #     'Receptores GNSS', xy=(lon[1], lat[1]), 
    #     xytext=(lon[1] - 5, lat[1] + 15),
    #     arrowprops=dict(lw = 2, arrowstyle='->'), 
    #     transform = ax.transData, 
    #     fontsize = 25
    #     )
    return None 

lat_lims = dict(min = -40, max = 20, stp = 10)
lon_lims = dict(min = -90, max = -30, stp = 10)

def plot_regions_over_map(year = 2013):
    
    """
    Plot only the regions (squares) over the map
    
    """
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (15, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(
        ax, year,
        degress = None, 
        grid = False, 
        lat_lims = lat_lims,
        lon_lims = lon_lims
)
    # gg.plot_rectangles_regions(ax, stop_index = 5)
    plot_sites(ax, year)
    plot_GNSS(ax, year, translate = False)
    
    ax.legend(
        loc = 'upper right',
        ncol = 1, 
        bbox_to_anchor = (1.6, 0.5), 
        columnspacing = 0, 
        fontsize = 35
        
        )
    
    
    return fig

def main():
    fig = plot_regions_over_map(year = 2013)
    
    FigureName = 'gnss_receivers'
    
    # fig.savefig(
    #     b.LATEX(FigureName, folder = 'maps'),
    #     dpi = 400
    #     )
    
    save_in = 'G:\\My Drive\\Papers\\Paper 2\\Midnight EPBs\\Eps\\img\\'

    # fig.savefig(save_in + FigureName, dpi = 300
    #             )
    
main()