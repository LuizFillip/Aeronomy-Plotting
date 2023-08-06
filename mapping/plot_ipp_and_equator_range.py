from GEO import quick_map
from base import load
import numpy as np




def plot_ipp_and_equator_range(df):
    lat_lims = dict(
        min = -40, 
        max = 10, 
        stp = 10
        )
    
    lon_lims = dict(
        min = -85, 
        max = -30, 
        stp = 10
        )    
    
    fig, ax = quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (8, 8)
        )
    
    prns = df['prn'].unique()
    stations = df['sts'].unique()
    
    for sts in stations:
        for prn in prns:
            ds = df.loc[
                (df['prn'] == prn) &
                (df['sts'] == sts)]
            
            ax.plot(ds['lon'], ds['lat'], 
                    lw = 1, color = 'k'
                    )
        
    for long in np.arange(-80, -20, 10):
        ax.axvline(long)
        

# # stations = df['sts'].unique()
# # stations

#  = -80
#  = -70 
import matplotlib.pyplot as plt

fig, ax = plt.subplots(
    nrows = 5,
    dpi = 300,
    figsize = (8, 10),
    sharex = True, 
    sharey = True
    )



from base import format_time_axes

p = 'database/GNSS/roti/2014/001.txt'
df = load(p)

df = df.loc[df['roti'] < 6]

lons = np.arange(-80, -20, 10)

for i, ax in enumerate(ax.flat):
    lon_s, lon_e = lons[i], lons[i + 1]
    
    cond_long = (
        (df['lon'] > lon_s) & 
        (df['lon'] < lon_e)
        )
    ds = df.loc[cond_long].sort_index()
    
    
    ax.plot(ds['roti'])
    
    ax1 = ax.twinx()
    ax1.plot(ds.index, 
             np.zeros(len(ds)) + lon_s, 
             color = 'white')
    
    ax1.set(yticks = [lon_s])
    
    if i == 4:
        format_time_axes(
            ax, pad = 60, hour_locator = 3
            )
        
#%%

import pytz
import datetime as dt




from timezonefinder import TimezoneFinder

def obter_fuso_horario(longitude):
   
    tf = TimezoneFinder()
    
    return tf.timezone_at(lng=longitude, lat= 0)

def round_dn(dn):
    return dt.datetime(
        dn.year, 
        dn.month, 
        dn.day, 
        dn.hour, 
        dn.minute
        )
timezone = pytz.timezone(obter_fuso_horario(-40))


local_time = dt.datetime.now(timezone)

universal_time = local_time.astimezone(pytz.utc)

delta = round_dn(universal_time) - round_dn(local_time)


dt.datetime(2014, 1, 1, 3, 0) - delta