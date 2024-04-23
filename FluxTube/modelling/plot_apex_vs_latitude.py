import matplotlib.pyplot as plt
import numpy as np
from FluxTube import Apex
import base as b

b.config_labels(fontsize = 25)

    
    
def plot_hlines(ax, label = False, x = -18):
    
    colors = ['r', 'k']
    names = ['Região E', 'Região F']
    
    for i, height in enumerate([150, 300]):
        ax.axhline(
            height, 
            color = colors[i], 
            lw = 1,
            linestyle = "-"
            )
        if label:
            
            ax.text(
                x, height - 50, 
                names[i],
                transform = ax.transData,
                color = 'k'
                )
    

def plot_arrow(ax, lat_mag = 3):
    
    zeq = Apex(400).apex_height(lat_mag)
        
    ax.arrow(
        x = lat_mag, y= 0, 
        dx = 0, dy=zeq, width= 0.1, 
        color='red', head_length = 5,
        label = 'Altura local') 

def sel_height(h, height = 300):
    if h == 300:
        args = dict(
            marker = 'o', 
            markerfacecolor = 'w', 
            lw = 2)
    else:
        args = dict(color = 'k', lw = 2)
        
    return args

def plot_apex_vs_latitude(
        ref_height = 300, 
        ax = None, 
        lim = 15,
        max_height = 500, 
        step = 100,
        base = 100,
        translate = False
        ):
    if ax is None:
        fig, ax = plt.subplots(
            figsize = (10, 10),
            dpi = 300
            )

    heights = np.arange(base, max_height, step )
     
   
    for h in [300]:
        
        apx = Apex(h) 
        lats =  apx.latitude_range(
            points = 30, 
            base = 150
            )
        apex = apx.apex_range(
            points = 30, 
            base = base
            )
        
        if h == ref_height:
            color = 'black'
        else:
            color = '#0C5DA5'
        
            
        args = dict(color = color, lw = 2, linestyle = '--')
        ax.plot(np.degrees(lats), apex, **args)    
    
    if translate:
        ylabel = "Altura de Apex (km)"
        xlabel = "Latitude magnética (°)"
    else:
        ylabel = 'Apex height (km)'
        xlabel = 'Magnetic Latitude (°)'
    ax.set(
        xlim = [-lim, lim],
        ylim = [100, 450],
        ylabel = ylabel, 
        xlabel = xlabel
        )
    
    ax.axvline(0, linestyle = "--", lw = 1)

    
    plot_hlines(ax)

    if ax is None:
        return fig 

def main():
    fig = plot_apex_vs_latitude()
    # 
    FigureName = 'magnetic_lines'
    
    fig.savefig(b.LATEX(FigureName, folder = 'modeling'), dpi = 400)