import numpy as np
import cartopy.crs as ccrs
import pandas as pd
import GEO as gg
import GNSS as gs 
import os 
import PlasmaBubbles as pb 

def mapping(year = 2013):
    
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
        year = year, 
        degress = None
        )
    
    return ax
     

def equator_coords(year = 2013):

    eq = gg.load_equator(year)
    
    return pd.DataFrame(
        eq, columns = ['lon', 'lat']
        )



def corner_coords(
        year = 2013, 
        radius = 10,  
        angle_degrees = -45
        ):
    
    df = equator_coords(year)

    x_coords = []
    y_coords = []
    
    for slon in list(
            range(-65, -30, radius)
            ):
        
        coords = df.loc[
            (df['lon'] > slon - radius) &
            (df['lon'] < slon)
            ].min()
        
        
        clon = coords['lon']
        clat = coords['lat']
        
        angle_radians = np.radians(angle_degrees)
        
        x_limits = []
        y_limits = []
        
        for i in range(4):
            angle = angle_radians + i * np.pi / 2  
            x = clon + (radius - 3) * np.cos(angle)
            y = clat + (radius + 3) * np.sin(angle) 
            
            x_limits.append(round(x, 4))
            y_limits.append(round(y, 4))
        
        
        x_limits.append(x_limits[0])
        y_limits.append(y_limits[0])
        
        x_coords.append(x_limits)
        y_coords.append(y_limits)
    
    return x_coords, y_coords
            
    



def plot_corners(ax, clon, clat):
    ax.scatter(clon, clat, c = 'k') 

    for x_limits, y_limits in zip(x_coords, y_coords):
        ax.plot(
            x_limits,
            y_limits,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )

def set_coords(
        x_coords, 
        y_coords
        ):

    coords = {}
    
    for i in range(4):
        
        lon_set = sorted(tuple(set(x_coords[i])))
        lat_set = sorted(tuple(set(y_coords[i])))
        
        coords[i + 1] = (lon_set, lat_set)
    
    return coords






year = 2019
doy = 1
path  = gs.paths(year, doy, root = os.getcwd())
df = pb.load_filter(path.fn_roti)

x_coords, y_coords = corner_coords(year)


ax = mapping()
coords = set_coords(x_coords, y_coords)

(x0, x1), (y0, y1) = coords[1]


ds  = df.loc[
    (df['lat'] > y0) & (df['lat'] < y1) &
    (df['lon'] > x0) & (df['lon'] < x1)
    ]


ax.scatter(ds.lon, ds.lat, c = ds.roti, s = 3)

ds
