import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import plotting as pl
import os 
import imager as im
import base as b 
import datetime as dt 
import PlasmaBubbles as pb 


PATH_SKY = 'database/images/CA_2013_1224/'
PATH_IONO = 'database/ionogram/20131224F/'

def plot_images(file, ax_img):
     
    AllSky = im.processing_img(
        os.path.join(PATH_SKY, file)
        )
    AllSky.display(ax_img, AllSky.bright)
            
    return im.fn2datetime(file)

# 


def closest_iono(target):
    iono_times = [dg.ionosonde_fname(f) for 
                  f in os.listdir(PATH_IONO) 
                  if 'PNG' in f ]
    
    dn = b.closest_datetime(iono_times, target)
    
    return dn.strftime('FZA0M_%Y%m%d(%j)%H%M%S.PNG')

def plot_ionogram(target, ax_ion):
            
    file = closest_iono(target)
    infile = os.path.join(PATH_IONO, file)
    pl.plot_single_ionogram(
        infile, ax = ax_ion
        )


fig = plt.figure(
    dpi = 300,
    figsize = (16,  10),
    layout = 'constrained'
    )

ncols = 4
gs2 = GridSpec(3, ncols)

gs2.update(hspace = 0, wspace = 0.5)



files = ['O6_CA_20131224_214144.tif', 
         'O6_CA_20131224_214144.tif',
         'O6_CA_20131224_214144.tif',
         'O6_CA_20131224_214144.tif']


# plot_ionogram(times)

for col, file in enumerate(files):
    
    ax_img = plt.subplot(gs2[0, col])
    
    target = plot_images(file, ax_img)
    
    ax_ion = plt.subplot(gs2[1, col])
    
    plot_ionogram(target, ax_ion)
    
  