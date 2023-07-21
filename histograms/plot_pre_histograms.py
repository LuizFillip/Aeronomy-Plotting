import matplotlib.pyplot as plt
import numpy as np
from Digisonde.drift_utils import load_drift

def plotHistogram(ax, arr, binwidth = 10):

    lmax = round(arr.max())
    lmin = round(arr.min())

    bins = np.arange(lmin, 
                     lmax + binwidth, 
                     binwidth)

    ax.set(
           xlim = [lmin - binwidth, 
                   lmax + binwidth]
           )

    args = dict(facecolor = 'lightgrey', 
                alpha = 1, 
                edgecolor = 'black', 
                hatch = '////', 
                color = 'gray', 
                linewidth = 1)


    ax.hist(arr, bins = bins, **args)
     
    plot_stats(ax, arr)
    
    return ax
    
    
def plot_stats(ax, arr, unit = "m/s", fontsize = 15):
    mean = round(arr.mean(), 2)
    std = round(arr.std(), 2)
    vmax = round(arr.max(), 2)
    vmin = round(arr.min(), 2)
    
    
    info_mean = f"$\mu = {mean}$ {unit}\n"
    info_std = f"$\sigma = {std}$ {unit}\n"
    info_max = f"max = {vmax} {unit}\n"
    info_min = f"min = {vmin} {unit}"
    
    
    ax.text(0.05, 0.6, (info_mean + 
                        info_std + 
                        info_max + 
                        info_min), 
            fontsize = fontsize, 
            transform = ax.transAxes)
    
args = dict(
    site = "SSA", 
    ext = "RAW", 
    smoothed = True, 
    col = "vy"           
    )



def histogram_subplots(col = "vz", **args):
    
    if col == "vz":
        figtitle = "Deriva vertical - 2013"
    elif col == "vx":
        figtitle = "Deriva meridional - 2013"
    else:
        figtitle = "Deriva zonal - 2013"
    
    fig, ax = plt.subplots(nrows = 3, 
                           ncols = 4, 
                           sharex = True, 
                           sharey = True, 
                           figsize = (22, 12))
    
    ax[1, 0].set_ylabel("Numero de eventos", fontsize = 30)
    
    plt.subplots_adjust(wspace = 0.1)
    for n, ax in enumerate(ax.flat):
    
        df = load_drift(n, **args)
        
        arr = df[col].values
        title = df.index[0].strftime("%B")
        ax = plotHistogram(ax, arr, binwidth = 10)
        
        ax.set(title = title)
        
    fig.suptitle(figtitle, fontsize = 30)
    fig.text(0.43, 0.05, "Velocidade (m/s)", fontsize = 30)

        
histogram_subplots(**args)