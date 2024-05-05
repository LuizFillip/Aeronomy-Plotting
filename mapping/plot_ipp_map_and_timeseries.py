import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import os 
import numpy as np 

b.config_labels(fontsize = 25)


def plot_ipp_on_map(ax, ds, dn, colorbar = False):
    
    corners = gg.set_coords(dn.year)
    
    for i, sector in enumerate(corners.keys()):
                
        sel = pb.filter_region_and_dn(ds, dn, sector)
        
        ticks = np.arange(0, 2, 0.5)
        
        img = ax.scatter(
            sel.lon,
            sel.lat, 
            c = sel.roti, 
            s =  20, 
            vmin = ticks[0], 
            vmax = ticks[-1],
            cmap = 'jet'
            )
        
        
        b.colorbar(
            img, ax, ticks, 
            anchor = (.05, 0., 1, 1)
            )
        




def plot_ipp_map_and_timeseries(
        df, 
        start, 
        dn, 
        twilight = 12
        ):
    
    fig, ax_map, axes = b.multi_layout(nrows = 4)

    eq_lon, eq_lat = gg.terminator2(dn, 18)
    
    ax_map.scatter(eq_lon, eq_lat, c = 'k', s = 5)
    
    gg.plot_rectangles_regions(ax_map, dn.year)
    
    
    gg.map_attrs(
        ax_map, 
        dn.year, 
        grid = False,
        degress = None
        )
    

    pl.plot_roti_timeseries( 
        axes, 
         df, 
         dn, 
         start,
         occurrence = False
            )
        
    plot_ipp_on_map(ax_map, df, dn)

    fig.suptitle(
        dn.strftime('%d/%m/%Y %H:%M (UT)'),
        y = 1.01
        )
    
    return fig
    
def range_time(start, minutes):
        
    return start + dt.timedelta(minutes = minutes)


def single_view(start):
    
    
    df =  pb.concat_files(
        start, 
        root = os.getcwd(), 
        hours = 12
        )
    
    df = b.sel_times(df, start)
            
    dn = range_time(start, 200)
    
    fig = plot_ipp_map_and_timeseries(df, start, dn)
    
    plt.show()
    
    return fig

# start = dt.datetime(2014, 1, 1, 21)
# fig = single_view(start)


