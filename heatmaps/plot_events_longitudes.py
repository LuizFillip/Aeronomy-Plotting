import matplotlib.pyplot as plt
import seaborn as sns  
import base as b
import pandas as pd
import datetime as dt
import os 

PATH_EVENT = 'D:\\database\\epbs\\events\\'


def heat_map_for_events(
        df, 
        freq = '1h'
        ):
    
   
    
    # df.columns = pd.to_numeric(df.index)
    
    
    df.columns = pd.DatetimeIndex(
        df.columns).strftime('%H:00')
    
    fig, ax = plt.subplots(
        figsize = (12, 4), 
        dpi = 300
        )
    
    b.config_labels()
    xticks_spacing = (int(pd.Timedelta(freq) /
                          pd.Timedelta('30s')))
    
    sns.heatmap(
        df, 
        ax = ax,
        linecolor='white',
        vmax = 1,
        vmin = 0,
        cbar_kws = {
        'pad': .02, 
        'ticks': [0, 1],
        },
        xticklabels = xticks_spacing
        )
    
    ax.set(ylabel = 'Longitudes', 
            xlabel = 'Universal time')
        
    value_to_int = {j: i for i, j in
                    enumerate(['non EPB', 'EPB'])}

    n = len(value_to_int)     
    
    colorbar = ax.collections[0].colorbar 
    r = colorbar.vmax - colorbar.vmin 
    colorbar.set_ticks([colorbar.vmin + 
                        r * i for i in range(n)])
    colorbar.set_ticklabels(list(value_to_int.keys()))   

    return 


 
def get_date_range(ds):
    delta = dt.timedelta(hours = 20)
    s = pd.to_datetime(ds.index[0].date()) + delta 
    e = ds.index[-1].date() + delta 
    
    return pd.date_range(s, e, freq = '1D')

dn = dt.datetime(2022, 3, 8, 21)


infile = os.path.join(
        PATH_EVENT, 
        f'{dn.year}.txt'
    )
 
ds = b.sel_times(
        b.load(infile), 
        dn, 
        hours = 11
    )


heat_map_for_events(
        ds.T, 
        freq = '1h'
        )


from GEO import terminator 


