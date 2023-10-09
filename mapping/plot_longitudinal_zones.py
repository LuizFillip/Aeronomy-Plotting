import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np 
import datetime as dt
import base as b 
import GNSS as gs 
import PlasmaBubbles as pb 

b.config_labels()

def sel_df(df, dn):
    df = b.sel_times(df, dn)

    delta = dt.timedelta(
        minutes = 9,
        seconds = 59
        )
    return df.loc[
        (df.index >= dn) &
        (df.index < dn + delta)].copy()

def plot_terminators(ax, dn):
    for i in range(5):
        
        delta = dt.timedelta(
            minutes = i * (40 + i))
        
        tlon, tlat = gg.terminator(
            dn + delta, 18
            )
        
        ax.plot(
            tlon, 
            tlat, 
            lw = 2, 
            linestyle = '--'
            )
    


def map_attrs(ax, year):
    
    gg.map_features(ax)
    
    lat = gg.limits(
        min = -30, 
        max = 20, 
        stp = 10
        )
    
    lon = gg.limits(
        min = -90, 
        max = -20, 
        stp = 10
        )    
    
    gg.map_boundaries(ax, lon, lat)
    
    
    gg.mag_equator(
        ax,
        year,
        degress = None
        )





def plot_longitudinal_zones(dn):

    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (9, 9),
        subplot_kw = 
            {
            'projection': ccrs.PlateCarree()
            }
        )
    
  
    map_attrs(ax, dn.year)

    return ax





def plot_filtered_points(
        ax, 
        df, 
        xx, yy, 
        xx1, yy1
        ):
    
    x = df.lon
    y = df.lat
    
    x, y =  gg.filter_between_curves(
        x, y, 
        xx, yy, 
        xx1, yy1
        )
    
    ds = df.loc[df['lon'].isin(x) & 
                df['lat'].isin(y)]
    
    ax.scatter(
        x, y, 
        c = ds['roti'], 
        s = 20, 
        cmap = 'jet'
        )
    



def plot_arrow_annotate(
        ax, 
        nx, ny,
        ex, ey
        ):
    
    ax.annotate(
        '', 
        xy = (nx, ny), 
        xytext = (ex, ey), 
        arrowprops = dict(
            arrowstyle='<->', 
            lw = 2
            )
        )
    
    middle_x = nx + (ex - nx) / 2
    middle_y = ny + (ey - ny) / 2
    
    dis = round(
        np.sqrt(
            pow(nx - ex, 2) + 
            pow(ny - ey, 2)), 2
        )
    
    ax.annotate(
        f'{dis}',
        xy = (middle_x, middle_y + 1), 
        xycoords = 'data',
        fontsize = 25.0,
        textcoords = 'data', 
        ha = 'center',
        color = 'b'
        )



            
def plot_filter_meridians(ax):
    
    lons =  [-81., -73, -64.1, -52.6, -40, -33]
    
    
    for i in range(len(lons) - 1):    
        
        lon = lons[i]
    
        xx, yy  = gg.get_limit_meridians(
            dn,
            lon, 
            delta = 10,
            lat_min = -30, 
            lat_max = 30
            )
        
        ax.plot(xx, yy, lw = 1)
        
        nx, ny = gg.intersec_with_equator(xx, yy, year = 2021)
        
        ax.scatter(nx, ny, s= 100)
        
        xx, yy  = gg.get_limit_meridians(
            dn,
            lons[i + 1], 
            delta = 10,
            lat_min = -30, 
            lat_max = 30
            )
            
        ex, ey = gg.intersec_with_equator(xx, yy, year = 2021)
        
        if lon != -40:
            
            plot_arrow_annotate(
                    ax, 
                    nx, ny,
                    ex, ey
                    )
            
            
path = gs.paths(2021, 3)

dn = dt.datetime(2021, 1, 3, 0, 0)   
ax = plot_longitudinal_zones(dn)


            
df = pb.load_filter(path.fn_roti)


plot_filter_meridians(ax)

df = b.sel_times(df, dn, hours = 1)

x = df.lon
y = df.lat

ax.scatter(
    x, y, 
    c = df['roti'], 
    s = 20, 
    cmap = 'jet',
    vmin = 0, 
    vmax = 3
    )







