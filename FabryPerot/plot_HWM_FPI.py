import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base as s 
from FabryPerot import load_FPI


def plot_component(
        ax, 
        res, 
        coord = "zon", 
        year = 2013, 
        Type = "observado"
        ):
    
    if coord == "zon": 
        label = "zonal"
        vmin, vmax, step = -100, 150, 50
    else:
        label = "meridional"
        vmin, vmax, step = -100, 100, 50
        
    res["time2"] = s.time2float(res.index)

    
    df = pd.pivot_table(res, 
                        values = coord, 
                        columns = res.index.date, 
                        index = "time2")
    
    df = df.interpolate()
    
    X, Y = np.meshgrid(df.columns, df.index)
    Z = df.values
    
    img = ax.pcolormesh(
        X, Y, Z,  
        vmax = vmax, 
        vmin = vmin, 
        cmap = "jet"
        ) 
       
    s.colorbar_setting(
        img, ax, 
        ticks = np.arange(vmin, 
                          vmax + step, 
                          step), 
        label = "Velocidade (m/s)"
        )
    
    ax.set(
        title = f"Vento {label}",
        ylabel = "Hora (UT)", 
        xlabel = "Meses", 
        yticks = np.arange(20, 34, 2),
        ylim = [20, 32]
           )
    
    ax.text(0.01, 1.01, f"{Type}", 
            transform = ax.transAxes) 
    
    s.format_axes_date(ax, interval = 2)
    
    return ax

def plot_dir(ax, col, HWM, FPI, coord = "zon"):

     ax1 =  plot_component(
         ax[0, col], HWM, coord = coord,
                Type = "HWM-14")
     
     ax1.set(xlabel = "")
     ax2 =  plot_component(
         ax[1, col], FPI, coord = coord, Type = "FPI (Cariri)"
         )
     
     ax2.set(title = "")
     return ax1, ax2


def plot_climatology_HWM_FPI():

    fig, ax = plt.subplots(
        figsize = (14, 6), 
        nrows = 2, 
        ncols = 2,
        sharey = True,
        sharex = True, 
        dpi = 300
        )
    s.config_labels()
    plt.subplots_adjust(hspace = 0.15, wspace=0.25)
         
    HWM = load().HWM(infile = "database/HWM/car_250_2013.txt") 
    
    FPI = load_FPI()
    
    year = FPI.index[0].year

    plot_dir(ax, 0, HWM, FPI, coord = "zon")
    ax1, ax2 = plot_dir(ax, 1, HWM, FPI, coord = "mer")
    
    ax1.set(ylabel = "")
    ax2.set(ylabel = "")
    
    fig.suptitle(year, y = 0.98)
    return fig
    
# save_plot(plot_climatology_HWM_FPI)