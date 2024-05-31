import matplotlib.pyplot as plt
import datetime as dt
import base as b
# from GEO import sun_terminator 
import pandas as pd
import digisonde as dg 
import numpy as np 


pd.options.mode.chained_assignment = None 
b.config_labels()

def get_maximum_row(ts, dn, N = 5):
    
    ts = ts[['vz', 'evz']]
    
    ts['max'] = ts['vz'].max()
    ts['filt'] = b.running(ts['vz'], N)
    
    ds = dg.sel_between_terminators(ts, dn)
    
    if len(ds) == 0:
        ds = ts.copy()
        
    ds = ds.sort_values(
        'vz',  
        ascending = False
        ).round(3)
    

    return ds.iloc[0, :].to_frame().T 

def plot_vertical_component_drift(ts, dn, ds = None, N = 5):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True, 
        figsize = (10, 4)
        )
    
    
    args = dict(
        marker = "s", 
        linestyle = "none", 
        markersize = 5, 
        color = "k", 
        capsize = 3
        )
    
           
    avg = b.running(ts['vz'], N)
    std = ts['vz'].std()
    
    ax.plot(
        ts.index, 
        avg, 
        lw = 2,
        color = 'r'
        )
    
    ax.errorbar(
        ts.index, 
        ts['vz'], 
        yerr = ts['evz'], 
        **args
        )

    ax.fill_between(ts.index, 
                    avg + std, 
                    avg - std, 
                    alpha = 0.2
                    )
    

        
    ax.axhline(0, lw = 2, linestyle = '--')
    
    b.format_time_axes(ax)
    
    
    
    ax.set(ylim = [-45, 90], 
           xlim = [ts.index[0], ts.index[-1]], 
           yticks = np.arange(-45, 90, 15),
           ylabel = "Velocity (m/s)", 
          
           )
    
    if ds is not None:
        
        raw = ds['vz'].item()
        filt = ds['filt'].item()
        ax.set( title = f'Raw = {raw} m/s, Filter = {filt} m/s')
    
    return fig
    
    




def single_plot():
    
    dn = dt.datetime(2015, 12, 20, 19)
    
    infile = 'digisonde/data/drift/data/saa/'
    
    df = b.load(infile + f'{dn.year}_drift.txt')

    ts = b.sel_times(df, dn, hours = 15)
    
    ts = ts.loc[~(ts['evz'] > 10)]
    
    ds = get_maximum_row(ts, dn)
        
    plot_vertical_component_drift(
        ts, dn, ds, N = 5)
    
    plt.show()


# single_plot()