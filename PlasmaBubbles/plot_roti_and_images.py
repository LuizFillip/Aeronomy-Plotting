import matplotlib.pyplot as plt
from skimage import io
from PlasmaBubbles as pb 
import os 
import imager as im
import base as b 
import datetime as dt 
import GEO as gg

def roti_limit(dn, sector = -50, root = 'E:\\'):
    
    df = pb.concat_files(dn, root = root)

    df = b.sel_times(df, dn, hours = 11)
    
    # return  df.loc[(df['lon']> -40) & (df['lon'] < -30)]
    return pb.filter_region(df, dn.year, sector)

def plot_roti_points(
        ax, ds, 
        threshold = 0.25,
        label = False, 
        points_max = True,
        vmax = 3,
        occurrence = True, 
        false_filter = None
        ):
        
    ax.plot(ds['roti'], **args, label = 'ROTI points')
    

    if len(ds) != 0:
        
        
        ax.axhline(
            threshold, 
            color = 'red', 
            lw = 2, 
            label = f'{threshold} TECU/min' 
            )
        
        times = pb.time_range(ds)
        
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
                threshold,
                color = 'b',
                false_filter = false_filter
                
                )
            
            # ax1.set_ylabel('Ocorrência', color = 'b')
            
        if occurrence:
            return ax1
    
    return ds

def plot_roti_timeseries(ax_rot, dn, ref_long = -50):
     
     df = roti_limit(dn)
     
     plot_roti_points(
             ax_rot, df , 
             threshold = 0.21,
             label = True
             )
     
     vmax = np.ceil(df['roti'].max()) 
     vmax = 4
     ax_rot.set(
         ylim = [0, vmax + 1], 
         xlim = [df.index[0], df.index[-1]],
         yticks = np.arange(0, vmax + 2, 1)
         )
     
     pl.plot_references_lines(
             ax_rot,
             -50, 
             dn, 
             label_top = 5.2,
             translate = False
             )
     
     b.format_time_axes(ax_rot, translate = False)
     
     return vmax
