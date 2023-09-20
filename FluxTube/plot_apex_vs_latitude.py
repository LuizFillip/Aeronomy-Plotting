import matplotlib.pyplot as plt
import numpy as np
from FluxTube import Apex
import settings as s



def plot_apex_vs_latitude(
        hmin = 200, 
        hmax = 700, 
        points = 100, 
        dz = 50, 
        base = 150):
        
    heights = np.arange(hmin, hmax + dz, dz)
     
    fig, ax = plt.subplots(
        figsize = (6, 5), 
        dpi = 300
        )   
    
    s.config_labels()

        
    for h in heights:
        apx = Apex(h)
        lats =  apx.latitude_range(
            points = points, 
            base = base
            )
        apex = apx.apex_range(
            points = points, 
            base = base
            )
        ax.plot(np.degrees(lats), apex, color = "w")    
        
    ax.set(
        ylabel = "Altura de apex (km)", 
        xlabel = "Latitude geomagnética (°)",
        ylim = [hmin, hmax]
           )
    
    ax.axvline(0, linestyle = "--")

        
    ax.axhline(150, color = "red", lw= 2,
                linestyle = "--", 
                label = "Região E")
    
    ax.axhline(300, color = "k", lw= 2,
                linestyle = "-")
    
    ax.legend()
    
    return fig, ax


fig, ax = plot_apex_vs_latitude(
    hmin  = 0, hmax = 500, 
    points = 100, dz = 200, 
    base = None)




# s.dark_background(fig, ax)

# fig.savefig('temp.png', transparent=True)