import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators, load_by_time
import RayleighTaylor as rt
import datetime as dt
import numpy as np
import digisonde as dg




def plot_gamma(
        ax, df, alt, 
        sign = 1,
        wind = "zon"
        ):

    df = df[df["alt"] == alt]
    dn = df.index[0].date()
    
    vz = dg.add_vzp()
    vzp = vz[vz.index == dn]["vzp"].item()
    
    gamma = df["L"] * ( sign * df[wind] + 
             (9.81 / df["nui"]) + vzp)  - df["R"]
    
    ax.plot(gamma *1e4, label = f"{alt} km")
    
    ax.axhline(0, linestyle = "--")
    ax.text(0.65, 0.1, f'Vzp = {vzp} m/s', 
            transform = ax.transAxes)
    
    if wind == "zon_ef":
        name = "Zonal efetivo"
    
    elif wind == "zon":
        name = "Zonal geográfico"
        
    elif wind == 'mer_ef':
        
        name = 'Meridional efetivo'
    
    else:
        name = "Meridional geográfico"
        
        
   
    ax.text(0.05, 0.1, name, 
            transform = ax.transAxes)
        
    return ax

def plot_local_winds_effects(infile, dn, sign = 1):
   
    df = load_by_time(infile, dn)
    
    fig, ax = plt.subplots(
                figsize = (14, 10),
                sharex = True,
                sharey = "row",
                nrows = 3,
                ncols = 2,
                dpi = 300
                )
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.05
        )
    
    lbs = rt.EquationsRT()
    
    for row, wd in enumerate(["zon", "mer"]):
        
        ax[row, 0].set(ylabel = lbs.label,
                       ylim = [-60, 60])
        
        plot_roti(
            ax[2, row], 
            df, 
            hour_locator = 1,
            station = "salu"
            )
        
        ax[0, row].set(title = lbs.complete(
            sign = sign, rc = True)
            )
        
        for alt in np.arange(250, 400, 50):
            
            plot_gamma(ax[row, 0], df, alt, sign = sign, wind = wd)
            plot_gamma(ax[row, 1], df, alt, sign = sign, wind = wd + "_ef")

    
    ax[0, 0].legend(
        bbox_to_anchor = (.5, 1.1), 
        ncol = 3, 
        loc = "lower left", 
        title = "Altitudes de $\gamma_{RT}$"
        )
    
    
    ax[2, 1].set(ylabel = "")
    for ax in ax.flat:    
        plot_terminators(ax, df)
        

    return fig
def main():
    
    infile = "database/RayleighTaylor/parameters_car.txt"
    
    dn = dt.datetime(2013, 3, 17, 20)

    plot_local_winds_effects(infile, dn, sign = 1)
    
# main()


