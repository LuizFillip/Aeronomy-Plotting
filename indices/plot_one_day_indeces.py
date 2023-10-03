import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np


KP_PATH = 'database/indices/Kp_hourly.txt'
DST_PATH = 'database/indices/kyoto2000.txt'

def plot_kp(ax, dn):
    
    df = b.load(KP_PATH)
    ds = b.sel_times(df, dn, hours = 14)
    ax.bar(
        ds.index, 
        ds['Kp'], 
        width = 0.1
        )
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 10], 
        yticks = np.arange(0, 11, 2),
        xlim = [ds.index[0], ds.index[-1]]
        )
    
    ax.axhline(4, lw = 2, color = 'r')

def plot_dst(ax, dn):
    
    df = b.load(DST_PATH)
    ds = b.sel_times(df, dn, hours = 14)
    
    ax.plot(ds)
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [-100, 50],
        ylabel = "Dst (nT)"
        )
    
    for limit in [-50, -100]:
        ax.axhline(limit, lw = 2, color = 'r')
        

def plot_one_day_indices():
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (10, 4), 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    dn = dt.datetime(2016, 4, 3, 18)
    
    plot_kp(ax[0], dn)
    plot_dst(ax[1], dn)
    
    b.format_time_axes(ax[1], hour_locator = 1)



