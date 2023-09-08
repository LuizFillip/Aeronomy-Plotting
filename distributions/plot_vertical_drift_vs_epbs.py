import numpy as np
import matplotlib.pyplot as plt

def plot_vertical_drift_distribution(
        df, 
        ymin = 0,
        ymax = 100, 
        yset = 20
        ):
    
    """
    Plotting probability distribution from 
    EPB occurence and PRE peak
    """
    
    year = df.index[0].year

    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 8)
        )
    
    df["rate"] = df["rate"] * 100
            
    df["rate"].plot(ax = ax, 
                    marker = "o", 
                    lw = 2, 
                    markersize = 18, 
                    color = "red")
    
    ax.set(ylim = (ymin - yset, ymax + yset), 
           xlabel = "$V_{zp}$ (m/s)", 
           ylabel = "Probabilidade de ocorrência (%)", 
           xlim = [-10, 90], 
           xticks = np.arange(-10, 100, 10), 
           yticks = np.arange(ymin, ymax + yset, yset))
    
    for bar in [ymin, ymax]:
        ax.axhline(bar, linestyle = ":", 
                   lw = 2, color = "k")
        
    for bar in [20, 60]:
        ax.axvline(bar, linestyle = "--", 
                   lw = 3, color = "k")
    
    ax.text(0.05, 0.9, 
            year,
            transform = ax.transAxes)    
    plt.show()
    
    return fig

