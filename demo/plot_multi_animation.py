import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import events as ev 
import os 
import imager as im
import base as b 
import datetime as dt 
from plotting import plot_roti_curves




def folder_date(dn):
    return dn.strftime('%Y%m%d')

def plot_imager(ax2, fname):
    
    img = io.imread(fname, as_gray = True)
    
    ax2.imshow(
        img, 
        cmap = 'gray'
        )
       
    ax2.set_axis_off()
    
    dn = im.imager_fname(fname).datetime
    title = dn.strftime('%H:%M')
    ax2.set(title = title)
    

    return ax2

def plot_ionogram(ax2, fname):
        
    img = io.imread(fname)
    
    ax2.imshow(
        dg.crop_image(
            img, 
            y = 200,
            h = 700, 
            x = 150, 
            w = 620
            )
        )
    
    ax2.tick_params(
        labelbottom = False, 
        labelleft = False
        )
    
    dn = dg.ionosonde_fname(fname) 
    
    title = dn.strftime('%H:%M')
    
    ax2.set(title = title)
     
    ax2.set(
        ylabel = 'Virtual Height (km)'
        )

    return dn

def shade(ax1, n):
    
    delta = dt.timedelta(minutes = 10)
                
      
    ax1.axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )


dn = dt.datetime(2013, 1, 14, 20)



PATH_IMAG = f'imager/img/{im.folder_from_dn(dn)}/'
PATH_IONO = f'digisonde/data/ionogram/{folder_date(dn)}/'


def plot_multianim(fname):

    fig = plt.figure(
        dpi = 400,
        figsize = (12, 8),
        layout = "constrained"
        )
    
    
    gs2 = GridSpec(2, 2)
    
    gs2.update(
        hspace = 0.2,  
        wspace = 0.2
        )
    
    ax1 = plt.subplot(gs2[0, 0])
    ax2 = plt.subplot(gs2[0, 1])
    
    ax3 = plt.subplot(gs2[-1, :])
        
    imag = os.path.join(
        PATH_IMAG,
        fname
        )
    
    plot_imager(ax2, imag)
    
    fn_iono = ev.get_closest_iono(fname, PATH_IONO)
    
    iono = os.path.join(
        PATH_IONO,
        fn_iono
        )
    
    n = plot_ionogram(ax1, iono)
    
    shade(ax3, n)
    
    plot_roti_curves(ax3)
    
    
    return fig


files  = os.listdir(PATH_IMAG)

for fname in files:

    fig = plot_multianim(fname)
    
    fig.savefig(f'database/temp/{fname}')