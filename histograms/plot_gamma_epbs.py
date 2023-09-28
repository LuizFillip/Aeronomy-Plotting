import events as ev
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 


df = b.load('interval.txt')

b.config_labels()

args = dict(
     facecolor = 'lightgrey', 
     edgecolor = 'black', 
     hatch = '////', 
     color = 'gray', 
     linewidth = 1
     )

def plot_hist(ax, arr, binwidth = 20):

    lmax = round(np.nanmax(arr))
    lmin = round(np.nanmin(arr))

    bins = np.arange(lmin, 
                     lmax + binwidth, 
                     binwidth)
    
    ax.hist(arr, bins = bins, **args)

    ax.set(
           xlim = 
           [lmin - binwidth, lmax + binwidth]
           )
    
def plot_stats(ax, arr, unit = "min", fontsize = 15):
    mean = round(np.nanmean(arr), 2)
    std = round(np.nanstd(arr), 2)
    
    
    info_mean = f"$\mu = {mean}$ {unit}\n"
    info_std = f"$\sigma = {std}$ {unit}\n"
  
    ax.text(
        0.85, 0.6, (info_mean + info_std), 
            fontsize = fontsize, 
            transform = ax.transAxes)
    

def plot_gamma_epbs_count(
        arr, 
        binwidth = 20
        ):
    
    fig, ax = plt.subplots(
        figsize = (8, 6), 
        dpi = 300
        )
    
    
    plot_hist(ax, arr, binwidth =  binwidth)
    
    plot_stats(ax, arr)
    
    ax.set(
        xlabel = '$\\delta t$ (minutes)', 
        ylabel = 'Frequency'
        )
    
    return fig
    
arr = df.values.ravel()
fig = plot_gamma_epbs_count(arr)

