import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl 
import digisonde as dg 
import base as b 
import pandas as pd
import numpy as np 


def plot_days_range(ax, site):
    
    dates = pd.date_range(
        '2015-12-19', 
        freq = '1D', 
        periods = 4
        )
    
    out = []
    for dn in dates:
        
        file =  dg.dn2fn(dn, site)

        out.append(dg.IonoChar(
            file,  
            sum_from = None
            ).chars
        )
        
    df = pd.concat(out).sort_index()

    df['hmF2'] = b.smooth2(df['hmF2'], 3)
    
    ax.plot(df['foF2'], color = 'k', lw = 2) 
   
    
    ax1 = ax.twinx()
    
    ax.bar(df.index, df['QF'], width = 0.05, color = 'gray') 
    
    ax1.plot(df['hmF2'], color = 'b', lw = 2)
    
    delta = dt.timedelta(hours = 24)

    ax.set(
        # ylabel = 'foF2 (Hz)',
        ylim = [-1, 20], 
        yticks = np.arange(0, 25, 5), 
        xlim = [dates[0], dates[-1] + delta]
        )
    
    ax1.set(
        # ylabel = 'hmF2 (km)',     
        ylim = [180, 600],
        yticks = np.arange(200, 700, 100)
        
        )
    
    pl.plot_terminators(ax, df, site)
    
    ax.axhline(0, linestyle = ':')
    
        
    return None 

sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']

nrows = len(sites)
fig, ax = plt.subplots(
    dpi = 300, 
    nrows = nrows,
    figsize = (12, 16), 
    sharex = True, 
    sharey = True
    )


plt.subplots_adjust(hspace = 0.1)

for i, site in enumerate(sites):

    plot_days_range(ax[i], site)
    
    name = dg.code_name(site)
    
    s = b.chars()[i]
    
    ax[i].text(
        0.02, 0.8, 
        f'({s}) {name}', 
        transform = ax[i].transAxes
        )

fig.text(
    0.032, 0.42, 
    'foF2 (MHz)', 
    fontsize = 35, 
    rotation = 'vertical'
    )

fig.text(
    0.95, 0.42, 
    'hmF2 (km)', 
    fontsize = 35, 
    rotation = 'vertical'
    )

b.format_time_axes(
    ax[-1], 
    translate = True,
    hour_locator = 12, 
    pad = 85, 
    format_date = '%d/%m/%y'
    )