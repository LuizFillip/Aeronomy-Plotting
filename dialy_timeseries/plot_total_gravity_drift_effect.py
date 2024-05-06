import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_roti, plot_terminators
import pandas as pd


def sum_gravity(df, recom = False):
    res = []
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        gamma = rt.effects_due_to_gravity(
            ds, recom = recom)
        
        res.append(gamma)
    
    return pd.concat(res, axis = 1).sum(axis = 1)


def sum_drift(df, recom  = False, drift = "vz"):
    res = []
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        gamma = rt.effects_due_to_drift(
                        ds, 
                        recom = recom, 
                        col = drift
                        )
        
        res.append(gamma)
    
    return pd.concat(res, axis = 1).sum(axis = 1)


def plot_gravity(ax, ds, recom  = False):
    
    eq = rt.EquationsFT()
    
    gamma = sum_gravity(ds, recom = recom)
     
    ax.plot(gamma * 1e4, label = eq.gravity(recom = recom))
                
    ax.set(ylim = [-40, 40], ylabel = eq.label,
           xlim = [ds.index[0], ds.index[-1]])
    
    ax.axhline(0, linestyle = "--")
    
    ax.text(0.05, 0.8, "Efeito à gravidade",
            transform = ax.transAxes)
    ax.legend(ncol = 2, 
              bbox_to_anchor = (0.5, 1.45),
              loc = "upper center")


def plot_drift(
        ax, 
        ds, 
        recom = False,
        drift = "vz"
        ):
    eq = rt.EquationsFT()

    gamma = sum_drift(ds, drift = drift, recom = recom)
     
    ax.plot(gamma * 1e4, label = eq.drift(recom = recom))
                
    ax.set(ylim = [-40, 40], ylabel = eq.label,
           xlim = [ds.index[0], ds.index[-1]])
    
    ax.axhline(0, linestyle = "--")
    ax.text(0.05, 0.8, f"$V_P = $ {drift.title()}", 
            transform = ax.transAxes)
    
    ax.legend(ncol = 2, 
              bbox_to_anchor = (0.5, 1.45),
              loc = "upper center")



def plot_total_gravity_drift_effect(
        ds, station = "salu"
        ):
    
    fig, ax = plt.subplots(
        figsize = (14, 10),
        nrows = 4,
        dpi = 300,
        sharex = True,
        )

    plt.subplots_adjust(hspace = 0.4)

    for row, rc in enumerate([False, True]):
        
        plot_gravity(ax[0], ds, recom = rc)
        plot_drift(ax[1], ds, recom = rc, drift = "vz")
        plot_drift(ax[2], ds, recom = rc, drift = "vzp")

    plot_roti(ax[3], ds, station = station)
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    fig.suptitle("Taxa de crescimento totais devido à gravidade e a deriva vertical")
        
    return fig


def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    
    df = rt.load_process(infile, apex = 300)
    
    #ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    
    import datetime as dt

    start = dt.datetime(2013, 3, 16, 20)
    end =  dt.datetime(2013, 3, 19, 20)
    ds = df[(df.index >= start) & (df.index <= end)]
    fig = plot_total_gravity_drift_effect(ds, station = "salu")
    
    plt.show()
# main()