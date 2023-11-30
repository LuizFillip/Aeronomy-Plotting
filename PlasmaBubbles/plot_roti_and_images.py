import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import os 
import imager as im
import base as b 
import datetime as dt 
import GEO as gg


def plot_roti(ax, dn, glon = -50):
    
    infile = f'database/epbs/longs/{dn.year}.txt'

    ds = b.sel_times(
            b.load(infile),
            dn, 
        )
    
    args = dict(
        marker = 'o', 
        markersize = 3,
        linestyle = 'none'
        )
    
    dusk = gg.dusk_time(
            dn,  
            lat = -5, 
            lon = glon, 
            twilight = 18
            )
    
    delta = dt.timedelta(hours = 1.8)
    
    ax.axvline(dusk, lw = 2)
    ax.text(
        dusk - delta, 0.9, 
        'Terminator', 
        transform = ax.transData
        )
    ax.plot(ds[str(glon)], **args)
    
    ax.set(
        ylim = [0, 1], 
        ylabel = 'ROTI (TECU/min)'
        )
    
    b.format_time_axes(ax)
    
    

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
    
    return ax2

def plot_shade_bars(ax2, times, ytext = 0.85):

    delta = dt.timedelta(minutes = 10)
    
    for index, dn in enumerate(times):
        
        ax2.text(
            dn, 
            ytext, 
            index + 1, 
            transform = ax2.transData
            )
        
        ax2.axvspan(
            dn, 
            dn + delta,
            alpha = 0.7, 
            color = 'gray',
            edgecolor = 'k', 
            lw = 2
        )

def plot_image_in_sequence(gs2, fn_skys):

    times = []

    for col, file in enumerate(fn_skys):
        
        
        ax1 = plt.subplot(gs2[0, col])
        
        plot_imager(ax1, file, col)
        fn = os.path.split(file)[-1]
        times.append(im.fn2datetime(fn))
        
    return ax1, times

fn_skys = [ 
    'database/CA_2017_0403P/O6_CA_20170404_022551.png',
    'database/CA_2017_0403P/O6_CA_20170404_030245.png', 
    'database/CA_2017_0403P/O6_CA_20170404_040009.png',
    'database/CA_2017_0403P/O6_CA_20170404_061121.png'
    ]


def plot_roti_and_images():


    fig = plt.figure(
        dpi = 300,
        figsize = (12, 8),
        layout = "constrained"
        )
        
    gs2 = GridSpec(2, 4)
    
    gs2.update(
        hspace = 0,  
        wspace = 0
        )
        
    
    times = plot_image_in_sequence(gs2, fn_skys)
    
    ax2 = plt.subplot(gs2[-1, :])
    
    plot_shade_bars(ax2, times, ytext = 0.85)
    
    dn = dt.datetime(2017, 4, 3, 20)
    
    plot_roti(ax2, dn)
    
    
    return fig 



