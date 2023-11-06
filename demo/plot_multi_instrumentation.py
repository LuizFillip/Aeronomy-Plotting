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

def plot_imager(ax2, fname, col):
    
    img = io.imread(fname, as_gray = True)
    
    ax2.imshow(
        img, 
        cmap = 'gray'
        )
       
    ax2.set_axis_off()
    
    dn = im.imager_fname(fname).datetime
    title = dn.strftime(f'({col + 1}) %H:%M')
    ax2.set(title = title)
    
    if col == 0:
        ax2.text(
            0.03, 0.85, '(a)',
            color = 'white',
            transform = ax2.transAxes
            )
    
    return ax2

def plot_ionogram(ax2, fname, col):
        
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
    
    title = dn.strftime(f'({col + 1}) %H:%M')
    
    ax2.set(title = title)
    
    if col == 1:
        ax2.text(0.6, -0.1, 'Frequency (MHz)',
        transform = ax2.transAxes
        )
    
    if col == 0:
        ax2.text(
            0.03, 0.85, '(b)',
            color = 'white',
            transform = ax2.transAxes
            )
        
        ax2.set(
            ylabel = 'Virtual Height (km)'
            )

    return dn




def plot_roti(ax1, dn, times):
    
    delta = dt.timedelta(minutes = 10)
    
   
                
    plot_roti_curves(ax1, dn)
    
    b.format_time_axes(ax1)
    
    
    
    for i, n in enumerate(times):
        
        # ax1.text(
        #     n, 4, i + 1, 
        #     transform = ax1.transData
        #     )
        
        ax1.axvspan(
            n, n + delta,
            alpha = 0.7, 
            color = 'gray',
            edgecolor = 'k', 
            lw = 2
        )
    
    ax1.text(
        0.02, 0.85, '(b)', 
        transform = ax1.transAxes
        )
    
def plot_multi_instrumentation(dn, fn_skys):

    fig = plt.figure(
        dpi = 400,
        figsize = (12, 8),
        layout = "constrained"
        )
    
    PATH_IMAG = f'imager/img/{im.folder_from_dn(dn)}/'
    PATH_IONO = f'digisonde/data/ionogram/{folder_date(dn)}S/'

    gs2 = GridSpec(2, len(fn_skys))
    
    gs2.update(
        hspace = 0,  
        wspace = 0
        )
    
    out = []
    
    for col, fn_sky in enumerate(fn_skys):
        
        imag = os.path.join(
            PATH_IMAG,
            fn_sky
            )
        
        ax1 = plt.subplot(gs2[0, col])
        
        plot_imager(ax1, imag, col)
        

        # fn_iono = ev.get_closest_iono(fn_sky, PATH_IONO)
        
        # iono = os.path.join(
        #     PATH_IONO,
        #     fn_iono
        #     )
        
        # ax2 = plt.subplot(gs2[1, col])
        
        # out.append(plot_ionogram(ax2, iono, col))
        out.append( im.fn2datetime(fn_sky))
    
    ax3 = plt.subplot(gs2[-1, :])
    
    
    plot_roti(ax3, dn, out)
    
    return fig

dn = dt.datetime(2013, 6, 10, 20)


fn_skys = [ 
    'O6_CA_20130610_220827.png',
    'O6_CA_20130610_225828.png', 
    'O6_CA_20130611_001329.png', 
    'O6_CA_20130611_014955.png'
    ]

dn = dt.datetime(2013, 1, 14, 20)

fn_skys = [
    'O6_CA_20130114_224619.png', 
    'O6_CA_20130114_231829.png',
    'O6_CA_20130114_234329.png', 
    'O6_CA_20130115_020958.png']

fig = plot_multi_instrumentation(dn, fn_skys)

# fig.savefig(b.LATEX('non_EPB_occurrence'), dpi = 400)
# 

