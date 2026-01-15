import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import base as b 
import core as c
import GEO as gg 


b.sci_format(fontsize = 20)



def _devtime(end, start):
    return (end - start).total_seconds() / 3600

def stormtime_spanning(ax, start, end, y = -100):
    
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

def evening_interval(ax, dusk):
    
    ax.axvline(
        dusk, 
        color = 'blue', 
        lw = 2, 
        linestyle = '--'
        )
    
    delta = dt.timedelta(hours = 2)
    
    ax.axvspan(
        dusk - delta, 
        dusk + delta, 
        ymin = 0, 
        ymax = 1,
        alpha = 0.2, 
        color = 'blue'
        )
    
    return None 
 
    


def plot_reference_lines(ax, dusk, dns, start = None, end = None):
  
    
    for a in ax.flat:
        if start is not None:
            a.axvspan(
                start, end, 
                ymin = 0, 
                ymax = 1,
                alpha = 0.2, 
                color = 'tomato'
                )
        
        evening_interval(a, dusk)
        
        for dn in dns:
            a.axvline(dn, lw = 1, linestyle = '--')

        
    return None

def filter_stormtime(dn):
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
    
    return None 

def plot_kp_by_range(ax, dn):
    
    ds = b.range_dates(c.low_omni(), dn, days = 4)
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

def plot_roti_and_indices(dn, ):
    
    dusk = gg.terminator( -50,  dn, 
        float_fmt = False
        )
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 10), 
        nrows = 5, 
        sharex = True
        )

    plt.subplots_adjust(hspace = 0.1)

  
    st, ds = filter_stormtime(dn)
    
    dns = np.unique(ds.index.date)
    
    start, end = set_time_limits(ds)
    
    # geomagnetic storm intervals 
    gs_start, gs_middle, gs_end = tuple(st)
    
    pl.plot_solar_speed(ax[0], ds)
    pl.plot_auroras(ax[1], ds)
    pl.plot_magnetic_fields(ax[2], ds, ylim = 30)
    pl.plot_dst(ax[3], ds)
    pl.plot_kp_by_range(ax[3].twinx(), dn)
    pl.plot_roti_in_range(ax[-1], start, end)
    
    # stormtime_spanning(ax[3], gs_start, dusk)
 
    plot_reference_lines(ax, dusk, dns)
    
    set_axes_time(ax, start, end)
    
    ax[0].set(title = dn.strftime('%B, %Y'))
    
    fig.align_ylabels()
    
    return fig



def main():
    # dn = dt.datetime(2022, 10, 3) # moderate
    # dn = dt.datetime(2018, 3, 13) # no storm 
    dn = dt.datetime(2022, 12, 26)
    dn = dt.datetime(2023, 12, 11)
    '''
    Plot de exemplificação da metolodogia do artigo
    
    '''
    
    df = b.load('core/src/geomag/data/stormsphase')
    
    dn = df.index[0]
    
    dn = dt.datetime(2013, 3, 26)
    
    plot_roti_and_indices(dn)
    
    # pl.savefig(fig, 'Indices_and_example_of_suppression')
    
    plt.show()
    return

df = b.load('core/src/geomag/data/stormsphase')

df = c.geomagnetic_analysis(df)


# df.loc[df['category'] == 'quiet']

main()

