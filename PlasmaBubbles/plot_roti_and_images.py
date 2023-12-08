import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import os 
import imager as im
import base as b 
import datetime as dt 
import GEO as gg

b.config_labels(fontsize = 20)


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
    
    b.format_time_axes(ax,pad = 50, hour_locator = 2)
    
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
            ax1 = plt.subplot(gs2[0, col])
            x, y = (.1, 1.05)
        
        else:
            ax1 = plt.subplot(gs2[1, col - 2])
            x, y = (.1, -0.16)

        ax = plot_imager(ax1, file)
        
        ax.text(
            x, y, 
            title, 
            transform = ax.transAxes
            )
        
        if col == 0:
            ax.text(
                0, 1.4, '(a)', 
                fontsize = 25,
                transform = ax.transAxes
                )
    return times



def plot_roti_and_images(
        dn,
        path_images, 
        fontsize = 25
        ):

    fig = plt.figure(
        dpi = 300,
        figsize = (12, 4),
        layout = 'constrained'
        )
        
    gs2 = GridSpec(2, 5)
    
    gs2.update(hspace = 0, wspace = 0)
        
    times = plot_image_in_sequence(gs2, path_images)
    
    ax2 = plt.subplot(gs2[:, 2:])
    
    plot_roti(ax2, dn)
    
    plot_shade_bars(ax2, times, ytext = 0.85)
    
    
    ax2.text(
        0.01, 1.2, '(b)', 
        fontsize = fontsize,
        transform = ax2.transAxes
        )
    
    ax2.tick_params(
        axis='y', 
        labelright = True, 
        labelleft = False, 
        right = True, 
        left = False)
    
    ax2.yaxis.set_label_position("right")
   
    return fig 


def main():
    
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