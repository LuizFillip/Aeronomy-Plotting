import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import os 
import imager as im
import base as b 
import datetime as dt 
import PlasmaBubbles as pb 


def get_datetime_from_file(fn):
    date_obj = im.fn2datetime(fn).date() 
    time_obj = dt.time(20, 0)
    
    return dt.datetime.combine(date_obj, time_obj)
    

def folder_date(dn):
    return dn.strftime('%Y%m%d')

def plot_imager(ax_img, PATH_SKY, file, index):
    
    
    AllSky = im.processing_img(
        os.path.join(PATH_SKY, file)
        )
    
    new_img= AllSky.bright
    
    AllSky.display(ax_img, new_img)
    dn = im.fn2datetime(file)
    title = dn.strftime(f'({index}) %Hh%M')
    ax_img.set(title = title)
    
    return dn 

def plot_ionogram(ax2, target, col, site, PATH_IONO):
    
    dn = closest_iono(PATH_IONO, target)
    file = dn.strftime(f'{site}_%Y%m%d(%j)%H%M%S.PNG')
            
    img = io.imread(os.path.join(PATH_IONO, file))
    
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
    
    
    title = dn.strftime(f'({col + 1}) %H:%M')
    
    ax2.set(title = title)
    
    if col == 1:
        ax2.text(0.6, -0.1, 'Frequency (MHz)',
        transform = ax2.transAxes
        )
    
    if col == 0:
        ax2.set(ylabel = 'Virtual Height (km)')

    return dn



args = dict(
     marker = 'o', 
     markersize = 5,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.7, 
     )



def plot_roti_curves(ax, dn):
    
    ds = pb.concat_files(dn, root = os.getcwd())

    ds = b.sel_times(ds, dn)
    
    # ds = ds.loc[(ds['lon'] > -50) & 
    #             (ds['lon'] < -40) &
    #             (ds['lat'] > -5) & 
    #             (ds['lat'] < -1 )]
    
    # ds = ds[~ds['prn'].str.contains('R')]
        
    ax.plot(ds['roti'], **args, 
            label = 'ROTI points')
    
    times = pb.time_range(ds)
    
    
    df1 = pb.maximum_in_time_window(ds, 'max', times)
    
    ax.plot(df1, 
            color = 'k',
            marker = 'o', 
            markersize = 5, 
            linestyle = 'none',
            label = 'Maximum value')
    
    ax.axhline(0.25, color = 'red', lw = 2, 
                label = '0.25 TECU/min')
    
    
    ax.set(yticks = list(range(0, 7)), 
           ylabel = 'ROTI (TECU/min)', 
           xlim = [df1.index[0], df1.index[-1]])
    ax.legend(loc = 'upper right')
    
    b.format_time_axes(ax)
    
    
def plot_shades(ax1, n, index):
    
    delta = dt.timedelta(minutes = 10)
    
    ax1.text(
        n, 5.5, index, 
        transform = ax1.transData
        )
    
    ax1.axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
    
def closest_iono(PATH_IONO, target):
    iono_times = [
        dg.ionosonde_fname(f) for f in os.listdir(PATH_IONO) 
                  if 'PNG' in f ]
    
    dn = b.closest_datetime(iono_times, target)
    
    return dn
  
    
def plot_multi_instrumentation(fn_skys):
    
    dn = get_datetime_from_file(fn_skys[0])

    fig = plt.figure(
        dpi = 300,
        figsize = (12, 12),
        layout = "constrained"
        )
    # site =  'FZA0M'
    site =  'SAA0K'
    folder_img = dn.strftime('CA_%Y_%m%d')
    folder_ion = dn.strftime('%Y%m%d')
    PATH_SKY = f'database/images/{folder_img}/'
    PATH_IONO = f'database/ionogram/{folder_ion}{site[0]}/'


    gs2 = GridSpec(3, len(fn_skys))
    
    gs2.update(hspace = 0.2, wspace = 0)
        
    ax3 = plt.subplot(gs2[-1, :])

    plot_roti_curves(ax3, dn)
    
    for col, fn_sky in enumerate(fn_skys):
                
        ax1 = plt.subplot(gs2[0, col])
        
        target = plot_imager(ax1, PATH_SKY, fn_sky, col + 1)
        
        ax2 = plt.subplot(gs2[1, col])
        
        dn1 = plot_ionogram(ax2, target, col, site, PATH_IONO)
        
        plot_shades(ax3, dn1, col + 1)
    
    
    
    
    return fig

FigureName = 'non_EPB_occurrence'
fn_skys = [ 
    'O6_CA_20130610_220827.tif',
    'O6_CA_20130610_225828.tif', 
    'O6_CA_20130611_001329.tif', 
    'O6_CA_20130611_014955.tif'
    ]

# FigureName = 'EPB_occurrence'

# fn_skys = [
#     'O6_CA_20130114_224619.tif', 
#     'O6_CA_20130114_231829.tif',
#     'O6_CA_20130114_234329.tif', 
#     'O6_CA_20130115_020958.tif']




fig = plot_multi_instrumentation(fn_skys) 



fig.savefig(
    b.LATEX(FigureName, 
    folder = 'modeling'), dpi = 400)
# 


