import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
import base as b 
import datetime as dt 


import matplotlib.patches as mpatches


def hor_gradient_image(ax, extent, darkest, **kwargs):


    img = np.linspace(0, 1, 100).reshape(1, -1)
    
    return ax.imshow(
        img, extent = extent, vmin=0, vmax=1, **kwargs)

def gradient_hbar(
        y, x0, x1, 
        ax=None, 
        info = '',
        height=0.7,
        darkest=1, 
        cmap = 'gray'
        ):
    
    factor = 2
    hor_gradient_image(
        ax, 
        extent = (x0, x1, y - height / factor, y + height / factor), 
        cmap = cmap, 
        darkest = darkest
        )
    
    rect = mpatches.Rectangle(
        (x0, y - height / factor), 
        x1 - x0, 
        height / (factor / 2),
        edgecolor = 'black',
        facecolor = 'none' 
        )
    
    ax.text(x1 + 0.1, y - 0.5, info, transform = ax.transData)
    
    ax.add_patch(rect)

fig, ax = plt.subplots(
    figsize = (12, 10), 
    dpi = 300
    )

gradient_hbar(0, 24, 25, ax=ax, info = 'F layer uplift (SL)')
gradient_hbar(-2, 27, 27.5, ax=ax, info = 'Spread F (SL)')

gradient_hbar(-4, 25, 28, ax=ax, info = 'EPB 1')

gradient_hbar(-22, 25, 29.2, ax=ax, info = 'EPB 2')
gradient_hbar(-24, 25, 28.5, ax=ax, info = 'Zonal wind divergence')
gradient_hbar(-26, 27, 28.5, ax=ax, info = 'Meridonal wind divergence')
gradient_hbar(-28, 25, 28, ax=ax, info = 'F layer uplift (CP)')
gradient_hbar(-30, 25, 28.5, ax=ax, info = 'Spread F (CP)')

gradient_hbar(-20, 27, 29, ax=ax, info = 'Temperature peak')
gradient_hbar(-18, 29, 30, ax=ax, info = 'OI 630,0 peak')

    
ax.set_aspect('auto')
ax.use_sticky_edges = False
ax.autoscale(enable=True, tight=False)



ax.set(
       ylabel = 'Geographic latitude (°)',
       xlabel = 'Universal time',
       xlim = [22, 34])
plt.show()