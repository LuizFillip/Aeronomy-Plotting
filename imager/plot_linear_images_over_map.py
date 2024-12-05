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
   
    if site == 'CA':
        limits = [0.35, 0.99]
    else:
        limits = [0.29, 0.99]
        
    asi = im.DisplayASI(
        path_asi, 
        site = site, 
        areap = areap, 
        limits = limits
        )
    
    asi.display_linear(ax)
    site_in = im.sites_infos(site)
    lon, lat = site_in.coords
    
    ax.scatter(lon, lat, s = 200, 
               marker = '^')
    

    time = im.fn2dn(path_asi).strftime('29:%M UT - ')
    
    yset = area_factor + 1.5
    xset = area_factor + 2.5
    
    ax.text(
        lon - xset, 
        lat + yset, 
        time + site,
        color = 'w',
        transform = ax.transData, 
        fontsize = 25
        )
    return None



def plot_linear_images_over_map(dn):
    
    
    fig, ax = plt.subplots(
        figsize = (16, 10), 
        dpi = 300, 
        subplot_kw = 
          {'projection': ccrs.PlateCarree()}
        )
    
    lat_lims = dict(min = -30, max = 0, stp = 10)
    lon_lims = dict(min = -60, max = -30, stp = 10) 
    
    
    gg.map_attrs(
        ax, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims, 
        year = 2022,
        grid = False
        )

    plt.grid(which='major')
    
    plot_image(ax, dn, site = 'CA')
    plot_image(ax, dn, site = 'BJL')
    plot_image(ax, dn, site = 'CP')
    
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.set(
        title = dn.strftime('%Y_%m_08-%d')
        )
    
    return fig

    
dn = dt.datetime(2022, 3, 9, 5, 21)
    
fig = plot_linear_images_over_map()