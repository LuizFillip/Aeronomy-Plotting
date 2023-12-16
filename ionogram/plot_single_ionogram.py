import matplotlib.pyplot as plt
from skimage import io
import numpy as np


def redefine_ticks(img):
    
    xticks = np.arange(0, 17, 1)
    yticks = np.arange(150, 1350, 150)

    x_positions = np.linspace(
        0, img.shape[1] - 1, 
        len(xticks)
        )
    y_positions = np.linspace(
        0, img.shape[0] - 1, 
        len(yticks)
        )
    
    plt.xticks(x_positions, xticks)
    plt.yticks(y_positions, yticks)
        
    
def crop_region_E(img):
    
    img = np.flipud(img)
    
    y, h = 128, 761
    x, w = 188, 559
    
    return img[y: y + h, x: x + w]



fig, ax = plt.subplots(
    figsize = (10, 8),
    dpi = 300)

fname = 'digisonde/data/ionogram/20130114/FZA0M_20130114(014)200000.PNG'

img = io.imread(fname)
img = crop_region_E(img)
ax.imshow(img)

plt.gca().invert_yaxis()


redefine_ticks(img)

ax.set(ylabel = 'Altitude (km)', 
       xlabel = 'Frequency (MHz)')

plt.show()