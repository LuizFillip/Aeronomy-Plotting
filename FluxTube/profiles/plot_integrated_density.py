import datetime as dt

import numpy as np
import matplotlib.pyplot as plt



def plot_profiles(fig, ax, df, glat = -2, col = "Ne"):
    
   
    if name == "Norte":
        label1 = "Local"
        label2 = "Fluxo de Tubo"
    else:
        label1 = ""
        label2 = ""
        
        
    ax.plot(np.log10(iri["ne"]),
            iri.index, 
            label = label1)
    
    ax1 = ax.twiny()
    ax1.plot(np.log10(df[col]), df.index, 
             label = label2,
             linestyle = "--")
    
    fig.legend(ncol = 2, 
               bbox_to_anchor=(0.5, 1.01), 
               loc="upper center")
    
    
    
    ax1.set(xlim = [13, 20], 
           xlabel = "Fluxo de tubo log10(N) ($cm^{-2}$)")
    ax.set(xlim = [4, 7], 
           xlabel = "Local log10(Ne) ($cm^{-3}$)")
    
    ax.text(0.1, 0.9, name, transform = ax.transAxes)
    
def plot_ft_density_profiles(Ne, K, alts):
    ffig, ax = plt.subplots(
        figsize = (8, 6),
        sharey = True,
        ncols = 2, 
        dpi = 300,
        
        )

    plt.subplots_adjust(wspace = 0.05)
    
    infile = "database/FluxTube/201301012100.txt"
    
    ax[1].set(xlabel = "$K = \\frac{1}{N_0 R_e L^3}\\frac{\partial }{\partial L}  (N L^3)$")
    
    
    

import plotting as pl 

ds = pl.load_fluxtube()

ds




