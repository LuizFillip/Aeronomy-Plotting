import matplotlib.pyplot as plt
from base import format_time_axes
import datetime as dt
from base import load


def plot_roti_and_occurrences(df, date):
    
    fig, ax = plt.subplots(
        figsize = (8, 6), 
        dpi = 300,
        sharex = True, 
        nrows = 2
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    sel_df = df.loc[df['sts'] == 'salu', 'roti']
    
    ax[0].axhline(1, lw = 2, color = 'r')
    
    
    sel_df.plot(ax = ax[0])
    
    start = dt.datetime(2013, 1, 2, 23, 0)
    
    end = start + dt.timedelta(minutes = 10)
    
    ax[0].axvspan(start, end, alpha = 0.3, color = "gray")
    
    
    format_time_axes(ax[1])
    for ax in ax.flat:
        
        ax.axvline(
            date.date() + dt.timedelta(days = 1), 
            color = 'blue',
            lw = 2
            )

import numpy as np
import pandas as pd

dn = dt.datetime(2013, 1, 4, 12)
ds = dt.datetime(2013, 1, 2, 12)

df = load('2013.txt')
df = df.loc[(df.index > ds) &
            (df.index < dn)]

fig, ax = plt.subplots(
    figsize = (12, 8), 
    nrows = 2, 
    sharex= True,
    dpi = 300
    )
plt.subplots_adjust(hspace=0.1)
def plot_roti(ax, df):
    ax.plot(df['ceeu'])
    
    
    dates = np.unique(df.index.date)
    
    for dn in pd.to_datetime(dates):
        delta = dt.timedelta(hours = 3)
        
        ax.axvline(dn + delta, color = 'red', lw = 2)
        
    ax.set(ylabel = 'ROTI (TECU/min)', 
           xlim = [df.index[0], df.index[-1]])
    
    ax.axhline(1, color = 'magenta', lw = 2)
    

plot_roti(ax[0], df)
import PlasmaBubbles as pb

ds = pb.check_occurrence_in_all(df)

ax[1].plot(ds['same'])

format_time_axes(ax[1], hour_locator = 4)

ax[1].set(ylabel = 'EPB occurrence')