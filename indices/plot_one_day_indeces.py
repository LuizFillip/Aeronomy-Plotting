import matplotlib.pyplot as plt
import base as b
import datetime as dt
import numpy as np
import epbs as pb 
import plotting as pl

b.sci_format(fontsize = 25)
PATH = 'database/indices/omni_hourly.txt'


def plot_dst(ax, ds, ylim = [-150, 50], color = 'k'):

    ax.plot(ds['sym'], lw = 2, color = color)
    
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [ylim[0] - 30, ylim[-1]],
        yticks = np.arange(ylim[0], ylim[-1] - 30, 50),
        ylabel = "SYM-H (nT)"
        )
    
    ax.axhline(0, lw = 1, color = 'k', linestyle = '-')
    
    for limit in [-50, -150]:
        ax.axhline(
            limit, 
            lw = 1, 
            color = 'k', 
            linestyle = '--'
            )
    return None 
        

def plot_magnetic_fields(
        ax, 
        ds, 
        ylim = 30, 
        by = False, 
        ax_co = 'purple'
        ):
    
    ax.plot(
        ds['bz'], 
        label = '$B_z$', 
        lw = 2
        )
    
    ax.set(
        ylim = [-ylim, ylim], 
        yticks = np.arange(-30, 40, 15),
        ylabel = '$B_y$ (nT)' #'$Ey$ (mV/m)'
        )
    
    ax.axhline(0, lw = 1, linestyle = '--', color = 'k')
    
    if by:
        ax1 = ax.twinx()
        
        ax1.plot(
            ds['by'], 
            color = ax_co, 
            label = '$B_y$', 
            lw = 2
            )
        
        b.change_axes_color(
                ax1, 
                color = ax_co,
                axis = "y", 
                position = "right"
                )
         
        
    ax.set(
        ylabel = '$B_z$ (nT)',
        yticks = np.arange(-30, 40, 15),
        ylim = [-ylim - 5, ylim + 5]
        )
    
   
    
    return None 


def load_indices(dn):
    
    import core as c
    
    df = pb.longterm_raw_roti(dn, days = 3)

    ds = b.sel_times(df, dn, hours = 12) 
    
    ds =  ds.replace(9999.99, np.nan)
    
    return ds


def plot_epbs(ax, dn, sector = -50):
    
    df = pb.concat_files(
        dn, 
        days = 2, 
        root = 'E:\\', 
        hours = 12, 
        remove_noise = True
        )
    df = pb.filter_region(df, dn.year, sector)
    
    ax.plot(df['roti'])
    
    ax.set(ylim = [0, 2], ylabel = 'ROTI')
    
    return None 

def plot_one_day_indices(dn, days = 2):
    '''
    plot para os indices (a escolher)
    e ROTI - paper da estatistica de tempestade
    '''
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
  
    ds = load_indices()
       
    plot_magnetic_fields(ax[0], ds)
    pl.plot_auroral(ax[1], ds)
    plot_dst(ax[2], ds)
    # plot_epbs(ax[-1], dn)
    
    b.format_time_axes(
        ax[-1], 
        hour_locator = 1, 
        translate = True
        
        )
    
    delta = dt.timedelta(hours = 2)
    
    for a in ax.flat:
         
        dusk, midnight  = pl.plot_references_lines(
                a,
                -50, 
                dn, 
                label_top = None,
                translate = True
                )
        
        a.axvspan(
            dusk - delta,
            dusk + delta, 
            ymin = 0, 
            ymax = 1,
            alpha = 0.2, 
            color = 'gray'
            )
        
    res = ds.loc[
        (ds.index > dusk - delta) &
        (ds.index < dusk + delta)
        ]
    
    # print(res.mean())
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.03, 
        num2white = None
        )
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

def main():
    days = 1

    fig = plot_one_day_indices(dn, days = days)
    
    FigureName = dn.strftime('Indices_%Y%m%d')
    
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'timeseries'),
    #       dpi = 300
    #       )
    
# main()




