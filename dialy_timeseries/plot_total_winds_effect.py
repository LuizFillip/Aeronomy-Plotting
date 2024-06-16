import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import PlasmaBubbles as pb 
import base as b 


def plot_roti_in_range(ax, dn):

    start = dn - dt.timedelta(hours = 9, days = 2)
    end = dn + dt.timedelta(days = 3)
    ds = pb.roti_in_range(
        start, end, root = 'E:\\')
    
    ax.scatter(
        ds.index, 
        ds['roti'], 
        c = 'k', 
        s = 5, 
        alpha = 0.6
        )
    
    ax.set(
        ylabel = 'ROTI (TECU/min)',
        ylim = [0, 3], 
        xlim = [start, end],
        yticks = np.arange(0, 4, 1)
        )

def plot_indices_roti_quiet_periods(dn):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 4, 
        sharex = True
        )

    plt.subplots_adjust(hspace = 0.1)

    ds = pl.indexes_in_range(dn, days = 3)


    pl.plot_auroras(ax[0], ds)
    pl.plot_kp(ax[1], ds)
    pl.plot_dst(ax[2], ds)

    plot_roti_in_range(ax[3], dn)

    for a in ax.flat:
        
        a.axvspan(
            dn, 
            dn + dt.timedelta(hours = 14), 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'gray'
            )
        

    b.format_time_axes(
        ax[-1], 
        hour_locator = 12, translate = True)
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        num2white = None
        )
    return 


dn = dt.datetime(2013, 3, 17, 21)
dn = dt.datetime(2015, 12, 20, 21)

plot_indices_roti_quiet_periods(dn)