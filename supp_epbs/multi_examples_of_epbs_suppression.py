import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
import base as b 
import core as c
import GEO as gg 
import numpy as np 


def plot_sym_h(ax, dn, before = 4, after = 4):
    
    ds = c.high_omni(dn.year)
    ds = b.range_dates(ds, dn, before, after)
    st = c.find_storm_interval(ds['sym'])
   
    ax1 = ax.twinx()

    pl.plot_dst(ax1, ds, color = 'red')
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    return np.unique(ds.index.date), st 

def set_axis(ax):
    b.axes_hour_format(
         ax, 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    b.adding_dates_on_the_top(
            ax, 
            fmt = '%d/%m/%y', 
            pad = -30
            )
    
    return None




def plot_single_case(
        ax, 
        dn, 
        days = 4, 
        double_sup = True, 
        root = 'D:\\'
        ):
    
    dusk = gg.terminator(-50, dn, float_fmt = False)
    
    dates, st =  plot_sym_h(ax, dn, days = days)
    
    delta = dt.timedelta(days = 2)
    start = dates[0] + delta
    
    end = dates[-1] 
    
    ds = pl.plot_roti_in_range(
        ax, start, end, root = root)
       
    gs_start, gs_middle, gs_end = tuple(st)
    
    # pl.plot_reference_lines(ax, dusk, estart, eend, dns)
    
    pl.stormtime_spanning(ax, gs_start, gs_end)
    
    set_axis(ax)
    
    ax.set(
        xlim = [start, end]
        )
    
    dns = np.unique(ds.index.date)
    
    ax.axvspan(
        gs_start, gs_end, 
        ymin = 0, 
        ymax = 1,
        alpha = 0.2, 
        color = 'tomato'
        )

    pl.evening_interval(ax, dusk, double_sup)
    
    for dn in dns:
        ax.axvline(dn, lw = 1, linestyle = '--')
    
    return None 
    
def check_double_sup(dn):
    delta = dt.timedelta(days = 1)
    df = c.category_and_low_indices()
    
    next_day = dn + delta
    if next_day in df.index:
        return True
    else:
        return False
            
      
    
def plot_multi_examples_of_suppression(dates):
    nrows = len(dates)
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharey = True,
        figsize = (16, 3 * nrows), 
        nrows = nrows
        )
    
    for i, dn in enumerate(dates):
        
        plot_single_case(
            ax[i], 
            dn, 
            double_sup = check_double_sup(dn)
            )
        
        if i < nrows - 1:
            ax[i].set(xticklabels = [])
        
    
    fig.align_ylabels()
    
    ax[-1].set(xlabel = 'Universal time')
    
    b.plot_letters(
        ax, 
        y = 1.02, 
        x = 0., 
        fontsize = 25
        )

    return fig

def main():
    #disturbed
    dates = [ 
        dt.datetime(2013, 3, 17),
        dt.datetime(2015, 3, 17),
        dt.datetime(2016, 3, 14),
        dt.datetime(2017, 3, 1),
        dt.datetime(2022, 10, 3)
        ]
    
    #quiets
    # dates = [
    #     dt.datetime(2014, 9, 9),
    #     dt.datetime(2016, 9, 22),
    #     dt.datetime(2017, 1, 23),
    #     dt.datetime(2019, 3, 13),
    #     dt.datetime(2022, 9, 10)
    #     ]

    
    fig = plot_multi_examples_of_suppression(dates)
    

    # pl.savefig(fig, 'multi_examples_quiettime')
    
# main()

dn =  dt.datetime(2015, 3, 17)
# dn = dt.datetime(2013, 3, 17)

