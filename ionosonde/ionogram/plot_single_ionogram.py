import matplotlib.pyplot as plt
# from skimage import io
import numpy as np
import digisonde as dg 
from PIL import Image
import datetime as dt 


    
def crop_image(img):
    
    img = np.flipud(img)

    y, h = 50, 900
    x, w = 150, 600
    img =  img[y: y + h, x: x + w]
    img = np.flipud(img)

    return img

def plot_single_ionogram(
        img_path, 
        ax = None, 
        label = False, 
        ylabel_position = "left",
        aspect = 'auto', 
        title = False, 
        ylim = [80, 1000]
        ):
    
  
    if ax is None:
        fig, ax = plt.subplots(
            figsize = (10, 8),
            dpi = 300
            )
        
        
    
    # img = io.imread(fname)
    # img = crop_image(img)
    
    img = Image.open(img_path)


    crop_box = (185, 50, 750, 920)  
    crop_box = (185, 50, 750, 920)  

    # (left, upper, right, lower) => coordenadas do retângulo de corte

    cropped_img = img.crop(crop_box)


    ax.imshow(
        cropped_img, 
        aspect = 'auto', 
        extent=[0, 16, 80, 1280]
        )
    
    ax.set_xlim(0, 16)
    ax.set_ylim(80, 1280)
    
    xlim = [0, 16]
    step = 4
    ax.set(
        # ylim = ylim, 
        # xlim = [0, 12], 
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
        time = dg.ionosonde_fname(img_path)

        ax.set(title = time.strftime('%Y-%m-%d %Hh%M'))
    
    if ax is None:
        return fig
    



def main():

    dn = dt.datetime(2020, 2, 27, 22, 30)
  
    dn = dt.datetime(2020, 1, 12, 22, 30)
    
    site = 'SAA0K'
    dn = dt.datetime(2020, 3, 2, 22, 30)
    fname = dg.IonoDir(site, dn, root = 'D').dn2PNG
    
    fname = f'D:\\ionogram\\quiet\\{fname}'
    # print(fname)
    
    plot_single_ionogram(fname, label = True)
    


# main()


