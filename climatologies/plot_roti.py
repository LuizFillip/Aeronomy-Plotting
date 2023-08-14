import pandas as pd
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
from base import time2float, colorbar_setting, load


def dataset(
        infile, 
        freq = "5min", 
        col = 'ceeu'
        ):
    
    """Load data and resample with a pivot"""
    
    df = load(infile)
    
    df["date"] = df.index
    
    df = df.groupby(pd.Grouper(
        key = "date", 
        freq = freq)
        ).mean()
    df["time"] = time2float(
        df.index.time, 
        sum24_from = 12)
    
    df["date1"] = df.index.date
    
    return pd.pivot_table(
        df, 
        columns = "date1", 
        index = "time", values = col)

def plot_roti(df):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 4)
        )
    
    X, Y = np.meshgrid(df.columns, df.index)
    Z = df.values
    img = ax.pcolormesh(
        X, Y, Z, 
        vmin = 0, 
        vmax = 5, 
        cmap = 'rainbow'
        ) 
    ticks = np.arange(0, 6, 1)
    colorbar_setting(img, ax, ticks = ticks)
    
    ax.set(yticks = np.arange(12, 36, 2), 
           ylabel = "Hora (UT)", 
           xlabel = "Meses")
    
    ax.xaxis.set_major_formatter(
        dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(
        dates.MonthLocator(interval = 1))
        
    return fig


infile = 'database/EPBs/2014.txt'
df = dataset(infile, col = 'alar')
fig = plot_roti(df)
    

# load(infile).sort_index()
