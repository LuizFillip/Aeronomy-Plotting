import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import events as ev 
import os 
import imager as im
import base as b 
import datetime as dt 

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
    
    ax2.set(title = dn.strftime('%H:%M (UT)'))
    
    if col == 0:
        ax2.text(0.01, 1.2, '(a)',
             transform = ax2.transAxes)
    
    return ax2

def plot_ionogram(ax2, fname):
        
    img = io.imread(fname, as_gray = False)
    
    ax2.imshow(dg.crop_image(img))
    
    ax2.tick_params(
        labelbottom = False, 
        labelleft = False
        )
    
    dn = dg.ionosonde_fname(fname) 
    ax2.set(title = dn.strftime('%H:%M (UT)'))
    
    if col == 0:
        ax2.text(0.01, 1.2, '(b)',
         transform = ax2.transAxes)

    return dn



def plot_roti(ax1, dn, out):
            
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
    
    ax1.text(0.02, 0.85, '(c)', 
             transform = ax1.transAxes)
    

fig = plt.figure(
    figsize = (10, 10),
    layout = "constrained"
    )

ncols = 4


PATH_IMAG = 'imager/img/CA_2013_0114/'
PATH_IONO = 'database/iono/20130114/'


fn_skys = [
    'O6_CA_20130114_224619.png', 
    'O6_CA_20130114_231829.png',
    'O6_CA_20130114_234329.png', 
    'O6_CA_20130115_020958.png']




dn = dt.datetime(2013, 1, 14, 20)


gs2 = GridSpec(3, ncols)

gs2.update(hspace=0.2,  wspace = 0.)

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