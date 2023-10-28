import matplotlib.pyplot as plt
import numpy as np
from FluxTube import Apex
import base as b

b.config_labels()

def plot_apex_vs_latitude(
        ax, 
        hmin = 200, 
        hmax = 700, 
        points = 100, 
        dz = 50, 
        base = 150
        ):
        
    heights = np.arange(hmin, hmax + dz, dz)
     
   
    # for h in heights:
        
    h = 300 
    apx = Apex(h)
    lats =  apx.latitude_range(
        points = points, 
        base = base
        )
    apex = apx.apex_range(
        points = 100, 
        base = 75
        )
        
    ax.plot(np.degrees(lats), 
            apex, color = "k", lw = 2)    
    
    lim = 25
    ax.set(
        xlim = [-lim, lim],
        ylim = [75, 400],
        ylabel = "Apex height (km)", 
        xlabel = "Magnetic latitude (°)"
        )
    
    ax.axvline(0, linestyle = "--")

        
    ax.axhline(150, color = "red", lw= 2,
                linestyle = "--")
    ax.text(12, 100, 'E region',
            transform = ax.transData)
    ax.text(12, 200, 'F region', 
            transform = ax.transData)
    
    ax.axhline(300, color = "k", lw= 2,
                linestyle = "--")
        
    return ax

# fig, ax = plt.subplots(
#     figsize = (7,5), 
#     dpi = 400
#     )   

# plot_apex_vs_latitude(ax)