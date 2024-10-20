import pandas as pd
import datetime as dt
import GNSS as gs 
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import numpy as np 

def shade(
        ax, 
        df: pd.DataFrame, 
        start: dt.datetime, 
        label: bool = True
        ):
    
    end = start + dt.timedelta(minutes = 10)
    
    ax.axvspan(start, end, alpha = 0.3, color = "gray")
    
    

def plot_demo_data_reduced(
        df, 
        fontsize = 20
        ):
    
    b.config_labels()
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300,
        sharex = True,
        sharey = True,
        figsize = (10, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    args = dict(marker = 'o', 
                markersize = 1,
                linestyle = 'none', 
                color = 'k'
                )
    
    
    ax[0].plot(df['roti'], **args)
    
    df = df.loc[
        (df['el'] > 30) & (df['roti'] < 5)]
    
    ax[0].set(
        title = 'All PRNs (GPS and GLONASS) and stations'
        )
    
    
    ax[1].plot(df['roti'], **args)
    
    df = pb.remove_bad_stations(
            df, 
            threshold = 0.2 
            )
    ax[2].plot(df['roti'], **args)
    
    ax[2].set(ylim = [0, 3], )
        
    b.format_time_axes(ax[2], 
                       hour_locator = 4)
    
    c = b.chars()
    
    names = ['Raw data', 
             '$el > 30^\circ$ and ROTI$ < 5$ TECU/min', 
             'Removing bad receivers']
    
    for i, ax in enumerate(ax.flat):
        name = names[i]
        ax.text(0.01, 0.82, f'({c[i]}) {name}', 
                transform = ax.transAxes)
    
    fig.text(
        0.06, 0.35, "ROTI (TECU/min)",
        rotation = "vertical", 
        fontsize = fontsize)
    
# year = 2013
# dn = dt.datetime(year, 10, 3, 12)

# ds = pb.concat_files(dn)

# ds = b.sel_times(ds, )


def plot_bad_receiver_example(
        ds, 
        station = 'brft'
        ):
    
    fig, ax = plt.subplots(
        figsize = (8, 4), 
        dpi = 300
        )
    
    args = dict(marker = 'o', 
                markersize = 1,
                linestyle = 'none', 
                color = 'k'
                )
    
    df = ds.loc[ds['sts'] == station]
    
    ax.plot(df['roti'], **args)
    
    ax.set(title = station.upper(), 
           ylabel = 'ROTI (TECU/min)', 
           ylim = [0, 10],
           xlim = [df.index[0], 
                   df.index[-1]])
    
    b.format_time_axes(
        ax, 
        hour_locator = 2
        )
    
    ax.axhline(1, lw = 2, color = 'r')
    
    
# plot_bad_receiver_example(ds)


# plot_demo_data_reduced(
#         ds, 
#         fontsize = 20
#         )