import pandas as pd
import matplotlib.pyplot as plt
from common import plot_terminators, load
import settings as s
from utils import smooth2
import digisonde as dg


def load2(iono_file, alt = None):
    ds = pd.read_csv(iono_file, index_col = 0)
    ds.index = pd.to_datetime(ds.index)
    if alt is not None:
        return ds.loc[ds["alt"] == alt]
    else:
        return ds

def plot_parameters_iri_digisonde(alt = 300):
    
    
    iri = load2("database/IRI/march_2013.txt", alt = alt)
    
    dig = load2("database/Digisonde/profilogram/SAA0K_20130319(078)_pro", 
               alt = alt)
    
    dig["ne"] = smooth2(dig["ne"], 10)
    
    
    df = load("database/Digisonde/SAA0K_20130316(075)_cha")
    
    df["hmF2"] = smooth2(df["hmF2"], 5)
    df["foF2"] = smooth2(df["foF2"], 5)
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (15, 15), 
        nrows = 5, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0)
    
    ax[0].plot(iri["ne"], label = "IRI - 2016")
    ax[0].plot(dig["ne"], label = "Measured (São Luis)")
    
   
    
    ax[0].set(ylim = [0, 2.5e12], 
              ylabel = "Ne ($m^{-3}$)",
              xlim = [df.index[0], df.index[-1]])
    
    ax[1].plot(iri['hmF2'], label = "IRI - 2016")
    ax[1].plot(df["hmF2"], label = "Measured (São Luis)")
    
    ax[1].set(ylim = [100, 600], 
              ylabel = "hmF2 (km)",
              xlim = [df.index[0], df.index[-1]])
    
    ax[2].plot(iri['foF2'], label = "IRI - 2016")
    ax[2].plot(df["foF2"], label = "Measured (São Luis)")
    
    for i in range(3):
        ax[i].legend(ncol = 2, loc = "upper right")
    
    ax[2].set(ylim = [0, 20], ylabel = "foF2 (MHz)")
    
    infile = "database/Digisonde/SAA0K_20130216_freq.txt"


    
    df = load(infile)
    

    
    freqs = ['6', '7', '8']

    vz = dg.drift(df, sel_columns = freqs)
    
    for col in freqs:
        df[col] = smooth2(df[col], 4)
        vz[col] = smooth2(vz[col], 4)
        

    for num, col in enumerate(freqs):
        ax[4].plot(vz[col], label = f'{col} MHz')
        ax[3].plot(df[col], label = f'{col} MHz')


    ax[3].set(ylabel = "hF (km)", ylim = [100, 600])
        
    ax[3].legend( ncol = 3, loc = "upper right")
    
    

    ax[4].axhline(0, linestyle = '--')
    ax[4].set(
              ylabel = r"$V_z$ (m/s)", 
              ylim = [-60, 60], 
              xlim = [df.index[0], df.index[-1]]
              )
    ax[4].legend(ncol = 4, loc = "upper right")
    
    name = [f"Electron density ({alt} km)",
            "Peak height", 
            "F layer critical freqrency",
            "Real heights", 
            "Vertical drift"]
    
    s.format_time_axes(ax[4])
    
    for i, ax in enumerate(ax.flat):
        plot_terminators(ax, df)
        
        letter = s.chars()[i]
        ax.text(0.01, 0.82, f"({letter}) {name[i]}", 
                transform = ax.transAxes)
        
        
    return fig

fig = plot_parameters_iri_digisonde()

# fig.savefig("liken/src/figures/parameters_iri_digisonde.png", 
#               dpi = 300)


    
    
   
      
