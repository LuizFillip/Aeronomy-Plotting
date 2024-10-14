import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import digisonde as dg 
import os 


    
def crop_image(img):
    
    img = np.flipud(img)

    y, h = 50, 900
    x, w = 150, 600
    img =  img[y: y + h, x: x + w]
    img = np.flipud(img)

    return img

def plot_single_ionogram(
        fname, 
        ax = None, 
        label = False, 
        ylabel_position = "left",
        aspect = 'auto', 
        title = False, 
        ylim = [150, 1000]
        ):
    
  
    if ax is None:
        fig, ax = plt.subplots(
            figsize = (10, 8),
            dpi = 300)
        
        
    
    img = io.imread(fname)
    img = crop_image(img)

    ax.imshow(
        img, 
        aspect = 'auto', 
        extent = [-1, 15, 50, 1280]
        )
    
    xlim = [0, 10]
    step = 2
    ax.set(
        ylim = ylim, 
        xlim = [0, 10], 
        xticks = np.arange(xlim[0], xlim[-1] + step, step)
        )
    
    
    if label:
       
        ax.set(
            ylabel = 'Altitude (km)', 
            xlabel = 'Frequency (MHz)'
            )
        
        if ylabel_position == 'left':
            labelleft = True
            labelright = False
        else:
            labelright = True
            labelleft = False
        
        
        ax.tick_params(
            top = True,
            right = True,
            left = False,
            bottom = False,
            labelright = labelright,
            labelleft = labelleft,
            # labeltop = True, 
            # labelbottom = False, 
            # 
            )
        ax.yaxis.set_label_position(ylabel_position)
        
    else:
        ax.axis('off')
    
    if title:
        time = dg.ionosonde_fname(fname)

        ax.set(title = time.strftime('%Y-%m-%d %Hh%M'))
    
    if ax is None:
        return fig
    

import datetime as dt 


def main():

    dn = dt.datetime(2022, 7, 25)

    site = 'CAJ2M'
    
    
    # site, fname = dg.path_ionogram(
    #         dn, 
    #         target = target, 
    #         site = 'CAJ2M', #'SAA0K'
    #         root = 'E:\\'
    #         )
    
    fname = dg.path_from_site_dn(dn, site, root = 'E:\\')
    
    
    plot_single_ionogram(fname, label = True)
    


# main()

import pandas as pd 
start = dt.datetime(2022, 7, 25, 1)

times = pd.date_range(start, freq = '1H', periods = 6)


fig, ax = plt.subplots(
    figsize = (18, 16), 
    ncols = len(times), 
    nrows = 2, 
    # sharex = True, 
    # sharey = True
    )

plt.subplots_adjust(hspace = 0.2, wspace=0)


for i, dn in enumerate(times):
    
    title = dn.strftime('%Hh%M')
    
    fname = dg.path_from_site_dn(dn, 'FZA0M')
    
    plot_single_ionogram(
        fname, 
        ax[0, i], 
        label = True, 
        ylim = [100, 1200]
        )
    
    ax[0, i].set(
      
        yticklabels = [], 
        xticklabels = [], 
        xlabel = '', 
        ylabel = ''
        )
    ax[0, i].text(
        0.3, 0.85, 
        title, color = 'w',
        transform = ax[0, i].transAxes
        )
    
    fname = dg.path_from_site_dn(dn, 'CAJ2M')
    
    plot_single_ionogram(
        fname, 
        ax[1, i],
        label = True, 
        ylim = [100, 1200]
        )
    
    ax[1, i].text(
        0.3, 0.85, title, color = 'w',
                  transform = ax[1,i].transAxes)
    
    if i != 0:
      
        ax[1, i].set(
            yticklabels = [], 
            xticklabels = [], 
            xlabel = '', 
            ylabel = ''
            )

y = 1.01
x = 0.01
fontsize = 45
ax[1, 0].text(
    x, y, 
    'Cachoeira Paulista', 
    fontsize = fontsize,
    transform = ax[1, 0].transAxes
    )


ax[0, 0].text(
    x, y,
    'Fortaleza', 
    fontsize = 40,
    transform = ax[0, 0].transAxes
    
    )