import matplotlib.pyplot as plt
import numpy as np
import aeronomy as io
import models as m
import datetime as dt
import base as b 

b.config_labels(fontsize = 25)

def plot_local_conductivies(
        ax, 
        nu, 
        alts, 
        step = 50
        ):
    
    name = "$\sigma$"
    units = "mho/m"
    
    if nu.name == "perd":
        symbol = "$\sigma_{P}$"
    elif nu.name == "hall":
        symbol = "$\sigma_{H}$"
    else:
        symbol = "$\sigma_{0}$"
        
    ax.plot(nu, alts,
            lw = 1, label = symbol)
    
    ax.legend(loc = "upper right")
    
    ax.set(
        xscale = "log", 
        yticks = np.arange(
            min(alts), 
            max(alts) + step, 
            step
            ),
        
        ylim = [min(alts), max(alts)],
        xlim = [1e-14, 1e7],
        xlabel = f"{name} ({units})",
        ylabel = "Altitude (km)"
        )
    return ax

def plot_local_ratio_conductivities(df):
    
     fig, ax = plt.subplots(
         dpi = 300, 
         ncols = 2,
         figsize = (8, 8), 
         sharey = True
         )
     
     ax[1].plot(df["hall"] / df["perd"],  df.index)
     
     ax[1].set(
         xlim = [-2, 100], 
         xlabel = "$\sigma_H / \sigma_P$"
               )
     
     plot_local_conductivies(
            ax[0], 
            df["perd"], 
            df.index
            )
    
     plot_local_conductivies(
            ax[0], 
            df["hall"], 
            df.index
            )
    
     ax = plot_local_conductivies(
            ax[0], 
            df["parl"], 
            df.index
            )
     
     return fig
     
dn = dt.datetime(2013, 12, 24, 22)

df = m.altrange_models(**m.kargs(dn, hmin = 80))
   
df = io.conductivity_parameters(df, other_conds = True)

fig = plot_local_ratio_conductivities(df)

