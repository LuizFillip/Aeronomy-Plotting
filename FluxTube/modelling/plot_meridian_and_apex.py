import cartopy.crs as ccrs
import matplotlib.pyplot as plt 
import plotting as pl
from matplotlib.gridspec import GridSpec
import base as b 
import GEO as gg 

args = dict( 
    s = 50, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )

b.config_labels(fontsize = 25)

def plot_meridian_and_apex(year = 2013):
    
    width = 16
    height = width / 2
    fig = plt.figure(
        figsize = (width, height), 
        dpi = 300,
        )
    
    
    gs2 = GridSpec(2, 6)
    
    gs2.update(wspace = 0)
    
    ax1 = plt.subplot(gs2[0:2, 0:2])
    
    pl.plot_apex_vs_latitude(ax1)
    
    ax2 = plt.subplot(
        gs2[0:2, 2:],  projection = ccrs.PlateCarree()
        )
    gg.plot_square_area(
        ax2,
        lat_min = -10,
        lon_min = -50,
        lat_max = 5, 
        lon_max = -40
        )
    
    
    pl.plot_mag_meridians(ax2, year)
    
    lons, lats = gg.stations_coordinates(year, distance = 10)
    
    glat, glon = gg.sites['car']['coords']
    
    ax2.scatter(glon, glat, s = 150, 
                marker = 's', color = 'b', 
                label = 'Cariri (imager)')
    
    for lon, lat in zip(lons, lats):
        if (lon > -50) and (lon < -40):
            ax2.scatter(
                lon, lat, **args
                )
            
    ax2.scatter(
        lon, lat, **args, 
        label = 'GNSS receivers'
        )
    
    ax2.legend(loc = 'upper right')
    
    for i, a in enumerate([ax1, ax2]):
        l = b.chars()[i]
        a.text(
            -0.1, 1.1, f'({l})', 
            transform = a.transAxes,
            fontsize = 35
            )
        
        
    return fig

fig = plot_meridian_and_apex()

# fig.savefig(b.LATEX('apex_meridian', folder = 'modeling'), dpi = 400)
# plt.show()