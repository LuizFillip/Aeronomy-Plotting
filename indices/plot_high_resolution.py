import base as b 
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl 
 

    
def plot_high_resolution(
        ds, dn, 
        translate = False
       ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 10), 
        nrows = 4, 
        sharex = True
        )
     
    plt.subplots_adjust(hspace = 0.05)
    
    pl.plot_solar_speed(ax[0], ds, vmax = 500, step = 50)
    
    pl.plot_SymH(
        ax[1], 
        ds,
        ylim = [-50, 10],
        step = 20)
    
    pl.plot_magnetic_fields(
        ax[2], 
        ds, 
        ylim = 10, 
        step = 10, 
        by = True
        )
    
    pl.plot_auroral(
        ax[3], ds, vmax = 600, step = 100)
     
    
   
 
    fig.align_ylabels()
    
    b.axes_hour_format(
         ax[-1], 
         locator = 6, 
         tz = "UTC"
         )
    
    ax[-1].set(xlabel =  'Universal time')
    
    b.adding_dates_on_the_top( ax[0])
    return fig 


def main():
    
    import core as c 
    
    dn = dt.datetime(2019, 10, 10)
    
    df = c.high_omni(dn.year)

    ds = b.range_dates(df, dn)
     
    fig = plot_high_resolution(ds, dn)
    
   
    
main()