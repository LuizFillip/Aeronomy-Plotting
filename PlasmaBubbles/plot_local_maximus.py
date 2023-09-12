import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 



year = 2013

df = pb.concat_files(year)

dn = dt.datetime(year, 1, 1, 20)

df = b.sel_times(df, dn, hours = 11)

def plot_local_maximus(df):
    
    times = pb.time_range(df)
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        sharey = True,
        nrows = 5, 
        figsize = (10, 8)
        )
    
    longs = np.arange(-80, -30, 10)
    
    args = dict(marker = 'o', 
                 markersize = 1,
                 linestyle = 'none', 
                 color = 'k'
                 )
    
    c = b.chars()
    
    
    for i, long in enumerate(longs):
        
        long_df = pb.longitude_sector(
            df, 
            long
            )
        
        sel_time = pb.time_dataset(
            long_df, 
            long, 
            times
            )
        
        ax[i].plot(sel_time, **args)
        
        info =  f'({c[i]}) {long}° to {long + 10}°'
            
        ax[i].text(0.02, 0.7, info, 
                transform = ax[i].transAxes)
        
    
        ax[i].set(ylim = [0, 5], 
                  yticks = np.arange(0, 6, 1))
        
        ax[i].axhline(1, lw = 2, color = 'r')
    
    
    b.format_time_axes(ax[4])
    
    
    fig.text(
        0.06, 0.35, "ROTI (TECU/min)",
        rotation = "vertical", 
        fontsize = 20
        )
    
    
    
    fig.suptitle(
        'Maximus for each longitude sector',
        y = 0.95
        )
    
