import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import base as b 
import datetime as dt
import PlasmaBubbles as pb 

def plot_arrows_distance(
        ax, lat, s_lon, lon
        ):
        
    d = g.haversine_distance(
        lat, s_lon, lat, lon
        )
    
    ax.annotate(
        '', 
        xy = (s_lon, lat ), 
        xytext = (lon, lat ), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    middle = lon + (s_lon - lon) / 2
    
    ax.annotate(
        f'{round(d, 2)}',
        xy = (middle, lat + 0.5), 
        xycoords='data',
        fontsize= 15.0,
        textcoords='data', 
        ha='center')

def plot_distance_in_each_sector(
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        subplot_kw={
            'projection': ccrs.PlateCarree()
            }
        )
    
    g.map_features(ax)
    
    lat = g.limits(
        min = -30.0, 
        max = 10, 
        stp = 10
        )
    lon = g.limits(
        min = -80, 
        max = -20, 
        stp = 10
        )    
    
    g.map_boundaries(ax, lon, lat)
    
    # dn = dt.datetime(2022, 1, 1, 0)
    
        
    # g.mag_equator(
    #         ax, 
    #         year = dn.year, 
    #         degress = None
    #         )
    
    for lon in pb.longitudes():
        s_lon = lon + 10
       
        
        ax.axvline(s_lon)
        
        plot_arrows_distance(
                ax, -7, s_lon, lon
                )
    
    

    

plot_distance_in_each_sector(
        lat = -7
        )