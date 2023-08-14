from GEO import quick_map
from base import load
import numpy as np
from base import (
    sel_times,
    aware_dn,
    config_labels
    )
import pandas as pd
import datetime as dt

config_labels()

def plot_ipp_and_equator_range(ds):
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
    
    # prns = df['prn'].unique()
    # stations = df['sts'].unique()
    
    # for sts in stations:
    #     for prn in prns:
    #         ds = df.loc[
    #             (df['prn'] == prn) &
    #             (df['sts'] == sts)]
            
    ax.scatter(
        ds['lon'], 
        ds['lat'],
        c = ds['roti'],
        s = 50,
        cmap = 'jet',
        vmin = 0, 
        vmax = 6
        )
        
    for long in np.arange(-80, -20, 10):
        ax.axvline(long)
        




def concat():
    p = 'database/GNSS/roti/2014/'
    files = ['001.txt', '002.txt']
    return pd.concat(
        [load(p + f) for f in files])

df = concat().sort_index()
df = df.loc[df['roti'] < 6]

dn = dt.datetime(2014, 1, 1, 20)
df = sel_times(df, dn)

delta = dt.timedelta(minutes = 9, 
                     seconds = 59)
ds = df.loc[(df.index > dn) & 
            (df.index < dn + delta)]


plot_ipp_and_equator_range(ds)



