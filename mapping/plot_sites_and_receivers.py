import base as b
import GEO as gg
import cartopy.crs as ccrs
import  plotting as pl
import matplotlib.pyplot as plt 


PATH_COORDS = 'database/GEO/coords/'


args = dict( 
    s = 40, 
    marker = 'o',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )


b.config_labels(fontsize = 25)

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
    # plot_sites(ax)
    
    ax.legend(
        # bbox_to_anchor = (0.7, 1.2),
        ncol = 1, 
        loc = 'upper right'
        )
    
    return out

            

def plot_sites_and_receivers(
        year = 2013,
        distance = 5
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10,10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year)
    
    
    
    out = plot_receivers_coords(
        ax, year, distance = None)
    
    glat, glon = gg.sites['saa']['coords']
    
    # gg.circle_range(ax, glon, glat, radius = 500)
    
    fontsize = 35
    ax.text(0.03, 0.91, '(a)', 
            transform = ax.transAxes, 
            fontsize = fontsize)
    
    corners = pl.plot_corners(ax, year)
    
    pl.first_of_terminator(
            ax, 
            corners, 
            eq_lon = None, 
            eq_lat = None,
            year = 2013
            )
    
    
    
    ax.legend(loc = 'upper right')
    return fig, out

# fig, rec = plot_sites_and_receivers()

# FigureName = 'sites_instrumentation'

# fig.savefig(b.LATEX(FigureName), dpi = 400)


