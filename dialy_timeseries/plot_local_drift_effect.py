import settings as s
import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators, load_by_alt_time
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import numpy as np
import digisonde as dg





def plot_gamma(ax, df, alt):

    df = df[df["alt"] == alt]
    dn = df.index[0].date()
    
    vz = dg.add_vzp()
    vzp = vz[vz.index == dn]["vzp"].item()
    
    gamma = df["L"] * ((9.81 / df["nui"]))  - df["R"] #-
    
    ax.plot(gamma*1e4, label = f"{alt} km")
    
    vzp = 0
    
    ax.axhline(0, linestyle = "--")
    ax.text(0.65, 0.1, f'Vzp = {vzp} m/s', 
            transform = ax.transAxes)
    
    ax.legend(
        bbox_to_anchor = (.5, 1.5), 
        ncol = 3, 
        loc = "upper center", 
        title = "Altitudes de $\gamma_{RT}$"
        )
    




def plot_local_drift_effect(df, dn):

    fig, ax = plt.subplots(
                figsize = (10, 7),
                sharex = True,
                nrows = 2,
                dpi = 300
                )
    
    plt.subplots_adjust(hspace = 0.1)
    lbs = rt.EquationsRT()
    
        
    for alt in [250, 300, 350]:
        plot_gamma(ax[0], df, alt)
    
    
    ax[0].set(title = lbs.gravity(rc = True),
              ylabel = lbs.label,
              ylim = [-60, 60])
    plot_roti(
        ax[1], 
        df, 
        hour_locator = 1,
        station = "salu"
        )
    
    name = ["", "Salu"]
    for i, ax in enumerate(ax.flat):
        plot_terminators(ax, df)
        
        letter = s.chars()[i]
        ax.text(0.03, 0.82, f"({letter}) {name[i]}", 
                transform = ax.transAxes)
    
    return fig

infile = "database/RayleighTaylor/parameters_car.txt"

dn = dt.datetime(2013, 3, 16, 20)

for dn in [dt.datetime(2013, 3, 16, 20), 
           dt.datetime(2013, 3, 17, 20), 
           dt.datetime(2013, 3, 18, 20)]:
    df = load_by_alt_time(infile, dn)
    FigureName = f"local_gravity_{dn.strftime('%Y%m%d')}.png"
    fig = plot_local_drift_effect(df, dn)
    fig.savefig("RayleighTaylor/figures/" + FigureName, dpi = 300)