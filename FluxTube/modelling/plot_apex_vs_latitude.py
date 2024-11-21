import matplotlib.pyplot as plt
import numpy as np
from FluxTube import Apex
import base as b

b.config_labels(fontsize = 35)

    
    
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
            
    return None
    

def plot_arrow(ax, lat_mag = 3):
    
    zeq = Apex(400).apex_height(lat_mag)
        
    ax.arrow(
        x = lat_mag, y= 0, 
        dx = 0, dy = zeq, width= 0.1, 
        color='red', head_length = 5,
        label = 'Altura local'
        ) 
    return None 

def sel_height(h, height = 300):
    if h == 300:
        args = dict(
            marker = 'o', 
            markerfacecolor = 'w', 
            lw = 2)
    else:
        args = dict(color = 'k', lw = 2)
        
    return args

def grad(ax, xy, xytext):

    ax.annotate(
        '$\\nabla n_0$', xy=xy, 
        xytext=xytext,
        arrowprops=dict(
            color = 'green',
            lw = 4,
            arrowstyle='->'), 
        transform = ax.transData, 
        fontsize = 40, 
        color = 'green')
    return None 

def total_U(ax, xy, xytext):

    ax.annotate(
        '', xy=xy, 
        xytext=xytext,
        arrowprops=dict(
            color = 'blue',
            lw = 4,
            arrowstyle='<-'), 
        transform = ax.transData, 
        fontsize = 40, 
        color = 'blue')
    return None 

def info(ax, text, x, y, color = 'k', font = 40):
    ax.text(
        x, y, text, 
    color = color,
    fontsize = font,
    transform = ax.transData)
    return None 



def plot_apex_vs_latitude(
        ref_height = 300, 
        ax = None, 
        lim = 12,
        max_height = 500, 
        step = 100,
        base = 100,
        translate = False
        ):
    if ax is None:
        fig, ax = plt.subplots(
            figsize = (14, 10),
            dpi = 300
            )

    heights = np.arange(base, max_height, step )
    
    heights = [120, 180, 350, 500, 600]
    
    for h in heights:
        
        apx = Apex(h) 
        lats =  apx.latitude_range(
            points = 30, 
            base = 100
            )
        apex = apx.apex_range(
            points = 30, 
            base = 75
            )
        
        color = 'k'
        args = dict(color = color, lw = 2, linestyle = '-')
        ax.plot(np.degrees(lats), apex, **args)    
    
    if translate:
        ylabel = "Altura de Apex (km)"
        xlabel = "Latitude magnética (°)"
    else:
        ylabel = 'Apex height (km)'
        xlabel = 'Magnetic Latitude (°)'
    ax.set(
        xlim = [-lim, lim],
        ylim = [0, 400],
        ylabel = ylabel, 
        xlabel = xlabel
        )
    
    # ax.axvline(0, linestyle = "--", lw = 1)
    x = -6.6
    y = 250
    total_U(ax, (-10, y), (10, y))
    
    total_U(ax, (x, y), (-5, 300))
    total_U(ax, (x, y), (-4, 200))
    
    total_U(ax, (-x, y), (8.3, 200))
    total_U(ax, (-x, 250), (9, 290))
    
    grad(ax, (-2, 300), (-3, 200))
    # plot_hlines(ax)
    info(ax, '$V_{mpl}$', -7, 200)
    info(ax, '$V_{msr}$', 5, 200)
    info(ax, '$V_{msl}$', -8, 290)
    info(ax, '$V_{mpr}$', 6, 290)
    info(ax, '$V_{m}$', 0, 260, color = 'blue')
    
    info(ax, 'Diminui $\Sigma$', -8, 330, 
         font = 35, color = 'red')
    info(ax, 'Desastabiliza', -9, 150, 
         font = 35, color = 'red')
    info(ax, 'Aumenta $\Sigma$', 4, 150 , 
         font = 35, color = 'red')
    info(ax, 'Estabiliza', 4, 330, 
         font = 35, color = 'red')
    
    return fig 

def main():
    fig = plot_apex_vs_latitude(translate = True)
    # 
    FigureName = 'magnetic_lines_meridional_winds'
    
    fig.savefig(b.LATEX(FigureName, folder = 'winds'), dpi = 400)
    
# main()


