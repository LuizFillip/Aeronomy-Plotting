import base as b 
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import plotting as pl 

def plot_SymH(ax, ds, ylim = [-200, 50]):
    
    ax.plot(ds['sym/h'])
   
    ax.set(
        xlim = [ds.index[0], ds.index[-1]], 
        ylim = [ylim[0], ylim[-1]],
        yticks = np.arange(ylim[0], ylim[-1] - 30, 100),
        ylabel = "SYM-H (nT)"
        )
    
    ax.axhline(0, lw = 0.5, color = 'k', linestyle = '-')
    
    return None 

def plot_Aurora(ax, ds):
    ax.plot(ds['ae'])
    ax.set(
        yticks = np.arange(0, 3000, 1000),
        ylabel = 'AE (nT)'
        )
    return None


def plot_solar_speed(ax, ds):
    ds = ds.loc[ds['speed'] < 600]
    ax.plot(ds['speed'])
    ax.set(
        ylim = [300, 600],
        ylabel = '$V_{sw}$ (km/s)'
        )
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
        name = 'Sudden storm commencement'
    else:
        name = 'Ínicio subito de tempestade'
        
    
    plt.subplots_adjust(hspace = 0.05)
    
    plot_solar_speed(ax[0], ds)
    
    plot_SymH(ax[1], ds)
    
    pl.plot_magnetic_fields(ax[2], ds)
    
    plot_Aurora(ax[3], ds)
    
    
    pl.plot_kp(ax[4], dn, days = 2)
    
    
    b.format_time_axes(
        ax[-1],
        hour_locator = 12, 
        pad = 80, 
        format_date = '%d/%m/%y', 
        translate = translate
        )
    
    
    for a in ax.flat:
        
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
    
    ax[0].text(
        ssc, 610, 
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
        
    return fig 


def main():
    
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    infile = 'database/indices/omni_high/2015'
    df = b.load(infile)

    df = df.loc[df['by'] < 1000]

    dn = dt.datetime(2015, 12, 21)


    ds = b.range_dates(df, dn, days = 2)


    fig = plot_high_resolution(ds, dn, translate=True)
    
    FigureName = dn.strftime('%Y%m%d_GeoIndices')
    
    fig.savefig(
           path_to_save + FigureName,
          dpi = 400)
    
    
main()