import pyIGRF
import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import GEO as gg


def mapping():
    
    lat_lims = dict(
        min = -25, 
        max = 15, 
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
     
radius = 10

year = 2013

eq = gg.load_equator(year)

df = pd.DataFrame(
    eq, columns = ['lon', 'lat']
    )


ax = mapping()

for slon in list(
        range(-65, -30, radius)
        ):
    
    coords = df.loc[
        (df['lon'] > slon - radius) &
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

    angle_degrees = -45
    angle_radians = np.deg2rad(angle_degrees)
    
    x_limits = []
    y_limits = []
    
    for i in range(4):
        angle = angle_radians + i * np.pi / 2  
        x = clon + (radius - 3) * np.cos(angle)
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
    

