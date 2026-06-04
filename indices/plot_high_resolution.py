import base as b 
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl 
 

    
def plot_high_resolution(
        ds,   
        translate = False
       ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 12), 
        nrows = 4, 
        sharex = True
        )
     
    plt.subplots_adjust(hspace = 0.05)
    
    pl.plot_solar_speed(
        ax[0], ds,
        vmax = 900, 
        step = 300
        )
    
    pl.plot_SymH(
        ax[1], 
        ds,
        ylim = [-40, 50],
        step = 30
        )
    
    pl.plot_magnetic_fields(
        ax[2], 
        ds, 
        ylim = 20, 
        step = 10, 
        by = False
        )
    
    pl.plot_auroral(
        ax[3], ds, 
        vmax = 1500, step = 300)
     
    
    # ax[-1].plot(ds['field'])
 
    fig.align_ylabels()
    
    # b.axes_hour_format(
    #      ax[-1], 
    #      locator = 24, 
    #      tz = "UTC"
    #      )
    
    # ax[-1].set(xlabel =  'Universal time')
    
    # b.adding_dates_on_the_top( ax[0])
    
    b.format_days_axes(ax[-1])
    
    return fig 


def main():
    
    import core as c  
    
    

  
    start = dt.datetime(2016, 12, 25)
    end = dt.datetime(2017, 1, 9)
    
    df = c.high_omni(start.year)
     
    df = b.sel_dates(df, start, end)
     
    fig = plot_high_resolution(df)
    

   
    
main()