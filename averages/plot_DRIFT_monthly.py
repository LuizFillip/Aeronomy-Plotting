from digisonde import filter_values, pivot_data
import matplotlib.pyplot as plt
import numpy as np
from build import monthToNum


def plotDays(ax, df):

    for col in df.columns:
        ax.plot(df[col], lw = 0.5)

def plotAgerage(ax, avg, std):
 
    ax.plot(avg, label = "$\mu$", color = "k", lw = 2)
    
    for i in range(1, 3):
        ax.fill_between(avg.index, 
                        avg + i * std, 
                        avg - i * std, 
                        alpha = 0.3, 
                        label = f"{i} $\sigma$")
    
    ax.axhline(0, color = "red", linestyle = "--")
    
    ax.legend(ncol = 3)
    

def plot_average_and_std(col = "vy", n = 1):
    
    df = pivot_data(n, col = col)
        
    avg = df.mean(axis = 1)
    
    std = df.std(axis = 1)
    
    if col == "vx":
        name = "meridional"
        lim = 200
    elif col == "vy":
        name = "zonal"
        lim = 300
    
    new_df = filter_values(avg, std, df, std_factor = 1)
    
    fig, ax = plt.subplots(figsize = (10, 8), 
                           nrows = 2, 
                           sharex = True, 
                           sharey = True)
    
    plt.subplots_adjust(hspace = 0.1)
    
    for n, d in enumerate([df, new_df]):
        
        
        plotDays(ax[n], d)
        plotAgerage(ax[n], avg, std)
        
        ax[n].set(ylabel = f"Velocidade {name} (m/s)")
        
    ax[0].set(title = f"{monthToNum(1)} - São Luis")
    ax[1].set(xticks = np.arange(0, 25, 2),
              ylim = [-lim, lim],
              xlabel = "Hora universal")

#plot_average_and_std(col = "vx", n = 1)
