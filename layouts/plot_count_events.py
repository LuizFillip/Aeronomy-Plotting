import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import base as s 


def plot(ax, infile, filename):
    args = filename.split("_")
        
    df = pd.read_csv(infile + filename, 
                     index_col = 0)
    
    
    ymin = min(df.index)
    ymax = max(df.index)

    img = ax.pcolormesh(df.columns, 
                        df.index,
                        df.values, 
                        cmap = "Blues", 
                        vmax = 144)
                    
    ax.set_xticks(np.arange(0, 365, 30))
    
    years = np.arange(ymin, ymax + 1)
    
    ax.set(ylabel = "Anos", 
           xlabel = "Dias", 
           ylim = [ymin - 0.5, ymax])
    
    ax.set_yticks(years + 0.5, (years), 
                  va = "center")
    
    ax.text(0., 1.03,  f"{args[0]}", 
            transform = ax.transAxes, 
            fontsize = 16)
    
    s.colorbar_setting(img, ax, 
                       ticks = np.arange(0, 150, 20),
                       label = "# dados por dia")
    return ax
   



 
def plot_count_events(): 
    infile = "database/counts/"
    files = os.listdir(infile)
    
    fig, ax = plt.subplots(nrows = 2, 
                             figsize = (12, 8), 
                             sharex = True)
    
    plt.subplots_adjust(hspace = 0.1)
    
    for num, a in enumerate(ax.flat):
    
        plot(a, infile, files[num])
    
        if num == 0:
            a.set(xlabel = "")
        
    plt.show()