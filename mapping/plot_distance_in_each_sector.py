import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import base as b 
import datetime as dt
import PlasmaBubbles as pb 

def plot_arrows_distance(
        ax, 
        lat, 
        s_lon, 
        lon,
        color = 'b'
        ):
        
    d = g.haversine_distance(
        lat, s_lon, lat, lon
        )
    
    arrow =ax.annotate(
        '', 
        xy = (s_lon, lat ), 
        xytext = (lon, lat ), 
        arrowprops = dict(
            arrowstyle = '<->', 
            color = color, 
            lw = 2
            ), 
        
        label = 'distance (km)')
    
    middle = lon + (s_lon - lon) / 2
    
    ax.annotate(
        f'{round(d, 2)}',
        xy = (middle, lat + 0.5), 
        xycoords = 'data',
        fontsize = 20.0,
        textcoords = 'data', 
        ha = 'center',
        color = color
        )
    
    return arrow

def plot_distance_in_each_sector():
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12,12),
        subplot_kw = {
            'projection': ccrs.PlateCarree()
            }
        )
    
    g.map_features(ax, grid = False)
    
    lat = g.limits(
        min = -30.0, 
        max = 10, 
        stp = 10
        )
    lon = g.limits(
        min = -90, 
        max = -30, 
        stp = 10
        )    
    
    g.map_boundaries(ax, lon, lat)
    
    g.mag_equator(
        ax,
        2013,
        degress = None
        )
    
    ref_lat = 5
    step = 5
    for i, lon in enumerate(g.longitudes(
            start = -90, 
     end = -30, step = step)):
        s_lon = lon + step
       
        
        ax.axvline(s_lon)
        
        # plot_arrows_distance(
        #         ax, ref_lat, s_lon, lon
        #         )
        
        arrow = plot_arrows_distance(
                ax, ref_lat - i * 3, 
                s_lon , lon -step * i
                )
    
    

    plt.legend([arrow,], ['My label',])


plot_distance_in_each_sector()