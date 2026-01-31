import matplotlib.pyplot as plt
import digisonde as dg
import base as b 
import GEO as gg 
import datetime as dt 
sites = ['FZA0M', 'SAA0K', 'BVJ03']

def plot_heights_in_single_day(sites):
    
    fig, ax = plt.subplots(
        nrows = len(sites),
        dpi = 300,
        sharey = True, 
        sharex = True,
        figsize = (16, 10)
        )
    
    
    dn = dt.datetime(2023, 10, 14, 0)
    cols = list(range(1, 6, 1))
    
    start = dt.datetime(2023, 10, 14, 0)
    
    for i, site in enumerate(sites):
    
        file = dg.dn2fn(dn, site)
        
        df = dg.IonoChar(file, cols, sum_from = None)
        
        ax[i].plot(
            df.chars['hF2'], 
            color = 'k', 
            lw = 2
            )
        ds = b.sel_times(df.heights, start)
        
        ax[i].plot(ds)
        
        ax[i].set(
            ylim = [100, 400],
            xlim = [ds.index[0], ds.index[-1]]
            )
        
        s = b.chars()[i]
        name = dg.code_name(site)
        ax[i].text(
            0.02, 0.85, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
    
    ax[0].legend(
        cols, 
        ncol = len(cols), 
        title = 'Frequencies fixed (MHz)',
        bbox_to_anchor = (0.5, 1.5), 
        loc = 'upper center', 
        columnspacing = 0.7
        )
    
    b.format_time_axes(
        ax[-1], 
        hour_locator = 1, 
        pad = 70, 
        translate = True, 
        
        )
    
    ax[0].set(ylabel = 'Heights (km)')
    ax[1].set(ylabel = 'Heights (km)')
    
    plt.subplots_adjust(hspace = 0.1)