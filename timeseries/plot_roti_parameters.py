import pandas as pd
import matplotlib.pyplot as plt
from GNSS.core import load_tec
import numpy as np
import setup as s
from GNSS.base import join_data
from GNSS.build import paths

def load_roti(infile, station, prn = None):
    
    df = pd.read_csv(infile, index_col = "time")

    df.index = pd.to_datetime(df.index)

    df["lon"] = df["lon"] - 360
    
    if prn is None:
        return df.loc[(df["sts"] == station), ["roti"]]
    else:
        return df.loc[(df["sts"] == station) &
                      (df["prn"] == prn), ["roti"]]


station = "salu"
prn = "G10"
tec = load_tec(f"database/GNSS/tec/2013/001/{station}.txt")


def plot_roti_parameters(station, prn, tec):
    
    fig, ax = plt.subplots(figsize = (10, 8), 
                           nrows = 3, 
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0.05)
    args = dict(color = "k", lw = 1.5)
    
    path = paths(2013, 1)
    
    df1 = join_data(tec, path, prn, station)
    
    stec = df1.loc[df1["el"] > 30, :]
    
    ax[0].plot(stec["el"], **args)
    ax[1].plot(stec["stec"], **args)
    
    dn = df1.index[0].strftime("%d/%m/%Y")
    
    ax[0].set(ylabel = "Elevação (°)", 
              title = f"{dn} - {station.upper()} - {prn}")
    
    ax[1].set(ylabel = "STEC (TECU)")
    
    df = load_roti("database/GNSS/roti/2013/001.txt", station, prn)
    
    ax[2].plot(df, **args)
    
    ax[2].set(ylim = [0, 5], 
              yticks = np.arange(0, 6, 1),   
              xlabel = "Hora universal",
              ylabel = "ROTI")
    
    s.format_axes_date(ax[2], time_scale = "Hour", interval = 1)

plot_roti_parameters(station, prn, tec)
