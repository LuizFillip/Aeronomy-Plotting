import base as b
import GEO as gg
import matplotlib.pyplot as plt 
import events as ev 



b.config_labels()

def map_attrs(year = 2021):

    lat_lims = dict(
        min = -15, 
        max = 5, 
        stp = 5
        )
    
    lon_lims = dict(
        min = -55,
        max = -35, 
        stp = 5
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
        radius + 3, 
        color = 'gray', 
        alpha = 0.1, 
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
    
    name = ev.get_filters_lists(
            clon, 
            clat, 
            radius, 
            year = 2021
            )
    
    for x, y, n in zip(in_x, in_y, name):
        ax.text(
            x - 0.5, y + 0.2, 
            n.upper(), 
            transform = ax.transData
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




