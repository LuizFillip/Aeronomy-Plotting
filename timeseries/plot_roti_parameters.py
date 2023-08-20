import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from GNSS import paths
from base import load



station = "salu"
prn = "G10"



def plot_roti_parameters(path):
    
    fig, ax = plt.subplots(figsize = (10, 8), 
                           nrows = 3, 
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0.05)
    args = dict(color = "k", lw = 1.5)
    
    path = paths(2013, 1)
    
    ds = load(path.fn_roti)
        
    ax[0].plot(ds["el"], **args)
    ax[1].plot(ds["roti"], **args)
        
    df = load(path.fn_tec('station'))
    
    ax[0].set(ylabel = "Elevação (°)")
    
    ax[1].set(ylabel = "STEC (TECU)")
        
    ax[2].plot(df, **args)
    
    ax[2].set(ylim = [0, 5], 
              yticks = np.arange(0, 6, 1),   
              xlabel = "Hora universal",
              ylabel = "ROTI")
    

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
    ds = load(path.fn_tec('apma'))
    
    for prn in ds.columns:
        fig, ax = plt.subplots()
        ds[prn].dropna().plot(ax = ax)
        
        ax.set(title = prn)
        
        
        
path = paths(2022, 3)
ds = load(path.fn_roti)

station = 'amte'
prn = 'R21'

df = ds[(ds['sts'] ==  station)] 

for prn in ds['prn'].unique():
    fig, ax = plt.subplots()
    
    ds.loc[(ds['prn'] == prn)]['roti'].plot(ax = ax)
    ax.set(title = prn, ylim = [0, 6])


