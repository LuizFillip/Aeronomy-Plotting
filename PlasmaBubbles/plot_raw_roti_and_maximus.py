import base as b
import PlasmaBubbles as pb 
import GEO as gg
import numpy as np 

b.config_labels()


args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.2, 
     )
    
def plot_occurrence_events(ax, ds, threshold = 0.25):
    
    events = pb.events_by_longitude(ds['max'], threshold)
    
    line, = ax.plot(
          events, 
          marker = 'o',
          markersize = 3,
          color = 'b'
        )
    
    b.change_axes_color(
            ax, 
            color = 'b',
            axis = "y", 
            position = "right"
            )
    
    ax.set(
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.4]
        )
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = 'b', 
            linestyle = '--'
            )
        
    return events
        

def plot_roti_points(
        ax, ds, 
        threshold = 0.25,
        label = False, 
        points_max = True,
        vmax = 3,
        occurrence = True
        ):
        
    ax.plot(ds['roti'], **args, label = 'ROTI points')
    

    if len(ds) != 0:
        times = pb.time_range(ds)
        
        ax.axhline(
            threshold, 
            color = 'red', 
            lw = 2, 
            label = f'{threshold} TECU/min'
            )
        
        df1 = pb.maximum_in_time_window(ds, 'max', times)
        
        if points_max:
            extra_args = dict(
                marker = 'o', 
                linestyle = 'none', 
                markersize = 3
                )
        else:
            extra_args = dict(markersize = 3)
        
        ax.plot(
            df1, 
            color = 'k',                
            label = 'Valor máximo',
            **extra_args
            )
                
        
        if label:
            ax.set(ylabel = 'ROTI (TECU/min)')
            
        if occurrence:
        
            ax1 = ax.twinx()
            plot_occurrence_events(
                ax1, 
                df1, 
                threshold
                )
        
        if occurrence:
            return df1 
    




def plot_lines( 
        axes, 
        start,  
        plot_term = False,
        y = 4.8, 
        label_top = False
        ):
    """
    Plot terminator of the first occurrence in 
    the region and find the local midnight 
    
    """
    
    key = np.arange(-80, -40, 10)[::-1]
    
    for i, ax in enumerate(axes):
        
        ref_long = key[i]
        
        dusk = gg.terminator(
            ref_long, 
            start, 
            float_fmt = False
            )
        
        ax.axvline(dusk, lw = 2)
        
        midnight = gg.local_midnight(
            start, 
            ref_long + 5, 
            delta_day = 1
            )
        
        if label_top:
            ax.text(dusk, 0.5,
                'Local terminator',
                transform = ax.transData
                )
    
    
    
            ax.text(midnight, 0.5,
                'Local midnight',
                transform = ax.transData
                )
            
        ax.axvline(
            midnight, 
            lw = 2,
            color = 'k',
            linestyle = '--'
            )
        
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
        
        sel = pb.filter_region_and_dn(df, dn, sector)
        
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
            
    
    
    b.format_time_axes(axes[-1])