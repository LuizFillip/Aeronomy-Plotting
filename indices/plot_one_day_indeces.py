import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np

b.config_labels()
PATH = 'database/indices/omni_hourly.txt'

def plot_kp(ax, ds):
    
    ax1 = ax.twinx()
    
    line, = ax1.plot(ds['f107'], lw = 2, color = 'red')
    
    b.change_axes_color(
            ax1, 
            color = line.get_color(),
            axis = "y", 
            position = "right"
            )
    
    ax1.set(ylabel = '$F_{10.7} ~(sfu)$')
    
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
        # xlabel = 'Days'
        )
    
    ax.axhline(3, lw = 2, color = 'k', linestyle = '--')
    

def plot_dst(ax, ds, ylim = [-100, 50]):
    
    ax.plot(ds['dst'], lw = 2)
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = ylim,
        yticks = np.arange(ylim[0], ylim[-1] + 50, 50),
        ylabel = "Dst (nT)"
        )
    
    ax.axhline(0, lw = 1, color = 'k', linestyle = '-')
    
    for limit in [-50, -150]:
        ax.axhline(
            limit, 
            lw = 2, 
            color = 'k', 
            linestyle = '--'
            )
        
def range_dates(dn, PATH, days = 2):
    delta = dt.timedelta(days = days)
    
    ds = b.load(PATH)
    
    return b.sel_dates(ds, dn - delta, dn + delta)


def plot_auroral_indices(ax, ds):
    
    ax.plot(ds['ap'])

def plot_one_day_indices(dn, days = 2):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 8), 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    ds = range_dates(dn, PATH, days = days)
     
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
    
    return fig 



dn = dt.datetime(2014, 2, 9, 21)
dn = dt.datetime(2019, 3, 19, 21)
dn = dt.datetime(2017, 9, 17, 21)
dn = dt.datetime(2019, 5, 2, 21)
dn = dt.datetime(2016, 10, 3, 21)
dn = dt.datetime(2017, 8, 30, 21)
dn = dt.datetime(2014, 1, 2, 21)
dn = dt.datetime(2013, 3, 17, 21)
dn = dt.datetime(2022, 7, 24, 21)


days = 2

df = range_dates(dn, PATH, days = days)

fig = plot_one_day_indices(dn, days = days)

