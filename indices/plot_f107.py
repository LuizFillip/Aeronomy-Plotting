import numpy as np 
import core as c 
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

def plot_f107_load( ax,  color = 'k'):
     df = c.low_omni()
     
     df = df.rename(columns= {'f10.7':'f107'})
     
     df = df.resample('D').mean()
     
     ax.plot(df.index, df['f107'], lw = 2, color = color)
     
     df = df.rolling(27).mean()
     
     ax.plot(
         df.index, 
         df['f107'], 
         lw = 3, color = 'blue', 
         label = '27 average'
         )
     
     ax.legend()
     
     ylim = [100, 300]
     step = 50
     ax.set(
         ylabel = 'F10.7 (sfu)', 
         ylim = ylim ,
         yticks = np.arange( ylim[0],  ylim[-1] + step, step)
         )   
     return None
 
    
def plot_kp(ax, start, end):
  
    df = c.low_omni()

    df = b.sel_dates(df, start, end)
    
    df = df.resample('D').max()
    
    dats = [df.loc[df['kp'] > 3], df.loc[df['kp'] <= 3]]
    
    colors = ['red', 'blue']
    names = ['Kp $>$ 3', 'Kp $\leq$ 3']
    for i, ds in enumerate(dats):
        
        ax.bar(
            ds.index, ds['kp'], 
            label = names[i],
            color = colors[i]
            )
    
    ax.set(
        ylim = [0, 10], 
        yticks = np.arange(0, 10, 3),
        ylabel = 'Kp'
        )
 
    ax.legend(ncol = 2)
    
    return None 
    