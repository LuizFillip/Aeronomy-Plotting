import base as b
import numpy as np
import GNSS as gs
import pandas as pd
import datetime as dt
import cartopy.crs as ccrs
import GEO as g
import matplotlib.pyplot as plt
import PlasmaBubbles as pb

b.config_labels(fontsize = 15)


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



def concat_files(year):
     
    out = []
    for i in [1, 2]:
        
        path = gs.paths(year, i)
        
        out.append(
            pb.load_filter(path.fn_roti)
            )
        
        
    return pd.concat(out)


def sel_df(df, dn):
    df = b.sel_times(df, dn)

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
        figsize = (14, 6),
        ncols = ncols,
        nrows = 2,
        dpi = 300,
        subplot_kw =
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
    
        delta = dt.timedelta(hours = i)
    
        time = dn + delta
        
        ds =  sel_df(df, time)
        
        img = ax.scatter(
            ds['lon'],
            ds['lat'],
            c = ds['roti'],
            s = 10,
            cmap = 'jet',
            vmin = 0,
            vmax = 5
        )        
        # img = plot_ipp_(ax,)
    
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
            
    ticks = np.arange(0, 6, 1)
    
    
    b.colorbar_setting(
            img, 
            ax, 
            ticks, 
            width = "6%")
    
    
    s, e = df.index[0], df.index[-1]
    
    m = s.strftime('%m')
    y = s.strftime('%Y')
    s = s.strftime('%d')
    e = e.strftime('%d')
    fig.suptitle(f'{s}-{e}/{m}/{y}')


def main():
    
    year = 2013
    
    df = concat_files(year)
    
    dn = dt.datetime(year, 1, 1, 23, 0)
    
    plot_ipp_and_equator_range(df, dn)
