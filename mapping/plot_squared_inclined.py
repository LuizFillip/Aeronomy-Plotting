import cartopy.crs as ccrs
import GEO as gg
import base as b 
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import PlasmaBubbles as pb 

b.config_labels()

     

def rectangle(ax, longitudes, latitudes):
    
    square = Polygon(zip(longitudes, latitudes))
    
    x, y = square.exterior.xy
    
    ax.add_patch(plt.Polygon(
        list(zip(x, y)),
        transform=ccrs.PlateCarree(), 
        color = 'red', 
        alpha = 0.5)
        )
    
    
def middle_point(xlim, ylim):
     clat = sum(list(set(ylim))) / 2
     clon = sum(list(set(xlim))) / 2
     
     return clon, clat


def plot_corners(
        ax,
        year,
        radius = 10
        ):
    
    coords = gg.corner_coords(
            year, 
            radius, 
            angle = 45
            )

    x_limits, y_limits = coords[0], coords[1]
    
    out = {}

    for i in range(len(x_limits)):
        
        xlim, ylim = x_limits[i], y_limits[i]
        
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )
                
        clon = round(min(xlim))
        
        out[clon] = (xlim, ylim)
    
    return out
        
def find_closest(arr, val):
   return np.abs(arr - val).argmin()


def ellipse(
        center, 
        angle = 95, 
        semi_major = 10.0, 
        semi_minor = 1.0
        ):
     
    
    angle_rad = np.deg2rad(angle)
    
    t = np.linspace(0, 2 * np.pi, 100)
 
    x = (center[0] + semi_major * np.cos(t) * 
         np.cos(angle_rad) - semi_minor * np.sin(t) * 
         np.sin(angle_rad))
    y = (center[1] + semi_major * np.cos(t) * 
         np.sin(angle_rad) + semi_minor * 
         np.sin(t) * np.cos(angle_rad))
    
    return x, y


def plot_ellipse(ax, year = 2014, lon = -60):
    
    eq_lon, eq_lat  = gg.load_equator(year, values = True)
    
    i = find_closest(eq_lon, lon)
    
    x, y = ellipse((eq_lon[i], eq_lat[i]))
    
    ax.plot(x, y)
    
    ax.fill(x, y, color = 'gray', alpha = 0.5)

def mappping(year):
    fig, ax = plt.subplots(
        dpi=300,
        figsize=(10, 10),
        subplot_kw={
            'projection': ccrs.PlateCarree()
        }
    )

    gg.map_attrs(ax, year)
    
    return fig, ax


year = 2014

dn = dt.datetime(year, 1, 1, 5)
twilight = 18


df = b.load(
    pb.epb_path(
        year, path = 'events3'
        )
    )

ds = b.sel_times(df, dn, hours = 12)






def plot_terminator_and_equator(ax, dn):
 
    eq_lon, eq_lat  = gg.load_equator(dn.year, values = True)
    
    term_lon, term_lat = gg.terminator2(dn, twilight)
    
    ax.scatter(term_lon, term_lat, s = 10)
    
    inter_lon, inter_lat = gg.intersection(
        eq_lon, eq_lat, term_lon, term_lat)
    
    
    ax.scatter(inter_lon, inter_lat, s = 150, color = 'k')


v0 = 100 #m/s
x0 = -60

def velocity(v):
    return v * 3.6
def displacement(x0, v0, dt):
    return x0 + v0 * dt / 111

# for Dt in np.arange(0, 2, 0.1):
    # print(Dt)

    # plt.ioff()
Dt = 0
fig, ax = mappping(year)

delta = dt.timedelta(hours = Dt)

epb_dn = dt.datetime(year, 1, 1, 0) + delta

epb_lon = displacement(x0, velocity(v0), Dt)


plot_terminator_and_equator(ax, epb_dn)
coords = plot_corners(ax, year, radius = 10)


plot_ellipse(ax, lon = epb_lon)


ax.set(title = epb_dn.strftime("%H:%M:%S (UT)"))

name = epb_dn.strftime('%Y%m%d%H%M')

ax.text(0, 1.02, f'EPB drift = {v0} m/s', 
        transform = ax.transAxes)
plt.show()
    # fig.savefig(f'temp/{name}.png')
    
    
    
    # plt.clf()   
    # plt.close()