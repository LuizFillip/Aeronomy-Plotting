import imager as im 
import matplotlib.pyplot as plt 
import datetime as dt 
import GEO as gg
import base as b
import cartopy.crs as ccrs

b.config_labels()

def plot_image(ax, dn, site = 'CA'):
    
    area_factor = 2.5
     
    areap = 512 * area_factor

    path_asi = im.path_from_closest_dn(
            dn, 
            site = site, 
            )
    # print(path_asi)
    asi = im.DisplayASI(
        path_asi, 
        site = site, 
        areap = areap, 
        limits = [0.23, 0.99]
        )
    
    asi.display_linear(ax)
    site = im.sites_infos(site)
    lon, lat = site.coords
    
    ax.scatter(lon, lat, s = 200, label = site.name, 
               marker = '^')
    
    ax.legend(loc = 'lower right', 
              handletextpad = 0.1,
              fontsize = 25)
    
    time = im.fn2dn(path_asi).strftime('%H:%M UT')
    
    ax.text(
        lon - 5, lat + 4, time,
        color = 'w',
        transform = ax.transData, 
        fontsize = 30
        )
    return None



def plot_linear_images_over_map():
    
    
    fig, ax = plt.subplots(
        figsize = (16, 10), 
        dpi = 300, 
        subplot_kw = 
          {'projection': ccrs.PlateCarree()}
        )
    
    lat_lims = dict(min = -30, max = 0, stp = 5)
    lon_lims = dict(min = -55, max = -25, stp = 5) 
    
    
    gg.map_attrs(
        ax, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims, 
        year = 2022,
        grid = False
        )
    
    
    dn = dt.datetime(2022, 3, 9, 5, 21)
    
    
    
    plot_image(ax, dn, site = 'CA')
    plot_image(ax, dn, site = 'BJL')
    plot_image(ax, dn, site = 'CP')
    
    
    ax.set(title = dn.strftime('%B, %d %Y'))
    
    return fig