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
            dn
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
    
    
    ax.axvline(dusk, lw = 2.5, linestyle = '--')
    ax.text(
        dusk, 
        1.02, 
        'Terminator', 
        transform = ax.transData
        )
    ax.plot(ds[str(glon)], **args)
    
    ax.set(
        ylim = [0, 1], 
        ylabel = 'ROTI (TECU/min)'
        )
    
    b.format_time_axes(ax, hour_locator = 1)
    
    return None
    
    

def plot_imager(ax, fname):
    
    ax.imshow(
        io.imread(fname, as_gray = True), 
        cmap = 'gray'
        )
       
    ax.set_axis_off()

    return ax

def plot_shade_bars(ax, times, ytext = 0.85):

    delta = dt.timedelta(minutes = 12)
    
    for index, time in enumerate(times):
        
        ax.text(
            time, 
            ytext, 
            index + 1, 
            transform = ax.transData
            )
        
        ax.axvspan(
            time, 
            time + delta,
            alpha = 0.7, 
            color = 'gray',
            edgecolor = 'k', 
            lw = 2
        )
        
    return None


def plot_image_in_sequence(gs2, path_images):

    times = []

    for col, file in enumerate(path_images):
        
        fn = os.path.split(file)[-1]
        
        dn = im.imager_fname(fn).datetime
        times.append(dn)
        title = dn.strftime(f'({col + 1}) %H:%M')
        
        
        if col <= 1:
            ax1 = plt.subplot(gs2[0, col + 2])
            x, y = (.3, 1.05)
            
        elif col == 3:
            ax1 = plt.subplot(gs2[1, 2])
            x, y = (.3, -0.12)

        else:
            ax1 = plt.subplot(gs2[1, 3])
            x, y = (.3, -0.12)
        
       
        ax = plot_imager(ax1, file)
        
        ax.text(
            x, y, title, 
            transform = ax.transAxes
                       )
    return times



def plot_roti_and_images(
        dn,
        path_images, 
        fontsize = 30
        ):

    fig = plt.figure(
        dpi = 300,
        figsize = (16, 8),
        layout = 'compressed'
        )
        
    gs2 = GridSpec(2, 4)
    
    gs2.update(hspace = 0, wspace = 0.0)
        
    times = plot_image_in_sequence(gs2, path_images)
    
    ax2 = plt.subplot(gs2[:2, :2])
    
    plot_roti(ax2, dn)
    
    plot_shade_bars(ax2, times, ytext = 0.85)
    
    ax2.text(0, 1, '(a)', 
             fontsize = fontsize,
             transform = ax2.transAxes)
    
    ax2.text(1.0, 1, '(b)', 
             fontsize = fontsize,
             transform = ax2.transAxes)
   
    return fig 

path_images = [ 
    'database/CA_2017_0403P/O6_CA_20170404_022551.png',
    'database/CA_2017_0403P/O6_CA_20170404_030245.png',
    'database/CA_2017_0403P/O6_CA_20170404_061121.png',
    'database/CA_2017_0403P/O6_CA_20170404_040009.png'
    
    ]

dn = dt.datetime(2017, 4, 3, 20)
fig = plot_roti_and_images(dn, path_images)

save_in = 'G:\\Meu Drive\\Doutorado\Travels\\O6_CA_20170404'

fig.savefig(save_in, dpi = 300)