import pandas as pd
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
from plotConfig import *
from utils import annual_terminators
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def colorbar_setting(img, ax, ticks = np.arange(0, 6, 1)):
    
    """Color bar settings"""
    axins = inset_axes(
                ax,
                width = "3%",  
                height = "100%",  
                loc = "lower left",
                bbox_to_anchor = (1.05, 0., 1, 1),
                bbox_transform = ax.transAxes,
                borderpad = 0,
            )
    
    cb = plt.colorbar(img, cax = axins, ticks = ticks)
    
    cb.set_label(r'ROTI (TECU/min)')
    
def read_data(infile, resolution = "10min"):
    
    """Load data and resample with a pivot"""
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    df["date"] = df.index
    
    df = df.groupby(pd.Grouper(key = "date", 
                               freq = resolution)).mean()
    df["time"] = df.index.time
    df["time"] = df["time"].apply(lambda x: x.hour + x.minute/60)
    df["date1"] = df.index.date
    
    return pd.pivot_table(df, columns = "date1", 
                          index = "time", values = "roti" )

def plotAnnualVariationROTI(infile = "database/maximus/2014.txt"):
    
    df = read_data(infile, resolution = "10min")
    
    fig, ax = plt.subplots(figsize = (20, 8))
    
    X, Y = np.meshgrid(df.columns, df.index)
    Z = df.values
    img = ax.pcolormesh(X, Y, Z, 
                        vmin = 0, 
                        vmax = 5, 
                        cmap = "Blues") 
    
    colorbar_setting(img, ax)
    ax.set(yticks = np.arange(0, 26, 2), 
           ylabel = "Hora (UT)", 
           xlabel = "Meses")
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    

    
    ax.tick_params(axis = 'x', labelrotation = 0, pad = 10)
    
    plt.show()
    
    return fig
    
fig = plotAnnualVariationROTI(infile = "database/maximus/2014.txt")
    
fig.savefig(path_tex("results") + "\\AnnualContourROTI.png")
    
