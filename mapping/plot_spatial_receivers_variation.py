import PlasmaBubbles as pb 
import base as b
import os
import json 
import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 

def load_coords(year = 2021):
    infile = os.path.join(
        gg.PATH_COORDS, 
        f'{year}.json'
        )
    return json.load(open(infile))

b.config_labels()


lat_lims = dict(
    min = -30, 
    max = 10, 
    stp = 5
    )

lon_lims = dict(
    min = -90,
    max = -30, 
    stp = 10
    )    

year = 2021

fig, ax = gg.quick_map(
    lat_lims = lat_lims, 
    lon_lims = lon_lims, 
    figsize = (9, 9), 
    year = 2021, 
    degress = None
    )




clon, clat = gg.plot_square_area(
    ax, 
    lon_min = -60, 
    lat_min = -10, 
    radius = 12)




sites = load_coords()

for name, key in sites.items():
    lon, lat, alt = tuple(key)
    if gg.find_range(lon, lat, clon, clat):
        ax.scatter(
            lon, lat, 
            s = 50, 
            marker = '^', 
            color = 'k'
            )