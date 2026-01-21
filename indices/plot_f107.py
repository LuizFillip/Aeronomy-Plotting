import base as b 
import numpy as np 

def plot_f107(
        ax, 
        df, 
        color = 'k'
        ):
    
   
    
    ax.plot(df['f107'], color = color)
   
        
    ax.set(
        ylabel = '$F10,7$ (sfu)', 
        ylim = [50, 300],
        yticks = np.arange(50, 350, 100)
        )   
    return None