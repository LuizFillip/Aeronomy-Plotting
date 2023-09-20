from settings import format_time_axes
import matplotlib.pyplot as plt
from labels import Labels
import pandas as pd
import settings as s
import numpy as np


def limits_wind(ds, cols):

    vmin = min([ds[col].min() for col in cols])
    vmax = max([ds[col].max() for col in cols])

    return vmin, vmax


def limits_iono(ds, cols):
    dic = {}
    
    for col in cols:
        dic[col] = (ds[col].min(), ds[col].max())
        
    return dic




def set_figure(
        ncols = 2, 
        nrows = 2, 
        figsize = (8, 10), 
        dpi = 300
        ):
    
    fig, ax = plt.subplots(
        dpi = dpi,
        figsize = figsize,
        ncols = ncols,
        nrows = nrows,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.2, 
        wspace = 0.1
        )
    
    return fig, ax
    
        
      
        


def plot(
        ax, ts, 
        parameter = "zon", 
        cmap = "rainbow"
        ):
    
    pt = pd.pivot_table(ts, values = parameter, 
                        columns = ts.index, 
                        index = "alt").interpolate().bfill()
    
    
    img = ax.contourf(
        pt.columns, pt.index, pt.values, 30, cmap = cmap
       )
    
    vls = pt.values
    ticks = np.linspace(np.min(vls), np.max(vls), 5)
    
    lbs  = Labels().infos[parameter]
    
    if parameter == "ratio":
        label = lbs["symbol"] 
    else:
        label = f"{lbs['symbol']} ({lbs['units']})"
    
    s.colorbar_setting(
            img, ax, ticks, 
            label = label)
    
    ax.set(title = lbs["name"].replace("\n", " "))
    
    
def plot_ionospheric_parameters(ds):
   
    fig, ax = set_figure(
        ncols = 1, 
        nrows = 5, 
        figsize = (12, 12), 
        dpi = 300
        )
    
    cols = ["N", "K", "nui", "R", "ratio"]

    
    for i, ax in enumerate(ax.flat):
        
        plot(ax, ds, parameter = cols[i])
        
        ax.set(xlim = [ds.index[0], ds.index[-1]])
            
        if i == len(cols) - 1:
            format_time_axes(ax)
            
    fig.text(0.05, 0.45, "Altura de Apex (km)", 
             rotation = "vertical")
    
    return fig
    
    

