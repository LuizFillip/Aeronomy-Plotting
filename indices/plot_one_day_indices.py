import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np
import GEO as gg 
import plotting as pl
import core as c 
# PATH = 'database/indices/omni_hourly.txt'

# df = c.category_and_low_indices(
#         col_kp = 'kp_max', 
#         col_dst = 'sym_min'
#         )










b.sci_format(fontsize = 20)




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


def plot_range_day_indices(
        dn, 
        days = 3,
        storm_span = False, 
        double_sup = False,
        root = 'D:\\', 
        clear = None 
        ):
    
    dusk = gg.terminator(dn
        )
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 12), 
        nrows = 5, 
        sharex = True
        )

    plt.subplots_adjust(hspace = 0.1)

    ds, st = c.set_stormtime(
        dn, before = days, after = days)
  
    start, end = set_time_limits(ds)

    pl.plot_solar_speed(ax[0], ds)
    pl.plot_auroral(ax[1], ds)
    pl.plot_magnetic_fields(ax[2], ds, ylim = 30)
    pl.plot_dst(ax[3], ds)
    pl.plot_kp_by_range(ax[3].twinx(), dn)
    pl.plot_electric_field(ax[-1], ds)
     
    if storm_span:
        pl.stormtime_spanning(
            ax[3], st['start'], dusk)
    
    
    for a in ax.flat:
        a.axvline(
            st['main'],
            lw = 2, 
            color = 'purple')
    
    set_axes_time(ax, start, end)
    
    ax[0].set(title = dn.strftime('%B, %Y'))
    
    fig.align_ylabels()
    
    return fig





dn = dt.datetime(2014, 2, 9, 21)
dn = dt.datetime(2019, 3, 19, 21)
dn = dt.datetime(2019, 5, 2, 21)
dn = dt.datetime(2016, 10, 3, 21)
dn = dt.datetime(2017, 8, 30, 21)
dn = dt.datetime(2014, 1, 2, 21)
dn = dt.datetime(2013, 3, 17, 21)
dn = dt.datetime(2022, 7, 24, 21)
dn = dt.datetime(2015, 12, 20, 18)

# dn = dt.datetime(2015, 12, 25, 21)
# dn = dt.datetime(2019, 5, 2, 21)
# dn = dt.datetime(2019, 12, 6, 21)


fig = plot_range_day_indices(dn, days = 3)
    

