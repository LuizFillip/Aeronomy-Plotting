import matplotlib.pyplot as plt
from base import format_time_axes
import numpy as np
from base import load
import pandas as pd
import datetime as dt
from base import (
    sel_times,
    config_labels, 
    add_lines_and_letters,
    aware_dn
    )
from GEO import dawn_dusk, delta_timezone
config_labels()


def plot_roti_for_each_longitude(df):
    
    fig, ax = plt.subplots(
        nrows = 5,
        dpi = 300,
        figsize = (10, 10),
        sharex = True, 
        sharey = True
        )

    
    lons = np.arange(-80, -20, 10)[::-1]
    
    dn = df.index[0]
    
    add_lines_and_letters(
            ax, 
            names = lons, 
            y = 0.7
            )
    
    for i, ax in enumerate(ax.flat):
        lon_s, lon_e = lons[i + 1], lons[i]
        
        cond_long = (
            (df['lon'] > lon_s) & 
            (df['lon'] < lon_e)
            )
        
        ds = df.loc[cond_long].sort_index()
        
        ax.axhline(1, color = 'r', lw  = 2)
        ax.plot(ds['roti'])
        
        middle = (lon_s + lon_e) /  2
        middle = lon_e
        dawn, dusk = dawn_dusk(
                dn,  
                lat = 0, 
                lon = middle, 
                twilightAngle = 18
                )
        
        if aware_dn(dusk) < dn:
            dusk += dt.timedelta(days = 1)
        
        utc_midnight = dt.datetime(
            dn.year, dn.month, dn.day + 1
            )
        
        delta_tz = delta_timezone(utc_midnight, middle)
        local_midnight = utc_midnight + delta_tz
        
        
        ax.axvline(local_midnight, color = 'b', lw = 2, 
                   label = f'LT = UT + {delta_tz}')
        ax.axvline(dusk)
        
        ax.legend()
        
        if i == 4:
            format_time_axes(
                ax, 
                hour_locator = 1
                )
            
    
            

def concat():
    p = 'database/GNSS/roti/2014/'
    files = ['001.txt', '002.txt']
    return pd.concat(
        [load(p + f) for f in files])

def main():
    df = concat().sort_index()
    df = df.loc[df['roti'] < 6]
    
    dn = dt.datetime(2014, 1, 1, 20)
    df = sel_times(df, dn)
    
    plot_roti_for_each_longitude(df)
    
    stations = df['sts'].unique()


