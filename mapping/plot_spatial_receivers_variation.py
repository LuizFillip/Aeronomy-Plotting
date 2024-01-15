import base as b
import GEO as gg
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs

import core as c


b.config_labels()


def plot_in_circle(
        year, 
        lon, lat, 
        center, radius = 8
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year, degress = 5, grid = False)
    
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
    
    name = c.get_filters_lists(
            clon, 
            clat, 
            radius, 
            year = 2013
            )
    
    for x, y, n in zip(in_x, in_y, name):
        ax.text(
            x - 0.5, y + 0.2, 
            n.upper(), 
            transform = ax.transData
            )

    return in_x, in_y





year = 2021
clon, clat, radius = -45, -5, 5

names, lon, lat = gg.arr_coords(
    year = 2021
    )

in_x, in_y = plot_in_circle(year, lon, lat, (clon, clat), 
    radius
    )




