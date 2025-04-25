# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 20:30:36 2025

@author: Luiz
"""

def plot_models(ax, values):
      
    infile = 'plotting/FabryPerot/December2015'
    
    df = b.load(infile)
    
    # print(df.columns)
    
    df["time"] = b.time2float(df.index.time)
    
    ds = pd.pivot_table(
        df, 
        columns = df.index.date, 
        index = "time", 
        values = values
        )
    
    mean = ds.mean(axis = 1)
    
    ax1 = ax.twiny()
    
    ax1.plot(
        mean, 
        lw = 2, 
        color = 'magenta', 
        label = 'Montly average'
        )
    ax1.set(
        xlim = [21, 32], 
        xticklabels = []
        )
    
    # ax1.legend(loc = 'lower left')s