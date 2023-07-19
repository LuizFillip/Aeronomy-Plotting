import matplotlib.pyplot as plt
from labels import Labels
import numpy as np
import settings as s
from RayleighTaylor import build
from utils import translate

    

    

def plot_profiles_parameters(date):
    infile = "database/FluxTube/201301012100.txt"

    fig, ax = plt.subplots(
        figsize = (12, 6), 
        sharey = True,
        ncols = 5,
        dpi = 300)

    plt.subplots_adjust(wspace = 0.05)

    def adding_labels(ax):

        cols = ['ratio', 'K', 'nui', "U", "U"]
        other =  ["", "", "", "\ngeográfico", "\nefetivo"]
        l = Labels().infos
        for i, col in enumerate(cols):
            info = l[col]
         
            ax[i].set(title = info["name"] + other[i],
                xlabel = f"{info['symbol']} ({info['units']})")
        
       
        
    for hem in ["north", "south"]:

        cols = ['ratio', 'K', 'nui', 'zon', 'zon_ef']
        
        ds = build(infile, hemisphere = hem, 
                   remove_smooth = 15)
            
        for i, col in enumerate(cols):
            
            ax[i].plot(ds[col], ds.index, 
                       label = translate(hem).title())
            
            ax[i].legend(loc = "upper left")
            
            if "zon" in col:
                ax[i].set(xlim = [-50, 50])
           
                

    adding_labels(ax)
    ax[0].set(ylabel  = "Altura de apex (km)", 
              yticks = np.arange(210, 600, 50), 
              ylim = [210, 600])

    plt.show()