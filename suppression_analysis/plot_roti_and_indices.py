import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import epbs as pb 
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
        ylabel = 'ROTI (TECU/min)',
        ylim = [0, 5], 
        yticks = np.arange(0, 6, 1),
        
        
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

def reference_ln_one_axes(a, dusk, start, end, dns):
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
def plot_reference_lines(ax, dusk, start, end, dns):

   
    if len(ax) > 1:
        for a in ax.flat:
            reference_ln_one_axes(a, dusk, start, end, dns)
    else:
        reference_ln_one_axes(ax, dusk, start, end, dns)
        
        
    return None

def load_storm(dn):
    ds = c.high_omni(dn.year)
    
    ds = b.range_dates(ds, dn, days = 4)
    st = c.find_storm_interval(ds['sym'])
    
    return st, ds

def set_time_limits(ds):
    dates = np.unique(ds.index.date)
    delta = dt.timedelta(days = 2)
    start = dates[0] + delta   
    end = dates[-1] 
    return start, end
    
 
def set_axes_time(ax, start, end):

    b.axes_hour_format(
         ax[-1], 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    ax[-1].set(
        xlabel = 'Universal time', 
        xlim = [start, end]
        )

    b.adding_dates_on_the_top(
           ax[0], 
           fmt = '%d/%m'
           )
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        fontsize = 25,
        num2white = None
        )

def plot_kp(ax, dn):
    
    ds = b.range_dates( c.low_omni(), dn, days = 4)
    ds = ds.resample('3H').mean() 
    ax.bar(
        ds.index, 
        ds['kp'] / 10, 
        width = 0.1,
        color = 'gray', 
        alpha = 0.5
        )
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 12], 
        yticks = np.arange(0, 12, 2)
        )
    
    ax.axhline(3, lw = 2, color = 'r')
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

  
    st, ds = load_storm(dn)
    
    start, end = set_time_limits(ds)
    
    estart, emiddle, eend = tuple(st)
    
    pl.plot_auroras(ax[0], ds)
    pl.plot_magnetic_fields(ax[1], ds, ylim = 30)
    pl.plot_dst(ax[2], ds)
    plot_kp(ax[2].twinx(), dn)
    
    dns = plot_roti_in_range(ax[3], start, end)
    
    plot_arrow_and_note(ax[2], estart, dusk)
    plot_reference_lines(ax, dusk, estart, eend, dns)
    
    set_axes_time(ax, start, end)
    
    ax[0].set(title = dn.strftime('%B, %Y'))
    
    fig.align_ylabels()
    
    return fig



def main():
    # dn = dt.datetime(2022, 10, 3) # moderate
    # dn = dt.datetime(2018, 3, 13) # no storm 
    dn = dt.datetime(2022, 12, 26)
    dn = dt.datetime(2023, 12, 11 )
    
    
    df = b.load('core/src/geomag/data/stormsphase')
    
    dn = df.index[0]
    
    fig = plot_roti_and_indices(dn)
    
    # df = c.geomagnetic_analysis(df)
    
    
    # # df.loc[df['category'] == 'intense']

