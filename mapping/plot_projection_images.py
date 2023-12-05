import GEO as gg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Create a map

def plot_projection(
        ax, 
        image_path, 
        center_lon, 
        center_lat, 
        radius_km = 512
        ):
    
    img = plt.imread(image_path)
    
    radius_deg = radius_km / 111
    
    extent = [
        center_lon - radius_deg,
        center_lon + radius_deg,
        center_lat - radius_deg,
        center_lat + radius_deg
    ]
    
    ax.imshow(img, 
              transform=ccrs.PlateCarree(), 
              extent=extent, cmap='gray')
    
    ax.scatter(center_lon, center_lat, marker = '^')

def plot_images_projection():
    
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    lat_lims = dict(min = -20, max = 10, stp = 5)
    lon_lims = dict(min = -60, max = -30, stp = 10) 
    
    
    gg.map_attrs(
        ax, 
        lon_lims = lon_lims, 
        lat_lims = lat_lims, 
        year = 2017
        )
    
    image_path = 'database/CA_2017_0403P/O6_CA_20170404_025433.png'  
    
    for site in ['car', 'str']:
        
        center_lat, center_lon = gg.sites[site]['coords']
        
        plot_projection(
            ax,
            image_path, 
            center_lon, 
            center_lat, 
            radius_km = 512
            )
        
        
    plt.show()
