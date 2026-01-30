import numpy as np
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt 
import base as b 
import core as c
import GEO as gg 


b.sci_format(fontsize = 20)

def evening_interval(ax, dusk, double = False):
    
    def plot_evening(ax, dusk):
        ax.axvline(
            dusk, 
            color = 'blue', 
            lw = 2, 
            linestyle = '--'
            )
        
        delta_shade = dt.timedelta(hours = 2)
        
        ax.axvspan(
            dusk - delta_shade, 
            dusk + delta_shade, 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'blue'
            )
        
        return None 
    
    if double:
        delta_day = dt.timedelta(days = 1)
        for dn in [dusk, dusk + delta_day]:
            plot_evening(ax, dn)
    else:
        plot_evening(ax, dusk)
    
    return None 
 
    


def plot_reference_lines(
        ax, dusk, dns,
        start = None, 
        end = None, 
        storm_span = True,  
        double = True         
        ):
  
    for a in ax.flat:
        if storm_span:
            a.axvspan(
                start, end, 
                ymin = 0, 
                ymax = 1,
                alpha = 0.2, 
                color = 'tomato'
                )
        
        evening_interval(
            a, dusk, double = double
            )
              
        for dn in dns:
            a.axvline(dn, lw = 1, linestyle = '--')
    return None



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
        y = 0.75, 
        x = 0.02, 
        fontsize = 25,
        num2white = None
        )
    
    return None 


def plot_roti_and_indices(
        dn, 
        storm_span = True, 
        double_sup = False,
        root = 'D:\\', 
        clear = None 
        ):
    
    dusk = gg.terminator(dn
        )
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 10), 
        nrows = 5, 
        sharex = True
        )

    plt.subplots_adjust(hspace = 0.1)

    ds, st = c.set_stormtime(
        dn, before = 4, after = 4)
    dns = np.unique(ds.index.date)
    
    #days intervals (for limits)
    start, end = set_time_limits(ds)

    pl.plot_solar_speed(ax[0], ds)
    pl.plot_auroral(ax[1], ds)
    pl.plot_magnetic_fields(ax[2], ds, ylim = 30)
    pl.plot_dst(ax[3], ds)
    pl.plot_kp_by_range(ax[3].twinx(), dn)
    pl.plot_roti_in_range(
        ax[-1], 
        start, end, 
        root = root, 
        clear = clear
        )
     
    if storm_span:
        pl.stormtime_spanning(
            ax[3], st['start'], dusk)
    
    double = c.check_double_sup(dn)
    
    plot_reference_lines(
        ax, dusk, dns, 
        st['start'], st['end'], 
        storm_span = storm_span,  
        double  = double 
        )
    
    for a in ax.flat:
        a.axvline(
            st['main'],
            lw = 2, 
            color = 'purple')
    
    set_axes_time(ax, start, end)
    
    ds = c.category_and_low_indices()
    name = ds.loc[dn, 'category']
    ax[0].set(title = dn.strftime('%B, %Y - ') + name)
    
    fig.align_ylabels()
    
    return fig



def main():
    # dn = dt.datetime(2022, 10, 3) # moderate
    # dn = dt.datetime(2018, 3, 13) # no storm 
    dn = dt.datetime(2022, 12, 26)

    dn = dt.datetime(2013, 1, 26) #Paper example
    dn = dt.datetime(2015, 3, 17)
    dn = dt.datetime(2014, 9, 24)
    dn = dt.datetime(2016, 9, 18)
    dn = dt.datetime(2023, 4, 9)
    dn = dt.datetime(2016, 12, 21)
    dn = dt.datetime(2014, 9, 9)
    dn = dt.datetime(2017, 2, 13)
    
dn = dt.datetime(2013, 1, 26)
fig = plot_roti_and_indices(dn)
    
