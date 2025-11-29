import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import numpy as np 





def legend_dummy():
    
    kwargs = dict(
        edgecolors = 'none',
        s = 300
        )
    
    l1 = plt.scatter(
        [], [], color = 'black', marker = 's', 
        **kwargs)
    l2 = plt.scatter(
        [], [], color = 'green', marker = 'o', 
        **kwargs)
    l3 = plt.scatter(
        [], [], color = 'red', marker = '^', 
        **kwargs)
    
    l4 = plt.scatter(
        [], [], color = 'orange', marker = '*', 
        s = 400,)

    labels = ["Ionosonde", "FPI", 
              'GNSS receivers', 
              'Magnetometers']

    plt.legend(
        [l1, l2, l3, l4], 
        labels, 
        ncol = 2, 
        fontsize = 25,
        handlelength = 2,
        bbox_to_anchor = (0.9, 1.15),
        labelspacing = 0,
        columnspacing = 0.3 
        # scatterpoints = 1
        )
    
    return None 
def curve_connect(
        ax, lat, lon, 
        name, 
        lat_delta, 
        lon_delta
        ):
    
    crs = ccrs.PlateCarree()

    line_kw = dict(color = 'k', lw = 2)
    text_kw = {"fontsize": 24, "ha": "left", "va": "center"
               } 

    lat_end = lat + lat_delta
    lon_end = lon + lon_delta
    
    xs = [lon, lon]
    ys = [lat, lat_end] 
     
    ax.plot(xs, ys, transform=crs, **line_kw)
    xs = [lon, lon_end]
    ys = ([lat_end, lat_end] )
    ax.plot(xs, ys, transform=crs, **line_kw)
    
    ax.text(lon_end , lat_end, name, transform=crs, **text_kw)


def plot_GNSS(ax, year, translate = False):

    lon, lat = gg.stations_coordinates(year, distance = 100)
    if translate:
        label = 'Receptores GNSS'
    else:
        label = 'GNSS receivers'
    
    args = dict( 
        s = 50, 
        marker = '^',
        color = 'red', 
        transform = ccrs.PlateCarree()
        )


    sits, lon, lat = gg.arr_coords(year = 2021)
    ax.scatter(lon, lat, **args)
    
    # ax.annotate(
    #     'Receptores GNSS', xy=(lon[1], lat[1]), 
    #     xytext=(lon[1] - 5, lat[1] + 15),
    #     arrowprops=dict(lw = 2, arrowstyle='->'), 
    #     transform = ax.transData, 
    #     fontsize = 25
    #     )
    return None 

stations = {
"Cachoeira\nPaulista" : {"lon": -45.0, "lat": -22.7, 
                        'lat_delta': 0, 'lon_delta': 11.3},
'Vassouras' : {
    "lon": -43.66, "lat": -22.41, 'lat_delta': -5, 'lon_delta': 10},
"São João \ndo Cariri": { 
    "lon": -36.5, "lat": -7.4, 'lat_delta': 0, 'lon_delta': 3.2},
 "Fortaleza": {
     "lon": -38.5, "lat": -3.7, 'lat_delta': 0, 'lon_delta': 5},
 "Campo\nGrande": {
     "lon": -54.6, "lat": -20.4, 'lat_delta': 3, 'lon_delta': 21},
"Boa Vista" :  {
    "lon": -60.7, "lat":  2.8, 'lat_delta': 0, 'lon_delta': 27
    },
 "São Luís": {
     "lon": -44.2, "lat": -2.6, 'lat_delta': 2, 'lon_delta': 11}
 }

fig, ax = plt.subplots(
    dpi = 300,
    sharex = True, 
    figsize = (15, 10),
    subplot_kw = {'projection': ccrs.PlateCarree()}
)

lat_lims = dict(min = -30, max = 10, stp = 10)
lon_lims = dict(min = -65, max = -30, stp = 10)

gg.map_attrs(
    ax, 2015,
    degress = None, 
    grid = False, 
    lat_lims = lat_lims,
    lon_lims = lon_lims
    )


for name, s in stations.items():
 
    lat, lon = s['lat'], s['lon']
    lat_delta, lon_delta = s['lat_delta'], s['lon_delta']
    
    curve_connect(
            ax, lat, lon, 
            name, 
            lat_delta, 
            lon_delta)
    
    if name[0] == 'V':
        marker = '*'
        color = 'orange'
    elif name[-1] == 'i':
        marker = 'o'
        color = 'green'
    else:
        marker = 's'
        color = 'k'
        
        
    ax.scatter(lon, lat, s = 200, marker = marker, 
               color = color)
    
s = stations['São Luís']
lat, lon = s['lat'], s['lon']
ax.scatter(lon, lat, s = 200, marker = '*', 
           color = 'orange')

plot_GNSS(ax, 2015, translate = False)
    
legend_dummy()