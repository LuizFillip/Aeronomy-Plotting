import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import setup as s
from FabryPerot.core import load
from build import paths as p


def plot(
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
    
    df = pd.pivot_table(res, 
                        values = coord, 
                        columns = "day", 
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
        yticks = np.arange(20, 34, 2)
           )
    
    ax.text(0.01, 1.01, f"Vento {Type}", 
            transform = ax.transAxes) 
    
    s.format_axes_date(ax)
    
    return ax


def plot_hwm_fpi_comparation(coord = "zon"):

    fig, ax = plt.subplots(figsize = (8, 6), 
                           nrows = 2, 
                           sharey = True,
                           sharex = True)
    s.config_labels()
    plt.subplots_adjust(hspace = 0.1)
    
    modeled = p("HWM").files[1]
    observed = p("FabryPerot").get_files_in_dir("processed")
        
    df = load(modeled)
    
    ax1 = plot(ax[0], df, 
               coord = coord, 
               Type = "modelado")
    
    df = load(observed)

    df = df.loc[(df["zon"] > -10) &
                (df["zon"] < 170) 
                ]
        
    ax1.set(xlabel = "")
    ax2 = plot(ax[1], df,  
               coord = coord)
    
    ax2.set(title = "")
    
plotCompare_Model_Observation()

 
