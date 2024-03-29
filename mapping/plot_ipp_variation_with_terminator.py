import GEO as gg
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import os 
import numpy as np 

b.config_labels(fontsize = 25)




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
        local_term,
        plot_term =False,
        y = 4.8
        ):
    """
    Plot terminator of the first occurrence in 
    the region and find the local midnight 
    
    """
    
    key = list(local_term.keys())
    
    for i, ax in enumerate(axes):
        
        ref_long = key[i]
        llon, llat = local_term[ref_long]

        dusk = gg.dusk_time(
                start,  
                lat = llat, 
                lon = llon, 
                twilight = 18
                )
        
        ax.axvline(dusk, lw = 2)

        midnight = gg.local_midnight(start, ref_long + 5)
        
        ax.axvline(
            midnight, 
            lw = 2,
            color = 'b',
            )
        
        if i == 0:
            if plot_term:
                ax.text(dusk, y, 'Terminator', 
                        transform = ax.transData)
                
            ax.text(midnight, y, 'midnight', 
                    color = 'b',
                    transform = ax.transData)
        
                
def plot_roti_timeseries(
        axes, 
        df, dn, 
        start,  
        local_term,
        right_ticks = False
        ):
    
    vmax  = 2
        
    if len(np.unique(df.index.date)) == 1:
        plot_term = False
    else:
        plot_term = True
        
    corners = gg.set_coords( dn.year)
    key = list(corners.keys())
    
    plot_lines( 
            axes, 
            start,  
            local_term,
            plot_term,
            y = vmax 
            )
    
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
            0.03, 0.75, f'Box {i + 1}', 
            transform = ax.transAxes
            )
    
        pl.plot_roti_points(ax, sel)
        
        ax.set(
            ylim = [0, vmax], 
            yticks = list(range(0, vmax + 1)), 
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


