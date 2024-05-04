import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np

b.config_labels()
PATH = 'database/indices/omni_hourly.txt'

def plot_kp(ax, ds):
    ds = ds.resample('3H').mean()
    ax.bar(
        ds.index, 
        ds['kp'], 
        width = 0.09,
        color = 'gray',
        alpha = 0.5, 
        edgecolor = 'k'
        )
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 10], 
        yticks = np.arange(0, 10, 2),
        xlim = [ds.index[0], ds.index[-1]]
        )
    
    ax.axhline(3, lw = 2, color = 'k', linestyle = '--')
    

def plot_dst(ax, ds):
    
    
    ax.plot(ds['dst'])
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [-200, 50],
        yticks = np.arange(-200, 100, 50),
        ylabel = "Dst (nT)", 
        xlabel = 'Days'
        )
    
    ax.axhline(0, lw = 1, color = 'k', linestyle = '-')
    
    for limit in [-50, -150]:
        ax.axhline(
            limit, 
            lw = 2, 
            color = 'k', 
            linestyle = '--'
            )
        
def range_dates(dn):
    delta = dt.timedelta(days = 2)
    
    ds = b.load(PATH)
    
    return b.sel_dates(ds, dn - delta, dn + delta)

def plot_one_day_indices(dn):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 8), 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    ds = range_dates(dn)
     
    plot_kp(ax[0], ds)
    plot_dst(ax[1], ds)
    
    
    b.format_days_axes(ax[1])
    
    delta = dt.timedelta(hours = 12)
    for i in range(2):
        ax[i].axvspan(
            dn, dn + delta, 
            ymin = 0, ymax = 1,
            alpha = 0.2, 
            color = 'gray'
            )
        
    b.plot_letters(ax, y = 0.85, x = 0.03)



dn = dt.datetime(2014, 2, 9, 21)

plot_one_day_indices(dn)