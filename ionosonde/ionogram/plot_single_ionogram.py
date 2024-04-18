import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import digisonde as dg 

def redefine_ticks(ax, img):
    
    xticks = np.arange(0, 16, 2)
    yticks = np.arange(150, 1350, 150)

    x_positions = np.linspace(
        0, img.shape[1] - 1, 
        len(xticks)
        )
    y_positions = np.linspace(
        0, img.shape[0] - 1, 
        len(yticks)
        )
    
    ax.set_xticks(x_positions, xticks)
    ax.set_yticks(y_positions, yticks)
        

    
def crop_region_E(img):
    
    img = np.flipud(img)
    
    y, h = 130, 750
    x, w = 186, 560
    return img[y: y + h, x: x + w]

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
    img = crop_region_E(img)
    ax.imshow(img, aspect = aspect)
    ax.invert_yaxis()
    
    
    if label:
        redefine_ticks(ax, img)
        
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

    return fig

infile = 'database/ionogram/20130114S/'

def run():
    import os 
    
    for file in os.listdir(infile):
        if 'PNG' in file:
            dn = dg.ionosonde_fname(file)
            
            plt.ioff()
            
            fig = plot_single_ionogram(
                os.path.join(infile, file), 
                label = True, 
                title = True
                )
            
            FigureName = dn.strftime('%Y%m%d%H%M')
            
            fig.savefig('temp/' + FigureName)
            plt.close()
    
    
    # plt.show()