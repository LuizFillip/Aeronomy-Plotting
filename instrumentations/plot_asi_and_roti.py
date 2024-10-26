import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd 
import imager as im
import datetime as dt 
import plotting as pl

def plot_shades(ax1, n, index, y = 4):
    
    delta = dt.timedelta(minutes = 10)
    
    ax1.text(
        n, y, 
        index, 
        transform = ax1.transData
        )
    
    ax1.axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
    
    return None 
  
def plot_asi_and_roti(start, site = 'CA'):
        
    fig = plt.figure(
        dpi = 300,
        figsize = (16,  12),
        layout = 'constrained'
        )
    
    ncols = 4
    gs = GridSpec(3, ncols)
    
    gs.update(hspace = 0.2, wspace = 0)
     
    times = pd.date_range(start, freq = '45min', periods = 12)
    
    
    ax_rot = plt.subplot(gs[-1, :])
    pl.plot_roti_timeseries(ax_rot, start)
      
    count = 0 
    for row in range(2):
        
        for col in range(ncols):
           
            dn = times[count]
            
            path_asi = im.path_from_closest_dn(
                    dn, 
                    site = site, 
                    )
            
            ax = plt.subplot(gs[row, col])
            
            
            asi = im.DisplayASI(
                path_asi, 
                site, 
                limits = [0.25, 0.99]
                )
            
            asi.display_original(ax)
    
            
            time = im.fn2dn(path_asi).strftime('%Hh%M')
            
            index = count + 1
            info = f'({index}) {time}'
            ax.text(
                0.2, 1.02, info, 
                transform = ax.transAxes
                )
            
            plot_shades(ax_rot, dn, index, y = 4)
            
            count += 1
            
            if count > ncols * 2:  
                break
        
        if count > ncols * 2:  
           break
       
    return fig 

import base as b 

start = dt.datetime(2013, 12, 24, 21)
fig = plot_asi_and_roti(start, site = 'CA')


fig.savefig(b.LATEX('asi_roti', 'posdoc'))