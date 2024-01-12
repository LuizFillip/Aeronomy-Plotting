import matplotlib.pyplot as plt
import numpy as np
from models import neutral_iono_parameters
import datetime as dt


def plot_collision_freq(
        ax, 
        nu, 
        alts, 
        step = 50
        ):
    
    name = "Frequências de colisão"
    units = "$s^{-1}$"
    
    if nu.name == "nui":
        symbol = "$\\nu_{in}$"
    else:
        symbol = "$\\nu_{en}$"
        
    ax.plot(nu, alts, lw = 1, label = symbol)
    
    ax.legend()
    
    ax.set(
        xscale = "log", 
        yticks = np.arange(
            min(alts), 
            max(alts) + step, 
            step),
        ylim = [min(alts), max(alts)],
        xlabel = f"{name} ({units})",
        ylabel = "Altitude (km)"
        )
    return ax

def quick_view():
    
    fig, ax = plt.subplots(
        dpi = 300
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    dn  = dt.datetime(2013, 1, 1)
    df = neutral_iono_parameters(
        dn  = dn, 
        hmin = 100
        )
    
    plot_collision_freq(
            ax, 
            df["nui"], 
            df.index)
    
    plot_collision_freq(
            ax, 
            df["nue"], 
            df.index)
   
    
    ax.set(ylabel = "")
    fig.suptitle("São Luis - " + dn.strftime("%d/%m/%Y"))
    plt.show()
    
    return fig

quick_view()