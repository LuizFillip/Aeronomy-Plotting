import GEO as gg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import imager as im
import base as b 
import pandas as pd 



b.config_labels()



def set_image(
        ax, 
        path_of_image, 
        area_factor = 0.5, 
        color = 'red'
        ):
    
    all_sky = im.processing_img(path_of_image)
    
    areap = 512 * area_factor
    
    # img = all_sky.linear(all_sky.bright(), area = areap)
    img = im.crop_circle(all_sky.bright())
    
    site = all_sky.site.lower()
    
    plot_projection(
        ax,
        img, 
        site = site,
        areap = areap,
        color = color
        )
        

def plot_projection(
        ax, 
        img, 
        site, 
        areap = 1024,
        color = 'red'
        ):
    
    center_lat, center_lon = gg.sites[site]['coords']


    radius_deg = (areap / 111) / 2
    
    extent = [
        center_lon - radius_deg,
        center_lon + radius_deg,
        center_lat - radius_deg,
        center_lat + radius_deg
    ]
    
    ax.imshow(
        img, 
        transform=ccrs.PlateCarree(), 
        extent = extent, 
        cmap='gray'
        )
    
    ax.scatter(center_lon, center_lat, 
               s = 250, marker = '^',
               color = color)
    
    
def plot_images_projection(dn):
    
    fig = plt.figure(figsize = (12, 12))
    ax = plt.axes(projection = ccrs.PlateCarree())
    
    lat_lims = dict(min = -30, max = 0, stp = 5)
    lon_lims = dict(min = -60, max = -30, stp = 5) 
    
    
    gg.map_attrs(
        ax, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims, 
        year = 2022,
        grid = False
        )
    
    path_of_image = im.path_from_closest_dn(dn, site = 'BJL')
    # print(path_of_image)
    set_image(ax, path_of_image, area_factor = 2, 
              color = 'blue')
    
    
    path_of_image = im.path_from_closest_dn(dn, site  = 'CA')
    # print(path_of_image)
    set_image(ax, path_of_image, area_factor = 2, 
              color = 'red')
    
    path_of_image = im.path_from_closest_dn(dn, site = 'CP')
    # print(path_of_image)
    set_image(ax, path_of_image, area_factor = 2, 
              color = 'green')
    
    
    color = ['blue', 'red']
    
    for i, site in enumerate(['saa', 'fza']):
        center_lat, center_lon = gg.sites[site]['coords']
        
        ax.scatter(center_lon, center_lat, 
                   s = 250, marker = 'o',
                   color = color[i])
        
        
    ax.set(title = dn.strftime('%Y-%m-%d %H:%M UT'))
    
    return fig

from tqdm import tqdm 
times = pd.date_range(
    '2022-07-24 21:00', 
    '2022-07-25 07:00', 
    freq = '2min'
    )

# for dn in tqdm(times):
    
#     plt.ioff()
#     fig = plot_images_projection(dn)

#     name = dn.strftime('temp/%Y%m%d%H%M')    
#     fig.savefig(name, dpi = 100)
    
#     plt.clf()
#     plt.close()

import datetime as dt 
dn = dt.datetime(2022, 7, 25, 2)
fig = plot_images_projection(dn)