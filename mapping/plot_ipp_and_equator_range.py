import base as b
import numpy as np
import cartopy.crs as ccrs
import GEO as g
import matplotlib.pyplot as plt
import PlasmaBubbles as pb
import datetime as dt

b.config_labels()


def map_attrs(ax, dn):

    lat_lims = dict(
        min = -30,
        max = 10,
        stp = 10
    )

    lon_lims = dict(
        min = -90,
        max = -30,
        stp = 15
    )

    g.map_features(ax)

    lat = g.limits(**lat_lims)
    lon = g.limits(**lon_lims)

    g.map_boundaries(ax, lon, lat)

    g.mag_equator(
        ax,
        year = 2014,
        degress = None
        )
    
    lon, lat = g.terminator(dn, 18)
    
    ax.plot(lon, lat, 
            color = 'k', 
            linestyle = '--', 
            lw = 2)







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
        hspace = 0.2,
        wspace = 0.1
    )
    

    for i, ax in enumerate(ax.flat):
        
     
        for long in pb.longitudes():
        
            ax.axvline(long, 
            linestyle = '--')
    
        delta = dt.timedelta(hours = i)
    
        time = dn + delta
        
        
        ds = b.sel_df(df, time)
        
        img = ax.scatter(
            ds['lon'],
            ds['lat'],
            c = ds['roti'],
            s = 10,
            cmap = 'jet',
            vmin = 0,
            vmax = 5
        )        
    
        map_attrs(ax, time)
    
        ax.set(title = time.strftime('%Hh00 (UT)'))
    
        if i != ncols:
    
            ax.set(xticklabels = [],
                   yticklabels = [],
                   xlabel = '', 
                   ylabel = ''
                   )
        
        else:
            ax.set(xticks = pb.longitudes())
            
    ticks = np.arange(0, 6, 1)
    
    
    b.colorbar_setting(
            img, 
            ax, 
            ticks, 
            width = "6%")
    
    
    s, e = df.index[0], df.index[-1]
    
  
    s = s.strftime('%d')
    e = e.strftime('%d/%m/%Y')
    fig.suptitle(f'{s}-{e}')
    
    return fig


# def main():
    


# fig = plot_ipp_and_equator_range(df, dn)

