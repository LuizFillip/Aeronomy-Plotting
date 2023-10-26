import pyIGRF
import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import GEO as gg


def mapping():
    
    lat_lims = dict(
        min = -20, 
        max = 10, 
        stp = 5
        )
    
    lon_lims = dict(
        min = -90,
        max = -30, 
        stp = 10
        )    
    
    fig, ax = gg.quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (9, 9), 
        year = 2013, 
        degress = None
        )
    
    return ax
     
radius = 5

year = 2013

eq = gg.load_equator(year)

df = pd.DataFrame(eq, columns = ['lon', 'lat'])


ax = mapping()

for slon in list(range(-85, -30, 5)):
    
    coords = df.loc[
        (df['lon'] > slon - 5) &
        (df['lon'] < slon)
        ].min()
    
    
    clon = coords['lon']
    clat = coords['lat']
    
    lon_min = clon - radius
    lat_min = clat - radius
    
    # d, _, _, _, _, _, _ = pyIGRF.igrf_value(
    #     clat, 
    #     clon, 
    #     alt = 300, 
    #     year = year
    #     )

    angle_degrees = -19
    angle_radians = np.deg2rad(angle_degrees)
    
    x_limits = []
    y_limits = []
    
    for i in range(4):
        angle = angle_radians + i * np.pi / 2  
        x = clon + radius * np.cos(angle)
        y = clat + (radius + 3) * np.sin(angle) 
        x_limits.append(x)
        y_limits.append(y)
    
    
    x_limits.append(x_limits[0])
    y_limits.append(y_limits[0])
    
    
    ax.plot(
        x_limits,
        y_limits,
        color = 'black', 
        linewidth = 2, 
        transform = ccrs.PlateCarree() 
        )
    
    
    ax.scatter(clon, clat)
    

