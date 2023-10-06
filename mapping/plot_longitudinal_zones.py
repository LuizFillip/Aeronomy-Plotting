import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import datetime as dt
import numpy as np

    
fig, ax = plt.subplots(
    dpi = 300,
    figsize = (9, 9),
    subplot_kw = 
        {
        'projection': ccrs.PlateCarree()
        }
    )

gg.map_features(ax)

lat = gg.limits(
    min = -40, 
    max = 40, 
    stp = 10
    )
lon = gg.limits(
    min = -90, 
    max = -20, 
    stp = 10
    )    

gg.map_boundaries(ax, lon, lat)

dn = dt.datetime(2016,9, 1, 21)

gg.mag_equator(
    ax,
    dn.year,
    degress = None
    )


for lon in np.arange(-90, -20, 5):
    
    xx, yy = gg.meridians(
        dn,
        max_lat = 60,
        delta = 10
        ).compute(lon)
    
    ax.plot(xx,  yy)
    
    # ax.axvline(lon, linestyle = '--')