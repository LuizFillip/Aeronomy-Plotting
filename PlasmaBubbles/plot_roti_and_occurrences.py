import matplotlib.pyplot as plt
from base import format_time_axes
import datetime as dt
from base import load
import PlasmaBubbles as pb
import numpy as np
import pandas as pd

def plot_roti_and_occurrences():
    
    dn = dt.datetime(2013, 1, 4, 12)
    ds = dt.datetime(2013, 1, 2, 12)

    df = load('2013.txt')
    df = df.loc[(df.index > ds) &
                (df.index < dn)]

    fig, ax = plt.subplots(
        figsize = (12, 6), 
        nrows = 2, 
        sharex= True,
        dpi = 300
        )
    plt.subplots_adjust(hspace = 0.05)
    
    plot_roti(ax[0], df)

    ds = pb.check_occurrence_in_all(df)

    ax[1].plot(ds['same'])

    format_time_axes(ax[1], hour_locator = 4, pad = 60)

    ax[1].set(ylabel = 'EPB occurrence')
    
    dates = np.unique(df.index.date)
    for ax in ax.flat:
        for dn in pd.to_datetime(dates):
            delta = dt.timedelta(hours = 3)
            
            ax.axvline(dn + delta, color = 'red', lw = 2)


def plot_roti(ax, df):
    ax.plot(df['ceeu'])
    
   
        
    ax.set(ylabel = 'ROTI (TECU/min)', 
           ylim = [0, 6],
           xlim = [df.index[0], df.index[-1]])
    
    ax.axhline(1, color = 'magenta', lw = 2)
    

# plot_roti_and_occurrences()