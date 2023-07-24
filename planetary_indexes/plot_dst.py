import numpy as np
import matplotlib.pyplot as plt
import settings as s
import datetime as dt
import pandas as pd


def plot_disturbance_index(ax,
       infile
        ):
    
    """Plotting Disturbance Storm and Kp indexes"""
    
    df = pd.read_csv(infile, index_col=0)
    df.index = pd.to_datetime(df.index)

    df = df[(df.index > dt.datetime(2013, 3, 10)) &
            (df.index < dt.datetime(2013, 3, 20))]


  

    ax.plot(df, lw= 1)
    ax.axhline(0, linestyle = "--")
    s.format_time_axes(ax)

    ax.set(ylabel = "Dst (nT)", 
           xlim = [df.index[0],  df.index[-1]], 
           ylim = [-200, 50], 
           yticks = np.arange(-200, 100, 50))


    s.config_labels(fontsize = 20)
    plt.show()
    
    return ax

def main():
    infile = "database/PlanetaryIndices/kyoto2000.txt"
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 6)
        )
    fig = plot_disturbance_index(ax, infile)
    
    #fig.savefig("PlanetaryIndices/figures/dst_index.png", dpi = 30
    
# main()