import pandas as pd
import datetime as dt
import ionosphere as io
import numpy as np
import matplotlib.pyplot as plt
from models import altrange_iri
import FluxTube as ft
from utils import translate
from utils import smooth2
from labels import Labels


def plot_profiles(fig, ax, df, glat = -2, col = "Ne"):
    
    dn = dt.datetime(2013, 1, 1, 21, 0)
    iri = altrange_iri(dn,
                       glat = glat, 
                       hmin = 150,
                       hmax  = 700, 
                       glon = -44)
    
    name = translate(col.replace("_F", "").title())
    
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


    for hemisphere in ["south", "north"]:
        ds = ft.IntegratedParameters(
            io.load_calculate(infile),
            hemisphere
            )

            
        Ne = ds["N"].values
        alts = ds.index.values

        K = smooth2(ft.gradient_integrated(Ne, alts), 5)
        
        ax[0].plot(Ne, alts, label = hemisphere)
        ax[1].plot(K, alts, label = hemisphere)
        
        ax[0].legend()
        ax[1].legend()
    
    
    ax[1].set(xlabel = "$K = \\frac{1}{N_0 R_e L^3}\\frac{\partial }{\partial L}  (N L^3)$")
    
    
    

        
    




