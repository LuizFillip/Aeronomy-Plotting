import GEO as gg 
import matplotlib.pyplot as plt
import datetime as dt 
import plotting as pl 
import digisonde as dg 
import base as b 


def plot_compare_quiet_disturbed(ref_lon = -50):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        figsize = (12, 8), 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    site = 'SAA0K'
    
    df = dg.IonoAverage(dn, cols, site, ref = ref)
            
    pl.plot_heights(ax[0], df, parameter = 'hF2')
    
    pl.plot_drift(ax[1], df, vmax = 50)
    
    start = dt.datetime(2013, 3, 17, 20)
    end = dt.datetime(2013, 3, 18, 10)
    
    
    ax[0].set(
        xlim = [start, end],
        ylabel = 'h`F (km)'
        )
    ax[1].set_ylabel(
        'Vertical drift (m/s)'
        )
    
    
    
    ax[0].legend(loc = 'upper center', ncols = 2)
    
    
    
    dusk = gg.terminator(
        -50, 
        ref, 
        float_fmt = False
        )
    
    ax[0].axvline(dusk)
    ax[1].axvline(dusk)
        
    b.format_time_axes(ax[-1], translate = True)
    
dn = dt.datetime(2013, 3, 4, 20)

ref = dt.datetime(2013, 3, 17)


cols = list(range(4, 8, 1))


plot_compare_quiet_disturbed()