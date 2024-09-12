import GEO as gg 
import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np 
import digisonde as dg 
import base as b 
import pandas as pd


def plot_compare_quiet_disturbed(
        translate = False
        ):
    
    if translate:
        
        ylabel = 'Vertical drift (m/s)'
        
    else:
        ylabel = 'Deriva vertical (m/s)'
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3,
        figsize = (16, 10), 
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    start = dt.datetime(2015, 12, 19)
    cols = np.arange(2, 7, 1)
    
    sites = ['SAA0K', 'BVJ03', 'CAJ2M']

    for i, site in enumerate(sites):
        
        qt = dg.repeat_quiet_days(site)
        
        ax[i].plot(qt, label = 'Período calmo')
    
        df = dg.join_iono_days(
                site, 
                start,
                cols = cols, 
                smooth = None 
                )
        
        df = df.interpolate()
        
        df[site] = b.smooth2(df[site], 10)
        
        ax[i].plot(df, label = 'Período perturbado')
    
        ax[i].set(
            ylim = [-30, 40], 
            xlim = [df.index[0], df.index[-1]]
            )
        
        for dn in np.unique(df.index.date):
            
            dusk = gg.dusk_from_site(
                    pd.to_datetime(dn), 
                    site = site[:3].lower(),
                    twilight_angle = 18
                    )
            
            ax[i].axvline(dusk, lw = 1, color = 'k')
        
        
    ax[1].set_ylabel(ylabel)
    
    
    
    ax[0].legend(
        bbox_to_anchor = (0.5, 1.4),
        loc = 'upper center', 
        ncols = 2)
    
    b.format_time_axes(
        ax[-1], hour_locator = 12, 
        translate = translate, 
        pad = 80)
    return fig
    
fig = plot_compare_quiet_disturbed()