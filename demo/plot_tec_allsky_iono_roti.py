import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import plotting as pl
import os 
import imager as im
import base as b 
import datetime as dt 
import numpy as np
import PlasmaBubbles as pb 
import cartopy.crs as ccrs
from skimage import io


PATH_SKY = 'database/images/CA_2013_1224/'
PATH_IONO = 'database/ionogram/20131224F/'

b.config_labels(fontsize = 20)

def roti_limit(dn):
    

    df = pb.concat_files(dn, root = 'D:\\')

    df = b.sel_times(df, dn, hours = 11)
    
    lon_min = -48
    
    return df.loc[(df['lon'] > lon_min) ]

def plot_images(file, ax_img):
     
    AllSky = im.processing_img(
        os.path.join(PATH_SKY, file)
        )
    AllSky.display(ax_img, AllSky.bright)
            
    return im.fn2datetime(file)


def closest_iono(target):
    iono_times = [dg.ionosonde_fname(f) for 
                  f in os.listdir(PATH_IONO) 
                  if 'PNG' in f ]
    
    dn = b.closest_datetime(iono_times, target)
    
    return dn

def plot_ionogram(target, ax):
            
    dn = closest_iono(target)
    file = dn.strftime('FZA0M_%Y%m%d(%j)%H%M%S.PNG')
    
    infile = os.path.join(PATH_IONO, file)
    
    img = io.imread(infile)
    y, h = 300, 560
    x, w = 188, 559
    
    img = img[y: y + h, x: x + w]
   
    ax.imshow(img)
    
    ax.set(
        xticks = [], 
        yticks = []
        )
    
    return dn
    
    
    
def plot_shades(ax1, n, index):
    
    delta = dt.timedelta(minutes = 10)
    
    ax1.text(
        n, 4, 
        index, 
        transform = ax1.transData
        )
    
    ax1.axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
  
def title(ax, dn, index):
    title = dn.strftime(f'({index}) %Hh%M')
    ax.set(title = title)
 
    
fig = plt.figure(
    dpi = 300,
    figsize = (11,  14),
    layout = 'constrained'
    )

ncols = 4
gs2 = GridSpec(4, ncols)

gs2.update(hspace = 0.3, wspace = 0)



files = ['O6_CA_20131224_214144.tif', 
         'O6_CA_20131225_002749.tif',
         'O6_CA_20131225_011602.tif',
         'O6_CA_20131225_021645.tif']

dn = dt.datetime(2013, 12, 24, 20)

ax_rot = plt.subplot(gs2[-1, :])

pl.plot_roti_points(
        ax_rot, roti_limit(dn), 
        threshold = 0.25,
        label = True
        )

b.format_time_axes(ax_rot, translate = True)

for col, file in enumerate(files):
    index = col + 1
    
    ax_img = plt.subplot(gs2[0, col])
    
    target = plot_images(file, ax_img)
    
    title(ax_img, target, index)
    
    ax_ion = plt.subplot(gs2[1, col])
    
    dn = plot_ionogram(target, ax_ion)
    

    title(ax_ion, dn, index)
    
    ax_tec = plt.subplot(
        gs2[2, col], 
        projection = ccrs.PlateCarree())
    
    img = pl.plot_tec_map(
        target, ax_tec, vmax = 100, 
        colorbar = False)
    
    if index == 2:
        ax_ion.text(
            0.6, -0.1, 'Frequência (MHz)',
            transform = ax_ion.transAxes
        )
        ax_tec.text(
            0.6, -0.1, 'Longitude (°)',
            transform = ax_tec.transAxes
        )
    if index == 1:
        ax_ion.set(ylabel = 'Altura virtual (km)')
        
    if index != 1:
        ax_tec.set(
            xticks = [], 
            yticks = [], 
            xlabel = '', 
            ylabel = '', 
            title = ''
            )

    else:
        
        ax_tec.set(
            xticks = np.arange(-90, -20, 20), 
            yticks = np.arange(-40, 40, 20), 
                xlabel = '', 
                title = '')
        
    
    title(ax_tec, dn, index)
    
    plot_shades(ax_rot, target, index)



