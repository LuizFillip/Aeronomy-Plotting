import matplotlib.pyplot as plt
import FabryPerot as fp
import pandas as pd 
import base as b 
import datetime as dt 
import numpy as np 


b.config_labels()

def plot_montly_averages(df, parameter = 'tn'):

    dirs = fp.DIRECTIONS
    
    
    fig, ax = plt.subplots(
        figsize = (16, 8), 
        dpi = 300,
        nrows = 2, 
        ncols = 2,
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    dn = dt.datetime(2022, 7, 24, 21)
    ds1 = b.sel_times(df, dn)
    
     
    if parameter == 'tn':
        ylabel = 'Temperature (K)'
        ylim = [700, 1500]
        yticks = np.arange(700, 1600, 200)
    else:
        ylabel = 'Velocity (m/s)'
        ylim = [-100, 300]
        yticks = np.arange(-100, 300, 50)
        
        
    for num, ax in enumerate(ax.flat):
        
        col = dirs[num]
        # print(col)
        ds = pd.pivot(
            df, 
            columns = 'day', 
            index = 'time', 
            values = col 
            )
        ax.plot(ds1['time'], ds1[col], color = 'r', lw = 2,
                label = dn.strftime('%Y-%m-%d'))
        ax.plot(ds, alpha = 0.5, color = 'gray')
        ax.plot(ds.mean(axis = 1), color = 'k', lw = 3)
        
        ax.set(title = dirs[num].capitalize(), 
               ylim = ylim,
               yticks = yticks
               )
        ax.legend(loc = 'upper right')
        # ax.axhline(0, lw = 1.5, linestyle = '--')
    
    fontsize = 30
   
        
        
    fig.text(
        0.05, 0.35, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.45, 0.02, 
        'Universal time', 
        fontsize = fontsize, 
        )
    
    fig.suptitle(df.index[0].strftime('%Y-%B'))

    return fig

infile = 'database/FabryPerot/cj/'
df = fp.join_days(infile, parameter = 'tn')
df  = df.loc[~(df['west'] > 1500)]
fig = plot_montly_averages(df, parameter = 'tn')