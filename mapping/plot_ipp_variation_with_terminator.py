import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
from matplotlib.gridspec import GridSpec
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import os 
import numpy as np 

b.config_labels(fontsize = 25)

def multi_layout(nrows = 4, year = 2014):
    
    fig = plt.figure(
        dpi = 300, 
        figsize = (18, 7)
        )
    
    gs = GridSpec(nrows, 8)
    
    plt.subplots_adjust(wspace = 2.2, hspace = 0.1)
    
    ax_map = fig.add_subplot( gs[:, :nrows], 
        projection = ccrs.PlateCarree()
        )
    
    gg.map_attrs(ax_map, year, grid = False)
    
    ax1 = fig.add_subplot(gs[0, nrows:])
    args = dict(sharey = ax1)
    
    ax2 = fig.add_subplot(gs[1, nrows:], **args)
    ax3 = fig.add_subplot(gs[2, nrows:], **args)
    ax4 = fig.add_subplot(gs[3, nrows:], **args)
    axes = [ax1, ax2, ax3, ax4]
    
    
    
    return fig, ax_map, axes


def plot_ipp_on_map(ax, ds, corners, colorbar = False):
    
        
    for i, key in enumerate(corners.keys()):
        
        xlim, ylim = corners[key]
        
        sel = ds.loc[
            (ds.lon > xlim[0]) & 
            (ds.lon < xlim[1]) & 
            (ds.lat > ylim[0]) & 
            (ds.lat < ylim[1])
            ]
        
        img = ax.scatter(
            sel.lon,
            sel.lat, 
            c = sel.roti, 
            s =  30, 
            vmin = 0, 
            vmax = 2,
            cmap = 'jet'
            )
        
        ticks = np.arange(0, 2, 0.2)
        b.colorbar(img, ax, ticks)
        
 
def plot_lines( 
        axes, 
        start,  
        local_term
        ):
    """
    Plot terminator of the first occurrence in 
    the region and find the local midnight 
    
    """
    
    for i, ax in enumerate(axes):
    
        llon, llat = local_term[i + 1]

        dusk = gg.dusk_time(
                start,  
                lat = llat, 
                lon = llon, 
                twilight = 18
                )
        
        ax.axvline(dusk, lw = 2)
        
        midnight = gg.local_midnight(llon, llat, start)
        
        ax.axvline(
            midnight, 
            lw = 2,
            color = 'b',
            )
        y = 4.8
        if i == 0:
            
            ax.text(dusk, y, 'Terminator', 
                    transform = ax.transData)
            ax.text(midnight, y, 'midnight', 
                    color = 'b',
                    transform = ax.transData)
                
def plot_roti_timeseries(
        axes, 
        df, dn, 
        corners,
        right_ticks = False
        ):
    
    key = list(corners.keys())
    
    for i, ax in enumerate(axes):
        
        xlim, ylim = corners[key[i]]
       
        sel = df.loc[
            (df.index < dn) & 
            (df.lon > xlim[0]) & 
            (df.lon < xlim[1]) & 
            (df.lat > ylim[0]) & 
            (df.lat < ylim[1])
            ]
        
        ax.text(
            0.03, 0.75,
            f'Box {i + 1}', 
            transform = ax.transAxes
            )
    
        pl.plot_roti_points(ax, sel)
        
        ax.set(
            ylim = [0, 4.5], 
            yticks = list(range(0, 5)), 
            xlim = [df.index[0], df.index[-1]]
            )
        
        if right_ticks:
            ax.tick_params(
                axis='y', 
                labelright = True, 
                labelleft = False, 
                right = True, 
                left = False)
            
        
        if i != -1:
            ax.set(xticklabels = [])
            
        # if i == 0:
        #     ax.legend(
        #         bbox_to_anchor = (.5, 1.5), 
        #         loc = "upper center", 
        #         ncol = 2,
        #         columnspacing = 0.7
        #         )
        
    b.format_time_axes(axes[-1])



def plot_ipp_variation(df, start, dn, twilight = 12):
    
    fig, ax_map, axes = multi_layout(
        nrows = 4, year = start.year)
    
   
    eq_lon, eq_lat = pl.plot_terminator_and_equator(
            ax_map, dn, twilight)
    
    corners = pl.plot_corners(
            ax_map,
            start.year,
            radius = 10,
            label = True
            )
    
    local_term = pl.first_of_terminator(
            ax_map, 
            corners, 
            eq_lon, 
            eq_lat
            )
    
    plot_lines( 
            axes, 
            start,  
            local_term)
    
    plot_roti_timeseries(
        axes, df, dn,
        corners
        )
    
    plot_ipp_on_map(ax_map, df, corners)

    fig.suptitle(
        dn.strftime('%d/%m/%Y %H:%M (UT)'),
        y = 1.01
        )
    
    return fig
    
def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)


def single_view(start):
    
    
    df =  pb.concat_files(
        start, 
        root = os.getcwd()
        )
    
    df = b.sel_times(df, start)
            
    dn = range_time(start, 10)
    
    fig = plot_ipp_variation(df, start, dn)
    
    plt.show()
    
    return fig


