import matplotlib.pyplot as plt
import seaborn as sns  
import base as b
import pandas as pd
import datetime as dt

def heat_map_for_events(
        ds, 
        values = 'roti',
        freq = '1h'
        ):
    
    df = pd.pivot_table(
        ds, 
        values = values,
        index = 'long', 
        columns = ds.index
        )
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
        vmax=1,
        vmin=0,
        cbar_kws={
        'pad': .02, 
        
        'ticks': [0, 1],
    },
        xticklabels = xticks_spacing)
    
    ax.set(ylabel = 'Longitudes', xlabel = 'Time (UT)')
    
    value_to_int = {j:i for i, j in
                    enumerate(['non EPB', 'EPB'])}

    n = len(value_to_int)     
    
    colorbar = ax.collections[0].colorbar 
    r = colorbar.vmax - colorbar.vmin 
    colorbar.set_ticks([colorbar.vmin + 
                        r * i for i in range(n)])
    colorbar.set_ticklabels(list(value_to_int.keys()))   


infile = 'D:\\database\\epbs\\2021\\01.txt'


ds = b.load(infile)

 
def get_date_range(ds):
    delta = dt.timedelta(hours = 20)
    s = pd.to_datetime(ds.index[0].date()) + delta 
    e = ds.index[-1].date() + delta 
    
    return pd.date_range(s, e, freq = '1D')


dn = get_date_range(ds)[0]

df = b.sel_times(ds, dn)


# heat_map_for_events(
#         df, 
#         values = 'event'
#         )

df