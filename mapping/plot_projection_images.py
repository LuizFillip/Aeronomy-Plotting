import GEO as gg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import imager as im
import base as b 

b.config_labels()


def plot_projection(
        ax, 
        img, 
        center_lon, 
        center_lat, 
        areap = 1024
        ):
    
    
    radius_deg = areap / 111
    
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
    
    ax.scatter(center_lon, center_lat, marker = '^')

def plot_images_projection(img, areap = 512, site = 'car'):
    
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    lat_lims = dict(min = -20, max = 10, stp = 5)
    lon_lims = dict(min = -60, max = -20, stp = 10) 
    
    
    gg.map_attrs(
        ax, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims, 
        year = 2017
        )
    
    center_lat, center_lon = gg.sites[site]['coords']
    
    plot_projection(
        ax,
        img, 
        center_lon, 
        center_lat, 
        areap = areap
        )
        
        
    return fig

path_of_image = 'database/images/CA_2013_1224/O6_CA_20131224_224601.tif'

all_sky = im.processing_img(path_of_image)

img = all_sky.linear( all_sky.bright)

fig = plot_images_projection(img)