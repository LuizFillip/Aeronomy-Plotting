import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import PlasmaBubbles as pb 
import base as b 
import core as c
import GEO as gg 


b.sci_format(fontsize = 20)


def plot_roti_in_range(ax, start, end):

    ds = pb.longterm_raw_roti(start, end)
    
    ax.scatter(
        ds.index, 
        ds['roti'], 
        c = 'k', 
        s = 5, 
        alpha = 0.6
        )
    
    ax.set(
        ylabel = 'ROTI',
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        xlim = [ds.index[0] + dt.timedelta(hours = 12), 
                ds.index[-1]]
        
        )
    
    dns = np.unique(ds.index.date)
    
    return dns 

def _devtime(end, start):
    return (end - start).total_seconds() / 3600

def plot_arrow_and_note(ax, start, end, y = -100):
    
    devtime = _devtime(end, start)
    
    time = round(devtime, 2)
        
    middle = end + (start - end) / 2
      
    ax.annotate(
        '', 
        xy = (start, y), 
        xytext = (end, y), 
        arrowprops = dict(arrowstyle='<->')
        )
    time = round(time, 2)
    
    ax.annotate(
        f'{time} hrs',
        xy = (middle, y + 5), 
        xycoords = 'data',
        fontsize = 20.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
    return None     

def plot_reference_lines(ax, dusk, start, end, dns):
    
    for a in ax.flat:
    
        a.axvline(
            dusk, 
            color = 'blue', 
            lw = 2, 
            linestyle = '--'
            )
    
        a.axvspan(
            start, end, 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'tomato'
            )
        
        delta = dt.timedelta(hours = 2)
        a.axvspan(
            dusk - delta, 
            dusk + delta, 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'blue'
            )
        
        for dn in dns:
            a.axvline(dn, lw = 1, linestyle = '--')
               
    return None
def plot_roti_and_indices(dn):
    
    dusk = gg.terminator( -50,  dn, 
        float_fmt = False
        )
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 10), 
        nrows = 4, 
        sharex = True
        )

    plt.subplots_adjust(hspace = 0.1)


    ds = c.high_omni(dn.year)
    
    ds = b.range_dates(ds, dn, days = 3)
    st = c.find_storm_interval(ds['sym'])
    estart, emiddle, eend = tuple(st)
    
    start = dn - dt.timedelta(days = 1)
    end = dn + dt.timedelta(days = 2)
    
    pl.plot_auroras(ax[0], ds)
    pl.plot_magnetic_fields(ax[1], ds, ylim = 30)
    pl.plot_dst(ax[2], ds)
    dns = plot_roti_in_range(ax[3], start, end)
    
    plot_arrow_and_note(ax[2], estart, dusk)
    plot_reference_lines(ax, dusk, estart, eend, dns)
    
    b.axes_hour_format(
         ax[-1], 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    ax[-1].set(xlabel = 'Universal time')
    
    b.adding_dates_on_the_top(
           ax[0], 
           start = start - dt.timedelta(days = 1), 
           end = dns[-1], 
           fmt = '%d/%m'
           )
   
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        num2white = None
        )
    
    ax[0].set(title = dn.strftime('%B, %Y'))
    
    fig.align_ylabels()
    
    return fig




# dn = dt.datetime(2022, 10, 3) # moderate
# dn = dt.datetime(2018, 3, 13) # no storm 
# # dn = dt.datetime(2022, 9, 5)


# fig = plot_roti_and_indices(dn)