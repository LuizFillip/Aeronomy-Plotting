import numpy as np
import magnet as mg

def plot_electrojet(ax):
      
    df = mg.electrojet(c1 = 'slz', c2 = 'eus')
    
    ax.plot(
        df.iloc[:, 0], color = 'k', 
        lw = 2, label = 'Storm-time')
    ax.plot(
        df.iloc[:, 1], color = 'purple',
        lw = 2, label = 'Quiet-time'
        )
    ax.set(
        ylabel = '$\Delta H_{EEJ}$ (nT)', 
        yticks = np.arange(-100, 200, 50), 
        ylim = [-100, 180]
        )
    ax.axhline(0, linestyle = ':')
    
    ax.legend(ncol = 1, loc = 'upper right')
    
    return None 
    