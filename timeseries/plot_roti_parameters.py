import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from GNSS import paths
import base as b
import datetime as dt

b.config_labels()

def plot_roti_parameters(
        path, 
        station = 'amte', 
        prn = 'E18'):
    
    ds = b.load(path.fn_roti)

    ds = ds[(ds['sts'] ==  station)] 

    fig, ax = plt.subplots(
        figsize = (10, 6),
        nrows = 2,
        sharex = True
        )

    roti  = ds.loc[(ds['prn'] == prn), 
           'roti'].dropna()
    ax[0].scatter(roti.index, roti, s = 1)

    ax[0].set(title = prn, 
              ylim = [0, 6], 
              ylabel = "ROTI")

    ax[0].axhline(1, color = 'r')

    tec = b.load(path.fn_tec(station))

    ax[1].plot(tec[prn].dropna())
    ax[1].set(ylabel = "STEC (TECU)")
    b.format_time_axes(ax[1])
    

    

# plot_roti_parameters(station, prn, tec)



def run_roti(ds):
    
    for station in ds['sts'].unique():
        fig, ax = plt.subplots()
        sel_sts = ds.loc[ds['sts'] ==  station]
        
        for prn in sel_sts['prn'].unique():
            sel_sts.loc[
                sel_sts['prn'] == prn, 
                        'roti'].plot(ax = ax)
            ax.set(title = station, ylim = [0, 5])
        

def run_tec():
    ds = b.load(path.fn_tec('apma'))
    
    for prn in ds.columns:
        fig, ax = plt.subplots()
        ds[prn].dropna().plot(ax = ax)
        
        ax.set(title = prn)
        

path = paths(2013, 1)
ds = b.load(path.fn_roti)

# run_roti(ds)

# station = 'salu'

# sel_sts = ds.loc[ds['sts'] ==  station]

# for prn in sel_sts['prn'].unique():
#     plot_roti_parameters(
#             path, 
#             station = 'salu', 
#             prn = prn)

# def test_mean(roti):
#     d = roti[roti.index> dt.datetime(2022, 1, 3, 9)]
    
#     d = d.loc[~(d > np.mean(d))]
    
#     plt.scatter(d.index, d)
#     plt.ylim([0, 1])