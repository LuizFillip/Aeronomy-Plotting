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
        xlim = [ds.index[0], ds.index[-1]], 
        xlabel = 'Days'
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
        
def range_dates(dn, days = 2):
    delta = dt.timedelta(days = days)
    
    ds = b.load(PATH)
    
    return b.sel_dates(ds, dn - delta, dn + delta)

def plot_one_day_indices(dn, days = 2):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 4), 
        ncols = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(wspace = 0.3)
    
    ds = range_dates(dn, days = days)
     
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
dn = dt.datetime(2019, 3, 19, 21)
dn = dt.datetime(2017, 9, 17, 21)
dn = dt.datetime(2019, 5, 2, 21)
dn = dt.datetime(2022, 7, 24, 21)
dn = dt.datetime(2016, 10, 3, 21)
dn = dt.datetime(2017, 8, 30, 21)
dn = dt.datetime(2014, 1, 2, 21)

dn = dt.datetime(2013, 3, 17, 21)


days = 8
df = range_dates(dn, days = days)

plot_one_day_indices(dn, days = days)

vls = df['dst'].values 


vls.min()