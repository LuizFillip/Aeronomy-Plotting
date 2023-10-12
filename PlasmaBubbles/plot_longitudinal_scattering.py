import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 


b.config_labels()


def plot_longitudinal_scattering(df):
    
    longs = pb.longitudes()
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        sharey = True,
        nrows = 5, 
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.2)
    
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
            0.8, 
            0.7, 
            info, 
            transform = ax[i].transAxes
            )
        
    b.format_time_axes(ax[4])
    
    title = 'Raw data for each longitude sector'
    
    ax[0].set(
        title = title, 
        xlim = [df.index[0], df.index[-1]],
        yticks = np.arange(0, 6, 1), 
        ylim = [0, 5]
        )
    
    fig.text(
        0.06, 0.35, "ROTI (TECU/min)",
        rotation = "vertical", 
        fontsize = 20
        )
    
    return fig

    
dn = dt.datetime(2013, 3, 20, 21)

ds = pb.concat_files(dn)


ds = ds.loc[~ds['sts'].isin(['lcuz', 'lpmo', 'lpuc'])]

df = b.sel_times(
        ds, 
        dn, 
        hours = 10
        )   


f = plot_longitudinal_scattering(df)

