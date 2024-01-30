from settings import format_time_axes
import matplotlib.pyplot as plt
from labels import Labels
import pandas as pd
import matplotlib as mpl

def set_figure(
        ncols = 2, 
        nrows = 2, 
        figsize = , 
        dpi = 300
        ):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 10),
        ncols = 2,
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.2, 
        wspace = 0.1
        )
    
    return fig, ax
    
        
      

        
    

def plot_integrated_winds(ds):
   
    fig, (ax1, ax2, ax3, ax4) = set_figure(ncols = 1, nrows = 4)
    
    cols = ["zon", "zon_ef", "mer", "mer_ef"]
    axs = (ax1, ax2, ax3, ax4)
    for i, ax in enumerate(axs):
        
        plot(ax, ds, parameter = cols[i])
        
        ax.set(xlim = [ds.index[0], ds.index[-1]])
            
        if i == len(cols) - 1:
            format_time_axes(ax)
            
    fig.text(0.05, 0.4, "Altura de Apex (km)", 
             rotation = "vertical")
    
    norm = mpl.colors.Normalize(vmin=-110, vmax=110)
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap="rainbow"),
             ax = [ax1, ax2, ax3, ax4],
             label="Velocidade (m/s)")
    
    plt.show()
    
    return fig
    


