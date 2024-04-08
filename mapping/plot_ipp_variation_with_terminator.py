import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import os 
import numpy as np 

b.config_labels(fontsize = 25)




def plot_ipp_on_map(ax, ds, year, colorbar = False):
    
    corners = gg.set_coords(year)
    
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
        plot_term =False,
        y = 4.8
        ):
    """
    Plot terminator of the first occurrence in 
    the region and find the local midnight 
    
    """
    
    key = np.arange(-80, -40, 10)[::-1]
    
    for i, ax in enumerate(axes):
        
        ref_long = key[i]
        
        dusk = pb.terminator(ref_long, start, float_fmt = False)
        
        ax.axvline(dusk, lw = 2)
        
        midnight = gg.local_midnight(
            start, 
            ref_long + 5, delta_day = 1)
        
        ax.axvline(
            midnight, 
            lw = 2,
            color = 'b',
            )
        
        # if i == 0:
        #     ax.text(dusk, y, 'Terminator', 
        #                 transform = ax.transData)
                
        #     ax.text(midnight, y, 'midnight', 
        #             color = 'b',
        #             transform = ax.transData)
        
                
def plot_roti_timeseries(
        axes, 
        df, 
        dn, 
        start,  
        right_ticks = False, 
        vmax  = 2, 
        threshold = 0.25
        ):
        
    sectors = np.arange(-80, -40, 10)[::-1]    
    plot_lines( axes, start, y = vmax + 1.2)
    
    
    for i, ax in enumerate(axes):
        
        sector = sectors[i]
        
        sel = pb.filter_region(df, dn, sector)
        
        pl.plot_roti_points(
            ax, sel, 
            threshold,
            label = False, 
            points_max = True,
            vmax = vmax,
            occurrence = True
            )
            
        ax.text(
            0.01, 1.05, f'Box {i + 1}', 
            transform = ax.transAxes
            )
        
        ax.set(
            ylim = [0, vmax + 1], 
            yticks = list(range(0, vmax + 1, 1)), 
            xlim = [df.index[0], df.index[-1]]
            )
        
        if right_ticks:
            ax.tick_params(
                axis='y', 
                labelright = True, 
                labelleft = False, 
                right = True, 
                left = False
                )
            
        
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
    
    fig, ax_map, axes = b.multi_layout(
        nrows = 4)
    
    
    eq_lon, eq_lat = gg.terminator2(dn, 18)
    
    ax_map.scatter(eq_lon, eq_lat, c = 'k', s = 5)
    
    

    
    gg.plot_rectangles_regions(ax_map, dn.year)
    
    
    gg.map_attrs(
        ax_map, 
        dn.year, 
        grid = False,
        degress = None
        )
    

    plot_roti_timeseries( axes, 
     df, 
     dn, 
     start
        )
    
    plot_ipp_on_map(ax_map, df, dn.year)

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
        root = os.getcwd()
        )
    
    df = b.sel_times(df, start)
            
    dn = range_time(start, 10)
    
    fig = plot_ipp_variation(df, start, dn)
    
    plt.show()
    
    return fig

# start = dt.datetime(2014, 2, 9, 21)
# fig = single_view(start)


