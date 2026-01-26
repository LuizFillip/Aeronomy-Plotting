import matplotlib.pyplot as plt 
import plotting as pl 
import datetime as dt 
import base as b 
import core as c
import GEO as gg 
import numpy as np 

b.sci_format(fontsize = 25)

def plot_sym_h(ax, ds, ylim = [-250, 50], step = 50):
    
    ax1 = ax.twinx()

    pl.plot_SymH(
        ax1, 
        ds['sym'], 
        ylim = ylim,  
        step = step,  
        kp = False
        )
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    dates = np.unique(ds.index.date)
    
    delta = dt.timedelta(days = 2)
    start = dates[0] + delta
    
    end = dates[-1] 
    
    ax.set(
        xlim = [start, end]
        )
    
    return [start, end] 

def set_axis(ax):
    
    b.axes_hour_format(
         ax, 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    b.adding_dates_on_the_top(
            ax, 
            fmt = '%d/%m/%y', 
            pad = -2
            )
    
    return None


def check_double_sup(dn):
    delta = dt.timedelta(days = 1)
    df = c.category_and_low_indices()
    
    next_day = dn + delta
    if next_day in df.index:
        return True
    else:
        return False
            
def category(dn):
    df = c.category_and_low_indices()
    return df.loc[dn]['category']

  


def plot_single_case(
        ax, 
        dn, 
        root = 'D:\\', 
        before = 4, 
        after = 4
        ):
    
    dusk = gg.terminator(dn)
    
    ds = c.high_omni(dn.year)
    ds = b.range_dates(ds, dn, before, after)
     
    if category(dn) != 'quiet':
        st = c.find_storm_interval(ds['sym'], dn)
        ylim = [-250, 50] 
        step = 100
    else:
        ylim = [-120, 20]
        step = 40
    
    dns = plot_sym_h(ax, ds, ylim = ylim, step = step)
     
    pl.plot_roti_in_range(
        ax,  
        dns[0], dns[-1], 
        root = root, 
        clear = dn + dt.timedelta(hours = 22)
        )
    
    set_axis(ax)     
    
    double = check_double_sup(dn)
    if category(dn) != 'quiet':
       
        pl.stormtime_spanning(
            ax, st['start'], st['dusk'], y = 2.5)
        
        ax.axvspan(
            st['start'], 
            st['end'], 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'tomato'
            )
        
        if double:
            delta = dt.timedelta(days = 1)
            pl.stormtime_spanning(
                ax, 
                st['start'], 
                st['dusk'] + delta, 
                y = 1.5
                )
    
    pl.evening_interval(ax, dusk, double)
        
    for dn in np.unique(ds.index.date):
        ax.axvline(dn, lw = 1, linestyle = '--')
    
    return None 


    
def plot_multi_examples_of_suppression(dates):
    
    nrows = len(dates)
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharey = True,
        figsize = (16, 3 * nrows), 
        nrows = nrows
        )
    
    for i, dn in enumerate(dates):
         
        plot_single_case(ax[i], dn)
         
        if i < nrows - 1:
            ax[i].set(xticklabels = [])
        
    
    fig.align_ylabels()
    
    ax[-1].set(xlabel = 'Universal time')
    
    b.plot_letters(
        ax, 
        y = 1.04, 
        x = 0., 
        fontsize = 25
        )

    return fig

def main():
    
    #disturbed
    dates = [ 
        dt.datetime(2015, 3, 17),
        dt.datetime(2017, 3, 1),
        dt.datetime(2013, 1, 26),
        dt.datetime(2014, 2, 9),
        # dt.datetime(2013, 9, 24),
        'stormtime'
        ]
    
    #quiets
    # dates = [
    #     # dt.datetime(2013, 9, 18), 
    #     dt.datetime(2014, 9, 9),
    #     dt.datetime(2016, 9, 22),
    #     dt.datetime(2017, 1, 23),
    #     dt.datetime(2019, 3, 13),
    #       'quiettime'
    #     ]

    
    fig = plot_multi_examples_of_suppression(dates[:-1])
    
    plt.show()

    pl.savefig(fig, f'multi_examples_{dates[-1]}')
    
# main() 