import matplotlib.pyplot as plt 
import base as b
import datetime as dt  
import os 
import PlasmaBubbles as pb 




args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.2, 
     )
    


def plot_roti_points(ax, ds, threshold = 0.25):
        
    ax.plot(ds['roti'], **args, 
            label = 'ROTI points')
    
    times = pb.time_range(ds)
    
    ax.axhline(0.25, color = 'red', lw = 2, 
                label = f'{threshold} TECU/min')
    
    df1 = pb.time_dataset(ds, 'max', times)
    
    ax.plot(df1, 
            color = 'k',
            marker = 'o', 
            markersize = 3, 
            linestyle = 'none',
            label = 'Maximum value')
    
    ax.set(yticks = list(range(0, 4)), 
           ylabel = 'ROTI (TECU/min)')
    
    ax.legend(loc = 'upper right')
    
   
    
    return df1['max']

def plot_occurrence_events(ax, ds):
    
    ax.plot(
          pb.events_by_longitude(ds, 0.25), 
          marker = 'o',
          markersize = 3,
          color = 'k'
        )
    
    ax.set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.4]
        )
    
    b.format_time_axes(ax)
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
        
        
import GEO as gg 

dn = dt.datetime(2013, 3, 31, 20)


df = pb.concat_files(
        dn, 
        root  = 'D:\\'
        )

fig, ax = plt.subplots(
    dpi = 300, 
    nrows = 2,
    sharex= True,
    figsize = (12, 8)
    )

df = b.sel_times(df, dn)

coords = gg.set_coords(dn.year, radius = 10)

df = pb.filter_coords(df, -50, coords)

df1 = plot_roti_points(ax[0], df, threshold = 0.25)


        
plot_occurrence_events(ax[1], df1)

