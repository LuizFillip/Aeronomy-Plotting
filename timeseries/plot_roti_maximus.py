import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import settings as s
import pandas as pd
import os

def split_fname(infile):

    _, f = os.path.split(infile)
    
    return f.split("_")[0]



def plot_roti_maximus(
        ax, 
        infile, 
        start, 
        station = "salu", 
        delta_hours = 10, 
        text = True):
    
    """Read files and plotting maximus"""
    
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    if isinstance(delta_hours, int):
        end = start + dt.timedelta(
            hours = delta_hours
            )
        
    elif isinstance(delta_hours, dt.datetime):
        end = delta_hours
    else:
        end = start + delta_hours

    df2 = df.loc[(df.index >= start) & 
                 (df.index <= end), :]
    
    y = df2[station].values
    x = df2.index 
    ax.bar(x, y, width = 0.001, color = "k")
    
    ax.axhline(1, lw = 2, color = "red", label = "1 TECU/min")
    if text:
        ax.text(0.05, 0.8, station.upper(), transform = ax.transAxes)
    ax.set(
        ylim = [0, 3], 
        yticks = np.arange(0, 6, 1),
        ylabel = "ROTI (TECU/min)")
           
    ax.legend(loc = "upper right")
    
    return ax
        

def main():

    fig, ax = plt.subplots(dpi = 300)
    infile = "database/Results/maximus/2013.txt"
    start = dt.datetime(2013, 12, 10, 12)   
    end = dt.datetime(2013, 12, 17, 0)
    ax = plot_roti_maximus(
            ax, 
            infile, 
            start, 
            delta_hours = end, 
            station = "salu"
            )

    s.format_time_axes(ax)
