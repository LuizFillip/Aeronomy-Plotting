# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 18:39:18 2023

@author: Luiz
"""

def plot_roti_and_occurrences(df, date):
    

    import matplotlib.pyplot as plt
    from base import format_time_axes
    import datetime as dt
    
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