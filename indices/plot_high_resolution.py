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
      

    
def plot_high_resolution(
        ds, dn, 
        translate = False
       ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14), 
        nrows = 4, 
        sharex = True
        )
    
    if translate:
        name = 'SSC'
        xlabel = 'Universal time'
    else:
        name = 'IS'
        xlabel = 'Hora universal'
    
    plt.subplots_adjust(hspace = 0.05)
    
    pl.plot_solar_speed(ax[0], ds)
    
    pl.plot_SymH(ax[1], ds)
    
    pl.plot_magnetic_fields(ax[2], ds)
    
    pl.plot_auroral(ax[3], ds)
     
    
   
 
    fig.align_ylabels()
    
    b.axes_hour_format(
         ax[-1], 
         locator = 6, 
         tz = "UTC"
         )
    
    ax[-1].set(xlabel = xlabel)
    
    b.adding_dates_on_the_top(
            ax[0],  
            )
    return fig 


def main():
    
    import core as c 
    
    dn = dt.datetime(2019, 10, 17)
    
    df = c.high_omni(dn.year)

    ds = b.range_dates(df, dn)
     
    
    fig = plot_high_resolution(ds, dn, translate)
    
   
    
main()