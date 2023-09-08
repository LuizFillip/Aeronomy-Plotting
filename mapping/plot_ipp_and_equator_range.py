from base import load
import numpy as np
from base import (
    sel_times,
    config_labels
)
import pandas as pd
import datetime as dt
import cartopy.crs as ccrs
import GEO as g
import matplotlib.pyplot as plt


config_labels(fontsize = 15)


def map_attrs(ax, dn):

    lat_lims = dict(
        min = -20,
        max = 10,
        stp = 10
    )

    lon_lims = dict(
        min=-90,
        max=-30,
        stp=15
    )

    g.map_features(ax)

    lat = g.limits(**lat_lims)
    lon = g.limits(**lon_lims)

    g.map_boundaries(ax, lon, lat)

    g.mag_equator(ax,
                  year=2014,
                  degress=None
                  )
    
    lon, lat = g.terminator(dn, 18)
    
    ax.plot(lon, lat, 
            color = 'k', 
            linestyle = '--', 
            lw = 2)


def plot_ipp_(ax, ds):
    

    img = ax.scatter(
        ds['lon'],
        ds['lat'],
        c = ds['roti'],
        s = 10,
        cmap = 'jet',
        vmin = 0,
        vmax = 5
    )
    
    return img

    


def concat():
    p = 'database/GNSS/roti/2014/'
    files = ['001.txt', '002.txt']

    df = pd.concat(
        [load(p + f) for f in files]).sort_index()

    return df.loc[df['roti'] < 6]


def sel_df(df, dn):
    df = sel_times(df, dn)

    delta = dt.timedelta(minutes=9,
                         seconds=59)
    return df.loc[
        (df.index >= dn) &
        (df.index < dn + delta)].copy()



def plot_ipp_and_equator_range(
        df, 
        dn, 
        ncols = 3
        ):

    fig, ax = plt.subplots(
        figsize = (12, 5),
        ncols = ncols,
        nrows = 2,
        dpi = 300,
        subplot_kw=
        {'projection': ccrs.PlateCarree()}
    )
    
    plt.subplots_adjust(
        hspace = 0.0,
        wspace = 0.1
    )
    
    
    lons = np.arange(-80, -20, 10)
    

    for i, ax in enumerate(ax.flat):
        
        for long in lons:
    
            ax.axvline(long)
    
        delta = dt.timedelta(hours=i)
    
        time = dn + delta
        
        
        img = plot_ipp_(ax, sel_df(df, time))
    
        map_attrs(ax, time)
    
        ax.set(title = time.strftime('%Hh00 (UT)'))
    
        if i != ncols:
    
            ax.set(xticklabels = [],
                   yticklabels = [],
                   xlabel = '', 
                   ylabel = ''
                   )
        
        else:
            ax.set(xticks = lons)
            
    bounds = np.linspace(1, 5, 5-)
    cbar_ax = fig.add_axes([1., 0.06, 0.02, 0.8])
    fig.colorbar(img, cax=cbar_ax,
                 ticks=np.arange(1,6),
                 boundaries=bounds)
            

df = concat()

dn = dt.datetime(2014, 1, 1, 23, 0)


plot_ipp_and_equator_range(df, dn)