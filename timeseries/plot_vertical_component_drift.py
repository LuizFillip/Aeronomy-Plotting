import matplotlib.pyplot as plt
import datetime as dt
import base as b
from GEO import sun_terminator 
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
        
    ds = ds.sort_values(
        'vz',  
        ascending = False
        ).round(3)
    

    return ds.iloc[0, :].to_frame().T 

def plot_vertical_component_drift(ts, ds, dn, N = 5):
    
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
    
  
    for lim in [0, 18]:
        end = sun_terminator(
                        dn, 
                        twilight_angle = lim, 
                        site = 'saa'
                        )
        
        ax.axvline(end, lw = 2, linestyle = '--')
        
    ax.axhline(0, lw = 2, linestyle = '--')
    
    b.format_time_axes(ax)
    
    raw = ds['vz'].item()
    filt = ds['filt'].item()
    
    ax.set(ylim = [-45, 90], 
           xlim = [ts.index[0], ts.index[-1]], 
           yticks = np.arange(-45, 90, 15),
           ylabel = "Velocity (m/s)", 
           title = f'Raw = {raw} m/s, Filter = {filt} m/s'
           )
    
    return fig
    
    
    

from tqdm import tqdm 



def run_days(year, root):
    
    infile = 'digisonde/data/drift/data/saa/'

    df = b.load(infile + f'{year}_drift.txt')

    df = df[['vz', 'evz']]

    out = []
    
    for day in tqdm(range(365), desc = str(year)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1, 18) + delta
        
        
        
        try:
            ts = b.sel_times(df, dn, hours = 6)
            
            ts = ts.loc[~(ts['evz'] > 20)]
            
            ds = get_maximum_row(ts, dn)
        
            out.append(ds)
            plt.ioff()
            fig = plot_vertical_component_drift(
                ts, ds, dn, N = 5)
            
            FigureName = dn.strftime('%j.png')
            
            fig.savefig(root + FigureName,
                        pad_inches = 0, 
                        bbox_inches = "tight")
            
            plt.clf()   
            plt.close()
        except:
            continue
        
        
    df1 = pd.concat(out)
    save_in = f'D:\\drift\\{year}.txt'
    df1.to_csv(save_in)

def run_years():
    
    for year in range(2013, 2023):
        
    
        root = f'D:\\img2\\{year}\\'
        
        
        b.make_dir(root)
        
        run_days(year, root)



def single_plot():
    
    year = 2015  
    infile = 'digisonde/data/drift/data/saa/'
    
    df = b.load(infile + f'{year}_drift.txt')
    
    
    dn = dt.datetime(year, 2, 18, 18)
    
    ts = b.sel_times(df, dn, hours = 6)
    
    ts = ts.loc[~(ts['evz'] > 20)]
    
    ds = get_maximum_row(ts, dn)
    
    plot_vertical_component_drift(
        ts, ds, dn, N = 5)



# run_years()
