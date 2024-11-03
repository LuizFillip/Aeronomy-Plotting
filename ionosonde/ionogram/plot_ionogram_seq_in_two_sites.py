import matplotlib.pyplot as plt
import plotting as pl
import datetime as dt 
import digisonde as dg 
import os 
import pandas as pd 


start = dt.datetime(2022, 7, 25, 1)

times = pd.date_range(start, freq = '1H', periods = 6)


fig, ax = plt.subplots(
    figsize = (20, 14), 
    ncols = len(times), 
    nrows = 2,
    )

plt.subplots_adjust(hspace = 0.15, wspace=0)


for i, dn in enumerate(times):
    
    title = dn.strftime('%Hh%M')
    
    fname = dg.path_from_site_dn(dn, 'FZA0M')
    
    pl.plot_single_ionogram(
        fname, 
        ax[0, i], 
        label = True, 
        ylim = [100, 1200]
        )
    
    ax[0, i].set(
      
        yticklabels = [], 
        xticklabels = [], 
        xlabel = '', 
        ylabel = ''
        )
    ax[0, i].text(
        0.3, 0.85, 
        title, color = 'w',
        transform = ax[0, i].transAxes
        )
    
    fname = dg.path_from_site_dn(dn, 'CAJ2M')
    
    plot_single_ionogram(
        fname, 
        ax[1, i],
        label = True, 
        ylim = [100, 1200]
        )
    
    ax[1, i].text(
        0.3, 0.85, title, color = 'w',
                  transform = ax[1,i].transAxes)
    
    if i != 0:
      
        ax[1, i].set(
            yticklabels = [], 
            xticklabels = [], 
            xlabel = '', 
            ylabel = ''
            )

y = 1.03
x = 0.01
fontsize = 45
ax[1, 0].text(
    x, y, 
    '(b) Cachoeira Paulista', 
    fontsize = fontsize,
    transform = ax[1, 0].transAxes
    )


ax[0, 0].text(
    x, y,
    '(a) Fortaleza', 
    fontsize = 40,
    transform = ax[0, 0].transAxes
    
    )