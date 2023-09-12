import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 

def plot_longitudinal_scattering(df):
    
    longs = np.arange(-80, -30, 10)
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        sharey = True,
        nrows = 5, 
        figsize = (10, 8)
        )
    
    args = dict(
        marker = 'o', 
        markersize = 1,
        linestyle = 'none', 
        color = 'k'
        )
    
    c = b.chars()
    
    for i, long in enumerate(longs):
        
        long_df = pb.longitude_sector(
            df, long)
        
        ax[i].plot(
            long_df['roti'], 
            **args
             )
    
        info =  f'({c[i]}) {long}° to {long + 10}°'
            
        ax[i].text(
            0.02, 
            0.7, 
            info, 
            transform = ax[i].transAxes
            )
        
    b.format_time_axes(ax[4])
    
    ax[0].set(yticks = np.arange(0, 6, 1))
    
    fig.text(
        0.06, 0.35, "ROTI (TECU/min)",
        rotation = "vertical", 
        fontsize = 20
        )
    
    
    fig.suptitle(
        'Raw data for each longitude sector',
        y = 0.95)
    
    return fig
    

year = 2013 
df = pb.concat_files(year)

dn = dt.datetime(year, 1, 1, 20)

df = b.sel_times(df, dn, hours = 11)

f = plot_longitudinal_scattering(df)