import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import numpy as np
import base as b 
import datetime as dt

fig, ax = plt.subplots(
    dpi = 300,
    figsize = (10, 10),
    subplot_kw={
        'projection': ccrs.PlateCarree()
        }
    )

g.map_features(axs)

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

    
g.mag_equator(
        ax, 
        year = dn.year, 
        degress = None
        )

fig.suptitle(
    dn.strftime('%d/%m/%Y'), 
    y = 0.85
    )