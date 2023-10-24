import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import events as ev 
import os 
import imager as im
import base as b 
import datetime as dt 

def plot_imager(fname, row, col):
    
    ax2 = fig.add_subplot(gs[row, col])
    
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
    
    ax2.set(title = dn.strftime('%H:%M (UT)'))
    
    return ax2

def plot_ionogram(fname, row, col):
    
    ax2 = fig.add_subplot(gs[row, col])
    
    img = io.imread(fname, as_gray = False)
    
    ax2.imshow(dg.crop_image(img))
    
    ax2.tick_params(
        labelbottom = False, 
        labelleft = False
        )
    
    dn = dg.ionosonde_fname(fname) 
    ax2.set(title = dn.strftime('%H:%M (UT)'))

    return dn


def plot_imager_digisonde(fn_skys):
    
    out = []
    
    for i, fn_sky in enumerate(fn_skys):
                
        imag = os.path.join(
            PATH_IMAG,
            fn_sky
            )
        
        plot_imager(imag, 0, i)
        
        fn_iono = ev.get_closest_iono(fn_sky)
        
        iono = os.path.join(
            PATH_IONO,
            fn_iono
            )
        
        dn = plot_ionogram(iono, 1, i)
        
        out.append(dn)
        
    return out

def plot_roti(dn, out):
        
    ax1 = fig.add_subplot(gs[-1, :])
    
    path = f'database/epbs/vad_random/{dn.year}.txt'
    
    ds = b.sel_times(b.load(path), dn)
    
    ax1.plot(ds)
    
    ax1.set(ylabel = 'ROTI (TECU/min)', 
            ylim = [0, 5])
    
    b.format_time_axes(ax1)
    
    for n in out:
        delta = dt.timedelta(minutes = 10)
        ax1.axvspan(
            n, n + delta,
            alpha = 0.3, 
            color = "gray"
        )
    

fig = plt.figure(
    figsize = (10, 10),
    layout = "constrained"
    )

ncols = 4

gs = GridSpec(3, ncols, figure = fig)


PATH_IMAG = 'imager/img/CA_2013_0114/'
PATH_IONO = 'database/iono/20130114/'


fn_skys = [
    'O6_CA_20130114_224619.png', 
    'O6_CA_20130114_231829.png',
    'O6_CA_20130114_234329.png', 
    'O6_CA_20130115_020958.png']



out = plot_imager_digisonde(fn_skys)

dn = dt.datetime(2013, 1, 14, 20)

plot_roti(dn, out)

    
    