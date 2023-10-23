import base as b
import GEO as gg
import matplotlib.pyplot as plt 



b.config_labels()

def map_attrs(year = 2021):

    lat_lims = dict(
        min = -15, 
        max = 10, 
        stp = 5
        )
    
    lon_lims = dict(
        min = -60,
        max = -30, 
        stp = 10
        )    
    
    fig, ax = gg.quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (9, 9), 
        year = year, 
        grid = False,
        degress = None
        )
    
    return ax

def plot_in_circle(
        ax, 
        lon, lat, 
        center, radius = 8
        ):
    
    circle = plt.Circle(
        center, 
        radius, 
        color = 'gray', 
        alpha = 0.2, 
        label = 'Circle'
        )
    
    plt.gca().add_patch(circle)
    
    in_x, in_y = gg.distance_circle(
        lon, lat, 
        center, 
        radius
        )
    
    ax.scatter(
        in_x, 
        in_y, 
        marker = '^',
        s = 50,
        color = 'k'
        )

    return in_x, in_y



    

ax  = map_attrs()


clon, clat, radius = -45, -5, 5

names, lon, lat = gg.arr_coords(
    year = 2021
    )

in_x, in_y = plot_in_circle(
    ax, lon, lat, (clon, clat), 
    radius
    )



