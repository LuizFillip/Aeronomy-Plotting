import matplotlib.pyplot as plt
import numpy as np
from FluxTube import Apex
import base as b

b.config_labels(fontsize = 25)

def infos(ax):
    x = -18
    fontsize = 35
    ax.text(
        x, 100, 
        'E region',
        transform = ax.transData, 
        fontsize = fontsize,
        color = 'k'
        )
    ax.text(
        x, 200, 'F region', 
        transform = ax.transData, 
        fontsize = fontsize,
        color = 'k'
        )
    

def plot_apex_vs_latitude(
       
        lim = 15,
        color = 'k'
        ):
    fig, ax = plt.subplots(
        figsize = (12, 6),
        dpi = 300
        )

    max_height = 500
    step = 50
    base = 75
    heights = np.arange(50, max_height + step, step )
     
   
    for h in heights:
        
        apx = Apex(h) 
        lats =  apx.latitude_range(
            points = 30, 
            base = 150
            )
        apex = apx.apex_range(
            points = 30, 
            base = base
            )
        
        if h == 300:
            args = dict(
                marker = 'o', 
                markerfacecolor = 'w', 
                lw = 2)
        else:
            args = dict(color = 'k', lw = 2)
            
        ax.plot(np.degrees(lats), apex, **args)    
        
    ax.set(
        xlim = [-lim, lim],
        ylim = [100, max_height],
        ylabel = "Altura de Apex (km)", 
        xlabel = "Latitude magnética (°)"
        )
    
    ax.axvline(0, linestyle = "--")

        
    ax.axhline(
        150, 
        color = "red", 
        lw = 2,
        linestyle = "--"
        )
    
   
    ax.axhline(
        300, 
        color = "k", 
        lw= 2,
        linestyle = "--"
        )
    
    # ax.text(
    #     0.03, 0.91, '(b)', 
    #     transform = ax.transAxes, 
    #     fontsize = fontsize
    #     )
        
    return fig 


fig = plot_apex_vs_latitude()

FigureName = 'magnetic_lines'

# fig.savefig(b.LATEX(FigureName, folder = 'modeling'), dpi = 400)