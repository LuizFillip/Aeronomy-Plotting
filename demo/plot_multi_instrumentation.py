import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import events as ev 
import os 
import imager as im
import base as b 
import datetime as dt 
import numpy as np

def folder_date(dn):
    return dn.strftime('%Y%m%d')

def plot_imager(ax2, fname):
    
    img = io.imread(fname, as_gray = True)
    
    ax2.imshow(
        img, 
        cmap = 'gray'
        )
    
    ax2.tick_params(
        labelbottom = False, 
        labelleft = False
        )
    
    dn  = im.imager_fname(fname).datetime
    
    ax2.set(title = dn.strftime('%H:%M'))
    
    if col == 0:
        ax2.text(
            0.03, 0.85, '(a)',
            color = 'white',
            transform = ax2.transAxes)
    
    return ax2

def plot_ionogram(ax2, fname):
        
    img = io.imread(fname)
    
    ax2.imshow(dg.crop_image(
        img, 
        x = 170, 
        w = 580)
        )
    
    ax2.tick_params(
        labelbottom = False, 
        labelleft = False
        )
    
    dn = dg.ionosonde_fname(fname) 
    ax2.set(title = dn.strftime('%H:%M'))
    
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
        
        ax2.set(ylabel = 'Virtual Height (km)')

    return dn



def plot_roti(ax1, dn, out):
            
    path = f'database/epbs/vad_random/{dn.year}.txt'
    
    ds = b.sel_times(b.load(path), dn)
    
    ax1.plot(ds)
    
    ax1.set(
        yticks = np.arange(0, 5),
        ylabel = 'ROTI (TECU/min)', 
        ylim = [0, 5]
        )
    
    b.format_time_axes(ax1)
    
    for n in out:
        delta = dt.timedelta(minutes = 10)
        ax1.axvspan(
            n, n + delta,
            alpha = 0.3, 
            color = "gray"
        )
    
    ax1.text(
        0.03, 0.85, '(c)', 
        transform = ax1.transAxes
        )
    



def plot_multi_instrumentation(dn, fn_skys):

    fig = plt.figure(
        dpi = 400,
        figsize = (8, 10),
        layout = "constrained"
        )
    
    PATH_IMAG = f'imager/img/{im.folder_from_dn(dn)}/'
    PATH_IONO = f'database/iono/{folder_date(dn)}/'
    

    
    gs2 = GridSpec(3, len(fn_skys))
    
    gs2.update(hspace = 0.12,  wspace = 0)
    
    out = []
    
    for col, fn_sky in enumerate(fn_skys):
        
        imag = os.path.join(
            PATH_IMAG,
            fn_sky
            )
        
        ax1 = plt.subplot(gs2[0, col])
        
        plot_imager(ax1, imag)
        
        
        fn_iono = ev.get_closest_iono(fn_sky)
        
        iono = os.path.join(
            PATH_IONO,
            fn_iono
            )
        
        ax2 = plt.subplot(gs2[1, col])
        
    
        out.append(plot_ionogram(ax2, iono))
           
    
    ax3 = plt.subplot(gs2[-1, :])
    
    
    plot_roti(ax3, dn, out)
    
    return fig

dn = dt.datetime(2013, 1, 14, 20)


fn_skys = [
    'O6_CA_20130114_224619.png', 
    'O6_CA_20130114_231829.png',
    'O6_CA_20130114_234329.png', 
    'O6_CA_20130115_020958.png'
    ]

fig = plot_multi_instrumentation(dn, fn_skys)