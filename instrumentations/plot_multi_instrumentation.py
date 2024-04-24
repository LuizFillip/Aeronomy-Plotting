import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import os 
import imager as im
import base as b 
import datetime as dt 
import PlasmaBubbles as pb 

b.config_labels(fontsize = 35)

def get_datetime_from_file(fn):
    date_obj = im.fn2datetime(fn).date() 
    time_obj = dt.time(20, 0)
    
    return dt.datetime.combine(date_obj, time_obj)
    

def folder_date(dn):
    return dn.strftime('%Y%m%d')

def plot_imager(ax_img, PATH_SKY, file, index):
    
    
    all_sky = im.processing_img(
        os.path.join(PATH_SKY, file)
        )
    
    new_img = all_sky.bright()
    
    all_sky.display(ax_img, new_img)
    dn = im.fn2datetime(file)
    title = dn.strftime(f'({index}) %Hh%M')
    ax_img.set(title = title)
    
    return dn 

def plot_ionogram(ax2, PATH_IONO, target, col, site):
    
    
    file = target.strftime(f'{site}_%Y%m%d(%j)%H%M%S.PNG')
            
    img = io.imread(os.path.join(PATH_IONO, file))
    
    # if target.month == 6:
        
    #     y, h = 80, 450
    #     x, w = 170, 450
    # else:
        
    y, h = 300, 560
    x, w = 188, 559
    
    img = img[y: y + h, x: x + w]
   
    ax2.imshow(img)
    
    ax2.tick_params(
        labelbottom = False, 
        labelleft = False
        )
    
    title = target.strftime(f'({col + 1}) %Hh%M')
    
    ax2.set(title = title)
    
    if col == 1:
        ax2.text(0.6, -0.2, 'Frequency (MHz)',
        transform = ax2.transAxes
        )
    
    if col == 0:
        ax2.set(ylabel = 'Virtual Height (km)')

def plot_legend(
        ax, 
        fontsize = 30, 
        s = 100, 
        threshold = 0.25
        ):
    
    l1 = plt.scatter(
        [], [], 
        color = 'gray', 
        marker = 'o', 
        s = s
        )
    
    l2 = plt.scatter(
        [], [], 
        color = 'black', 
        marker = 'o', 
        s = s
        )
    
    l3 = ax.axhline(
        threshold, 
        color = 'red', 
        lw = 2
        )
    

    labels = [
        'ROTI points',
        'Maximum value', 
        f'{threshold} TECU/min'
        ]

    plt.legend(
        [l1, l2, l3], 
        labels, 
        ncol = 1, 
        fontsize = fontsize,
        bbox_to_anchor = (1.07, 1.2),
        handlelength = 2,
        loc = 'upper right',
        borderpad = 1.8,
        handletextpad = 1, 
        scatterpoints = 1
        )

    
def plot_roti_curves(ax, dn):
    
    ds = pb.concat_files(dn, root = 'D:\\') #os.getcwd()

    ds = b.sel_times(ds, dn)
    
    # ds = ds.loc[(ds['lon'] > -50) & 
    #             (ds['lon'] < -40) &
    #             (ds['lat'] > -5) & 
    #             (ds['lat'] < -1 )]
    
    # ds = ds[~ds['prn'].str.contains('R')]
        
    ax.plot(
        ds['roti'], 
        marker = 'o', 
        markersize = 1,
        linestyle = 'none', 
        color = 'gray', 
        alpha = 0.3)
    
    times = pb.time_range(ds)

    df1 = pb.maximum_in_time_window(ds, 'max', times)
    
    ax.plot(
        df1, 
        color = 'k',
        marker = 'o', 
        markersize = 5, 
        linestyle = 'none'
        )

    
    ax.set(
        ylim = [0, 5], 
        yticks = range(0, 6, 1),
        ylabel = 'ROTI (TECU/min)', 
        xlim = [df1.index[0], df1.index[-1]]
        )
 
    plot_legend(ax, fontsize = 25)
    
    b.format_time_axes(ax, pad = 80)
    
    return None
    
    
def plot_shades(ax1, n, index, y = 4.5):
    
    delta = dt.timedelta(minutes = 10)
    
    ax1.text(
        n, y, index, 
        transform = ax1.transData
        )
    
    ax1.axvspan(
        n, n + delta,
        alpha = 0.5, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
    
def closest_iono(PATH_IONO, target):
    iono_times = [
        dg.ionosonde_fname(f) 
        for f in os.listdir(PATH_IONO) if 'PNG' in f ]
    
    dn = b.closest_datetime(iono_times, target)
    
    return dn
  
    
def plot_multi_instrumentation(
        images_files, 
        site =  'SAA0K', 
        letter = 'a'
        ):
    
    dn = get_datetime_from_file(images_files[0])

    fig = plt.figure(
        dpi = 300,
        figsize = (12, 16),
        layout = "constrained"
        )

    
    fig.text( 0.07, 0.9, f'({letter})', fontsize = 45)
    
    folder_img = dn.strftime('CA_%Y_%m%d')
    folder_ion = dn.strftime('%Y%m%d')
    PATH_SKY = f'database/images/{folder_img}/'
    PATH_IONO = f'database/ionogram/{folder_ion}{site[0]}/'


    gs2 = GridSpec(3, len(images_files))
    
    gs2.update(hspace = 0.1, wspace = 0)
        
    ax3 = plt.subplot(gs2[-1, :])

    plot_roti_curves(ax3, dn)
    
    for col, fn_sky in enumerate(images_files):
                
        ax1 = plt.subplot(gs2[0, col])
        
        time_imager = plot_imager(ax1, PATH_SKY, fn_sky, col + 1)
        
        ax2 = plt.subplot(gs2[1, col])
        
        target = closest_iono(PATH_IONO, time_imager)
        
        plot_ionogram(ax2, PATH_IONO, target, col, site)
        
        plot_shades(ax3, target, col + 1)
     
    return fig

non_epbs = [ 
    'O6_CA_20130610_220827.tif',
    'O6_CA_20130610_225828.tif', 
    'O6_CA_20130611_001329.tif', 
    'O6_CA_20130611_014955.tif'
    ]

with_epbs = [
    'O6_CA_20130114_224619.tif', 
    'O6_CA_20130114_231829.tif',
    'O6_CA_20130114_234329.tif', 
    'O6_CA_20130115_020958.tif'
    ]


# with_epbs = [
#     # 'O6_CA_20131224_222810.tif', 
#     'O6_CA_20131224_231957.tif',
#     'O6_CA_20131225_011602.tif',
#     'O6_CA_20131225_021645.tif',
#     'O6_CA_20131225_024146.tif'
#     ]

def main():

    figure_1  = plot_multi_instrumentation(with_epbs) 
    figure_2  = plot_multi_instrumentation(non_epbs, letter = 'b') 
    
    fig = b.join_images(figure_1, figure_2)
    
    FigureName = 'validation_roti_paper'
    
    
    
    fig.savefig(
        b.LATEX(FigureName, 
        folder = 'products'),
        dpi = 400)
    
main()