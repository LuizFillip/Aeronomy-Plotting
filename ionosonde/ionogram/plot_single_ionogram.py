import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import digisonde as dg 
import os 
def ionogram_path(dn, site, root = 'E:\\'):
    
    start = dn - dt.timedelta(days = 1)
    folder_ion = start.strftime(f'%Y/%Y%m%d{site[0]}')
    
    fmt = f'{site}_%Y%m%d(%j)%H%M%S.PNG'
    
    target = dn.strftime(fmt)
    
    return os.path.join(root, 'ionogram', folder_ion, target)
    
 

    
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
        title = False
        ):
    
  
    if ax is None:
        fig, ax = plt.subplots(
            figsize = (10, 8),
            dpi = 300)
        
        
    
    img = io.imread(fname)
    img = crop_image(img)


    ax.imshow(img, aspect = 'auto', extent = [-1, 15, 50, 1280])


    ax.set(ylim = [150, 1000], 
           xlim = [0, 10])
    
    
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


dn = dt.datetime(2022, 7, 25)

site = 'CAJ2M'

target = dt.datetime(2022, 7, 25, 2)
# site, fname = dg.path_ionogram(
#         dn, 
#         target = target, 
#         site = 'CAJ2M', #'SAA0K'
#         root = 'E:\\'
#         )

fname = ionogram_path(dn, site, root = 'E:\\')



plot_single_ionogram(fname, label = True)