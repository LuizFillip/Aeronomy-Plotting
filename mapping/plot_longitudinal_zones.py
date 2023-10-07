import GEO as gg
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import datetime as dt
import numpy as np
import base as b 
import pandas as pd

b.config_labels()

# def sel_df(df, dn):
#     df = b.sel_times(df, dn)

#     delta = dt.timedelta(minutes=9,
#                          seconds=59)
#     return df.loc[
#         (df.index >= dn) &
#         (df.index < dn + delta)].copy()


# dn = dt.datetime(2013, 1, 1, 23, 0)

# df = pb.concat_files(dn)

# df = sel_df(df, dn)




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
    max = 20, 
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



def filter_latitudes(
        xx, yy, 
        lat_min = -30, 
        lat_max = 20
        ):
    yy = np.where(
        (yy < lat_min) | 
        (yy > lat_max ), 
        np.nan, yy
        )
    
    mask = np.isnan(yy)
        
    return xx[~mask], yy[~mask]

def get_line_eq(x0, x1, y0, y1):
    return y0 - y1, x1 - x0, x0 * y1 - x1 * y0

def filter_between_curves(x, y, xx, yy, xx1, yy1):

    ar, br, cr = get_line_eq(
        xx[0], xx[-1], yy[0], yy[-1])
    
    mask1 = ((x < xx[0]) | (x < xx[-1]) & 
             (ar * x + br * y + cr <= 0))
    
    ar, br, cr = get_line_eq(
        xx1[0], xx1[-1], yy1[0], yy1[-1])
    
    mask2  = ((x > xx1[-1]) | (x > xx1[0]) & 
              (ar * x + br * y + cr >= 0))
    
    x = x[~(mask1 | mask2)]
    y = y[~(mask1 | mask2)]

    return x, y

lon = -60
xx, yy = gg.meridians(
    dn,
    max_lat = 60,
    delta = 10
    ).compute(lon)








lon = -50
xx1, yy1 = gg.meridians(
    dn,
    max_lat = 60,
    delta = 10
    ).compute(lon)


xx, yy = filter_latitudes(xx, yy)
ax.plot(xx,  yy, lw = 3)
xx1, yy1 = filter_latitudes(xx1, yy1)
ax.plot(xx1,  yy1, lw = 3)


N = 800
x = np.random.uniform(-80, -20, N)
y = np.random.uniform(-30, 20, N)



x, y = filter_between_curves(x, y, xx, yy, xx1, yy1)
ax.scatter(x, y, color = 'r')

