import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import settings as s
from FabryPerot.src.core import load_FPI
from common import load
from utils import time2float


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
    
    year = res.index[0].year
    
    res["time2"] = time2float(res.index)

    
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
        title = f"Vento {label} para {year}",
        ylabel = "Hora (UT)", 
        xlabel = "Meses", 
        yticks = np.arange(20, 34, 2),
        ylim = [20, 32]
           )
    
    ax.text(0.01, 1.01, f"{Type}", 
            transform = ax.transAxes) 
    
    s.format_axes_date(ax)
    
    return ax


def plot_climatology_HWM_FPI(coord = "zon"):

    fig, ax = plt.subplots(figsize = (8, 6), 
                           nrows = 2, 
                           sharey = True,
                           sharex = True, 
                           dpi = 300)
    s.config_labels()
    plt.subplots_adjust(hspace = 0.1)
         
    df = load().HWM(infile = "database/HWM/car_250_2013.txt") 
    
    ax1 =  plot_component(ax[0], df, 
               coord = coord, 
               Type = "HWM-14")
    
    df = load_FPI()

    df = df.loc[(df["zon"] > -10) &
                (df["zon"] < 170) 
                ]
        
    ax1.set(xlabel = "")
    ax2 =  plot_component(
        ax[1], df, coord = coord, Type = "FPI (Cariri)"
        )
    
    ax2.set(title = "")
    
    return fig
    

plot_climatology_HWM_FPI()