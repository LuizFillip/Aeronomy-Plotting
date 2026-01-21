import base as b
import matplotlib.pyplot as plt 
import GEO as gg 
import datetime as dt 
import core as c 

b.sci_format(fontsize = 25)

def save_figs(df):
    from tqdm import tqdm 
    plt.ioff()
    
    path_to_save = 'D:\\img\\storms\\'
    
    for dn, row in tqdm(df.iterrows()):
        
        ds, st = set_data(dn)
        
        fig = plot_storm_intervals(ds, st, dn, row)
        file = dn.strftime('%Y%m%d.PNG')
        
        fig.savefig(path_to_save + file)
        
    plt.clf()   
    plt.close()

def _devtime(end, start):
    return (end - start).total_seconds() / 3600

def stormtime_spanning(ax, start, end, y = -100):
    
    devtime = _devtime(end, start)
    
    time = round(devtime, 2)
        
    middle = end + (start - end) / 2
      
    ax.annotate(
        '', 
        xy = (start, y), 
        xytext = (end, y), 
        arrowprops = dict(arrowstyle='<->')
        )
    time = round(time, 2)
    
    ax.annotate(
        f'{time} hrs',
        xy = (middle, y + 5), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
    
    
    return None   

def reference_sym_hlines(ax):
    
    ax.axhline(0, linestyle = ':')
    
    for ref_line in [0, -30, -50, -100]:
        ax.axhline(
            ref_line, 
            linestyle = '-', 
            color = 'red'
            )
        
    return None 
        
def set_xaxis(ax, ds):
    start, end = ds.index[0], ds.index[-1]
    
    b.axes_hour_format(
         ax, 
         hour_locator = 12, 
         tz = "UTC"
         )
    
    ax.set(
        xlabel = 'Universal time', 
        xlim = [start, end]
        )

    b.adding_dates_on_the_top(
           ax, 
           fmt = '%d/%m'
           )
    
    import pandas as pd
    import numpy as np
    
    dns = pd.to_datetime(np.unique(ds.index.date))
    for dn in dns:
        ax.axvline(dn, lw = 1, linestyle = '--')

    return None 

  
def plot_storm_intervals(ds, st, dn, row):
     
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 8)
        )
    
    ax.plot(ds['sym'])

    dusk = gg.terminator(
        -50, 
        dn, 
        float_fmt = False
        )
    
    ax.axvline(
        dusk, 
        linestyle = '--', 
        color = 'b', 
        lw = 3
        )
    
    stormtime_spanning(
        ax, 
        st['start'], 
        dusk, 
        y = 10
        )
    
    ax.axvspan(
        st['start'], 
        st['end'], 
        ymin = 0, 
        ymax = 1,
        alpha = 0.2, 
        color = 'tomato'
        )
    
    set_xaxis(ax, ds)
    reference_sym_hlines(ax)
    
    s = ds['sym'] 
    vmin = round(s.min())
    
    time = s.idxmin(skipna = True)
    ax.scatter(time, vmin, s = 140, marker = '^')
    delta = dt.timedelta(days = 2)
    xe = time + delta
 
    ax.annotate(
        f'{vmin} nT',
        xy = (time, vmin) , 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        xytext = (xe, vmin - 3), 
        arrowprops = dict(arrowstyle='->'),
        ha = 'center'
        )
    
    ax.set(
        ylim = [vmin - 50, 50],
        ylabel = 'SYM-H (nT)',
        title = dn.strftime('%B, %Y - ') + row
        )
    
    return fig
    

def set_data(dn, backward = 2, forward = 6):
    df = c.high_omni(dn.year)
    
    df = b.range_dates(
        df, 
        dn, 
        b = backward, 
        f = forward
        )
    
    st = c.find_storm_interval(df['sym'])
    
    return df, st

def main():
    dn = dt.datetime(2013, 3, 17)
    dn = dt.datetime(2016, 10, 2)
    dn = dt.datetime(2016, 11, 13)
    dn = dt.datetime(2017,  1, 7)
    dn = dt.datetime(2017,  1, 23)
    dn = dt.datetime(2017,  3, 6)
    dn = dt.datetime(2017,  9, 24)
    dn = dt.datetime(2018,  1, 4)
    
    ds = c.category_and_low_indices()
    
    df, st = set_data(dn, before = 8, after = 2)
    
    row =  ds.loc[dn].category
    
    fig = plot_storm_intervals(df, st, dn, row)


