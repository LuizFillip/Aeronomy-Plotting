import base as b 
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import plotting as pl 
import magnet as mg

def plot_kp_hourly(ax1, ds):
    PATH_INDEX =  'database/indices/omni_hourly.txt'

    df = b.load(PATH_INDEX)
    df = df.loc[
        (df.index > ds.index[0]) &
        (df.index < ds.index[-1])
        ]
    
    ax1.axhline(9, lw = 1, linestyle = ':')
    ax1.bar(
        df.index, df['kp'], 
        width = 0.04, 
        alpha = 0.6, 
        color = 'gray', 
        edgecolor = 'k'
        )
    
    ax1.set(
        ylabel = 'Kp', 
        yticks = np.arange(0, 12, 3),
        ylim = [0, 18],
        )
    
    return None 
      
def plot_SymH(ax, ds, ylim = [-300, 50]):
    
    ax.plot(ds['sym/h'], lw = 2)
   
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [ylim[0], ylim[-1]],
        yticks = np.arange(-250, ylim[-1], 100),
        ylabel = "SYM-H (nT)"
        )
    
    ax.axhline(0, lw = 0.5, color = 'k', linestyle = '-')
    
    ax1 = ax.twinx()
 
    plot_kp_hourly(ax1, ds)
    
    return None 

def plot_auroral(ax, ds, vmax = 3000):
    ax.plot(ds['ae'], lw = 1.5)
    ax.set(
        ylim = [0, vmax],
        yticks = np.arange(0, vmax + 500, 500),
        ylabel = 'AE (nT)'
        )
    return None


def plot_solar_speed(ax, ds, vmax = 800):
    ds = ds.loc[ds['speed'] < 600]
    ax.plot(ds['speed'], lw = 1.5)
    ax.set(
        ylim = [200, vmax],
        yticks = np.arange(200, vmax + 100, 100),
        ylabel = '$V_{sw}$ (km/s)'
        )
    return None


def plot_electric_field(ax, ds):
    ds = ds.loc[ds['electric'] < 100]
    ax.plot(ds['electric'])
    ax.set(ylabel = 'Ey (mV/m)')
    return None 
 
    

    
def plot_high_resolution(
        ds, dn, 
        translate = False
       ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 5, 
        sharex = True
        )
    
    if translate:
        name = 'SSC'
        xlabel = 'Universal time'
    else:
        name = 'IS'
        xlabel = 'Hora universal'
    
    plt.subplots_adjust(hspace = 0.05)
    
    plot_solar_speed(ax[0], ds)
    
    plot_SymH(ax[1], ds)
    
    pl.plot_magnetic_fields(ax[2], ds)
    
    plot_auroral(ax[3], ds)
    
    pl.plot_electrojet(ax[-1])

    
    dates = (np.unique(ds.index.date))
        
    
    
    for a in ax.flat:
        
        for dn in dates:
            a.axvline(dn, lw = 1, linestyle = '--')
        
        start = dt.datetime(2015, 12, 20, 21, 0)
        
        a.axvspan(
             start, 
             start + dt.timedelta(hours = 12), 
             ymin = 0, 
             ymax = 1,
             alpha = 0.2, 
             color = 'gray'
             )
        
        ssc = dt.datetime(2015, 12, 19, 16, 20)
        
        a.axvline(
            ssc, 
            color = 'red', 
            lw = 3, 
            linestyle = '--'
            )
    delta = dt.timedelta(hours = 1)
    ax[0].text(
        ssc + delta,250, 
        name, 
        color = 'red',
        transform = ax[0].transData
        )
    
    b.plot_letters(
        ax, 
        y = 0.8, 
        x = 0.02, 
        num2white = None
        )
    
    fig.align_ylabels()
    
    b.axes_hour_format(
         ax[-1], 
         hour_locator = 6, 
         tz = "UTC"
         )
    
    ax[-1].set(xlabel = xlabel)
    
    b.adding_dates_on_the_top(
            ax[0], 
            # start = '2015-12-19', 
            # end = '2015-12-23'
            )
    return fig 


def main():
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    infile = 'database/indices/omni_high/20151'
    df = b.load(infile)
    
    df = df.loc[df['by'] < 1000]

    dn = dt.datetime(2015, 12, 21)

    ds = b.range_dates(df, dn, days = 2)
    
    translate = True
    
    fig = plot_high_resolution(ds, dn, translate)
    
    if translate:
        t= 'en'
    else:
        t = 'pt'
    FigureName = dn.strftime(f'%Y%m%d_GeoIndices_{t}')
    
    # fig.savefig(
    #       path_to_save + FigureName,
    #       dpi = 400
    #       )
    
    # 
