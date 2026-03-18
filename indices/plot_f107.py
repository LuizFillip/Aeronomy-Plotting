import numpy as np 

def plot_f107(
        ax, 
        df, 
        color = 'k', 
        ylim = [50, 300], step = 100
        ):
    
    df = df.rename(columns= {'f10.7':'f107'})
   
    ax.step(df.index, df['f107'], color = color)
        
    ax.set(
        ylabel = 'F10.7 (sfu)', 
        ylim = ylim ,
        yticks = np.arange( ylim[0],  ylim[-1] + step, step)
        )   
    return None