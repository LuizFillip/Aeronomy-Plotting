import pandas as pd
import RayleighTaylor as rt
import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators




def sum_gammas(
        df, 
        sign = 1, 
        drift = "vz", 
        wind = "zon",
        recom = False
        ):
    
    res = []
    
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        gamma = rt.all_effects(
                ds, 
                drift = drift, 
                wind = wind,
                sign_wd = sign, 
                recom = recom
                )
        
        res.append(gamma)
    
    return pd.concat(res, axis = 1).sum(axis = 1)



def plot_gamma(
        ax, df, 
        coord = "zonal", 
        rc = False, 
        drift = "vz",
        sign = 1):
    
    winds = [coord[:3], coord[:3] + "_ef"]
    
    labels = ["Geográfico", "Efetivo"]
    
    for i in range(2):
  
        gamma = sum_gammas(
            df, sign = sign, 
            drift = drift, 
            wind = winds[i], 
            recom = rc
            )
        
        ax.plot(gamma * 1e4, 
                label = labels[i])
        
    ax.text(0.05, 0.85, coord.title(), transform = ax.transAxes)
    
    ax.axhline(0, linestyle = "--")
    ax.set(ylim  = [-40, 40], 
           xlim = [df.index[0], df.index[-1]])
    return ax



def plot_total_all_effects(
        ds, drift = "vz", rc = False, station = "salu"
        ):
    
    fig, ax = plt.subplots(
        figsize = (14, 13),
        nrows = 5,
        dpi = 300,
        sharex = True,
        )

    plt.subplots_adjust(hspace = 0.3)


    eq = rt.EquationsFT()

    cols = [("zonal", 1), ("zonal", -1),
            ("meridional", 1), ("meridional", -1)]

    for row, col in enumerate(cols):
        
        coord, sign = col
        ax[row].set_ylabel(eq.label)
         
        ax[row].set(
            title = eq.complete(
            wind_sign = sign, 
            recom = rc
            ))
            
        plot_gamma(
            ax[row],
            ds, 
            coord = coord, 
            rc = rc,
            drift = drift, 
            sign = sign
            )

    plot_roti(ax[4], ds, station = station)
    ax[0].legend(
        ncol = 4, 
        bbox_to_anchor = (.5, 1.7),
        loc = "upper center"
        )
        
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    if rc:
        w = "com"
    else:
        w = "sem"
        
    if drift == "vz":
        d = "variando"
    else:
        d = "constante"
    
    fig.suptitle(f"Taxas de crescimento totais devido aos ventos neutros, com deriva {d} no tempo e {w} recombinação")
    plt.show()
    
    return fig
    

 
def main():
    rc = False
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    fig = plot_total_all_effects(ds, rc =  rc)
    



