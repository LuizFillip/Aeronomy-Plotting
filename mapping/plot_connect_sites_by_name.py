import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import numpy as np 


b.sci_format(fontsize = 25)


def legend_instruments(translate = False):
    
    if translate:
        label = 'Receptores GNSS'
    else:
        label = 'GNSS receivers'
    
    
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
        fontsize = 23,
        handlelength = 2,
        # bbox_to_anchor = (0.75, 0.87),
        labelspacing = 0,
        columnspacing = 0.3, 
        loc = 'upper center'
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
    
    return None 

def plot_GNSS(ax, year, translate = False):

    lon, lat = gg.stations_coordinates(year, distance = 100)

    args = dict( 
        s = 50, 
        marker = '^',
        color = 'red', 
        transform = ccrs.PlateCarree()
        )


    sits, lon, lat = gg.arr_coords(year = 2021)
    ax.scatter(lon, lat, **args)
    
    return None 

stations = {
"Cachoeira\nPaulista" : {"lon": -45.0, "lat": -22.7, 
                        'lat_delta': 0, 'lon_delta': 11.3},
'Eusébio' : {
    "lon": -38.45, "lat": -3.89, 'lat_delta': -8, 'lon_delta': 5}, 
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

def plot_connect_lines():
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (15, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    lat_lims = dict(min = -30, max = 15, stp = 5)
    lon_lims = dict(min = -65, max = -25, stp = 5)
    
    gg.map_attrs(
        ax, 2015,
        degress = None, 
        grid = False, 
        lat_lims = lat_lims,
        lon_lims = lon_lims
        )
    
    plot_GNSS(ax, 2015, translate = False)
        
    for name, s in stations.items():
     
        lat, lon = s['lat'], s['lon']
        lat_delta, lon_delta = s['lat_delta'], s['lon_delta']
        
        curve_connect(
                ax, lat, lon, 
                name, 
                lat_delta, 
                lon_delta)
        
     
        if name[-1] == 'i':
            marker = 'o'
            color = 'green'
            gg.plot_circle(
                    ax, 
                    s["lon"], s["lat"], 
                    radius = 250, 
                    edgecolor = color,
                    lw = 3
                    )
            s = 200
        else:
            marker = 's'
            color = 'k'
            s = 200
            
            
        ax.scatter(
            lon, lat, s = s, 
                   marker = marker, 
                   color = color)
    
    for site in ['São Luís', 'Eusébio']:
        s = stations[site]
        lat, lon = s['lat'], s['lon']
        ax.scatter(
            lon, lat, 
            s = 300, 
            marker = '*', 
            color = 'orange'
            )
        
    legend_instruments()
    
    return fig

def main():
    fig = plot_connect_lines()
    
    FigureName = 'sites_locations'
    
    save_in = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    fig.savefig(save_in + FigureName, dpi = 300 )
    
# main()