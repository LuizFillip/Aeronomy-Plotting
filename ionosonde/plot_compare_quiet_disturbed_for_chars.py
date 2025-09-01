import matplotlib.pyplot as plt
import datetime as dt 
import digisonde as dg 
import base as b 
from matplotlib.ticker import MultipleLocator
import numpy as np 

b.sci_format(fontsize = 30)


def plot_compare_quiet_disturbed_for_chars(
        sites, parameter = 'hF', cols = [5, 6]
        ):

    nrows = len(sites)
     
     
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = nrows,
        figsize = (14, nrows * 3), 
        sharex = True, 
        sharey = True
        )
    
    start = dt.datetime(2015, 12, 19)
   
    plt.subplots_adjust(hspace = 0.1)
    window = 3
    
     #'hmF2'
    
    for i, site in enumerate(sites):
     
        name = dg.code_name(site)
        
        s = b.chars()[i]
        
        ax[i].text(
            0.02, 0.8, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
     
    
        qt = dg.repeat_quiet_days(
             site, 
             start, 
             parameter, 
             cols = cols, 
             window = 10
             )
        
        for col in qt.columns:
            qt[col] = b.smooth2(qt[col], 10)
    
        ax[i].plot(
            qt.index, 
            qt['mean'], 
            color = 'purple', 
            lw = 2, 
            label = 'Quiet-time'
            )
        
        ax[i].fill_between(
            qt.index, 
            qt['mean'] - qt['std'], 
            qt['mean'] + qt['std'], 
            color = "purple", 
            alpha = 0.3
            )
    
        df = dg.join_iono_days(
                site, 
                start,
                parameter,
                cols = cols, 
                window = window
                )
        
        df.iloc[:, 0] = b.smooth2(df.iloc[:, 0], 3)
        ax[i].plot(df, lw = 2, label = 'Storm-time')
        
        ax[i].set(xlim = [df.index[0], df.index[-1]])
    
        dates = (np.unique(df.index.date))
            
        for dn in dates:
            ax[i].axvline(dn, lw = 1, linestyle = '--')
    
    b.format_time_axes(
         ax[-1], 
         hour_locator = 12, 
         translate = True, 
         pad = 85, 
         format_date = '%d/%m/%y'
         )
    
    return fig 


sites = [ 'SAA0K', 'BVJ03', 'CAJ2M', 'CGK21']

fig = plot_compare_quiet_disturbed_for_chars(sites)