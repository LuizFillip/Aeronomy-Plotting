import base as b
import GEO as gg
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs

b.sci_format(fontsize = 25)

def plot_in_circle(
        year, 
        clon, clat, 
        center, radius = 8
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year, degress = 5, grid = False)
    
   
    
    in_x, in_y = gg.distance_circle(
        clon, clat, 
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
    
    # name = c.get_filters_lists(
    #         clon, 
    #         clat, 
    #         radius, 
    #         year = 2013
    #         )
    
    # for x, y, n in zip(in_x, in_y, name):
    #     ax.text(
    #         x - 0.5, y + 0.2, 
    #         n.upper(), 
    #         transform = ax.transData
    #         )

    return in_x, in_y



def main():

    year = 2021
    clon, clat, radius = -45, -5, 5
    
    names, lon, lat = gg.arr_coords(
        year = 2021
        )
    
    in_x, in_y = plot_in_circle(year, lon, lat, (clon, clat), 
        radius
        )
    
import json 
year = 2019


lilat = dict(min = -10, max = -4, stp = 1)
lilon = dict(min = -40, max = -34, stp =1)



fig, ax = plt.subplots(
    dpi = 300,
    sharex = True, 
    figsize = (8, 8),
    subplot_kw = {'projection': ccrs.PlateCarree()}
)

gg.map_attrs(
    ax, year,
    degress = None, 
    grid = False, 
    lat_lims = lilat,
    lon_lims = lilon
)

site = gg.sites['ca']

name = site['name']
clat, clon = site['coords']

ax.scatter(
    clon, clat, 
    s = 200,
    marker = '*', 
    label = name
    )

gg.plot_square_area(
        ax, 
        lat_min = -9, 
        lon_min = -38.5,
        lat_max = None, 
        lon_max = None, 
        radius = 4, 
        color = 'black',
        center_dot = False
        )


path = "database/GEO/coords/2019.json"
dic = json.load(open(path))


gs_rec = ['sant', 'rnpf', 'rogm', 'salu', 'ampt', 'mtji', 'pitn', 'ceeu',
       'bepa', 'savo', 'pepe', 'ceft', 'aps1', 'bapa', 'amha', 'topl',
       'maba', 'amcr', 'gour', 'babj', 'apma', 'bait', 'perc', 'rnmo',
       'amte', 'naus', 'mabs', 'rnna', 'pait', 'togu', 'cesb', 'pifl',
       'bail', 'peaf', 'bele', 'picr', 'alma', 'amco', 'pbcg', 'pbjp',
       'impz', 'crat', 'riob', 'pisr', 'pove', 'saga', 'amua',
       'roji',  'ssa1', 'babr',  'aplj', 'mabb']

ax.legend()
for rec in gs_rec:
    

    glon, glat, alt = tuple(dic[rec])
    
    if (
        (lilat['min'] < glat) and 
        (lilat['max'] > glat) and 
        (lilon['min'] < glon) and 
        (lilon['max'] > glon)
        ):
        
            ax.scatter(
                glon, glat, s = 100, 
                c = 'k',
                       label = 'GNSS receivers')
            
            ax.text(
                glon, glat, 
                rec.upper(), 
                transform = ax.transData
                )
        
