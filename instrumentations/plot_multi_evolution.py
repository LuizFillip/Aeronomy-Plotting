import base as b
import epbs as pb
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg
import GEO as gg 
import matplotlib.pyplot as plt 


def plot_regions(ax_tec, site):
     
     lat, lon = gg.sites['ca']['coords']
     gg.plot_circle(
             ax_tec, 
             lon, 
             lat, 
             radius = 500, 
             edgecolor = "w"
             )
     
     if site[0] == 'S':
         lat, lon = gg.sites['saa']['coords']
     else:
         lat, lon = gg.sites['fza']['coords']
         
     gg.plot_circle(
             ax_tec, 
             lon, 
             lat, 
             radius = 230, 
             edgecolor = "w"
             )
     
     return None 
     
     
def save_image(fig, target, dn):
    folder = dn.strftime('%Y%m%d')
    path_to_save = f'movies/{folder}'
    b.make_dir(path_to_save)
    name = target.strftime('%Y%m%d%H%M%S')
    
    fig.savefig(f'{path_to_save}/{name}', dpi = 100)
    
    return None 

def title(dn):
    return dn.strftime('%Y/%m/%d %Hh%M (UT)')


    
def adjust_axes_position(ax1, ax2, offset= 0.08):    
    pos1 = ax1.get_position()
    pos2 = ax2.get_position()

    ax2.set_position(
        [pos1.x0 , pos2.y0 + offset, 
         pos2.width, pos2.height]
        )
    
    return ax2
    
    
 
def plot_time_evolution(
        file, 
        dn, 
        df, 
        target = None,
        vmax = 10, 
        save = True,
        threshold = 0.20, 
        fontsize = 30, 
        root_tec = 'E:\\'
        ):

    fig, ax_img, ax_ion, ax_tec, axes = b.layout4(
        figsize = (10, 20),  #(20, 10)
        hspace = 0.4, 
        wspace = 0.3
        )
    
    path_of_image = os.path.join(
        im.path_all_sky(dn, root = root_tec), file)
 
    target = im.plot_images(
        path_of_image, 
        ax_ion, 
        time_infos = False,
        fontsize = 15
        )
    
    fig.suptitle(title(target), y = 0.94)
    
    pl.plot_tec_map(
        target, 
        ax = ax_tec, 
        vmax = vmax, 
        colorbar = True, 
        boxes = True,
        root = root_tec, 
        vertical_cbar = False
        )
    
    site, path_of_ionogram = dg.path_ionogram(dn, target)
    
    plot_regions(ax_tec, site)
    
    pl.plot_single_ionogram(
        path_of_ionogram, 
        ax = ax_img, 
        aspect = 'auto',
        label = True,
        ylabel_position = 'right',
        title = False
        )
        
    pl.plot_roti_timeseries(
        axes, 
        df, 
        target, 
        dn, 
        site,
        vmax = 3, 
        right_ticks = False,
        threshold = threshold
        )
    

    fig.text(
       0.04, 0.25, # 0.62, 0.25, # 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.93, 0.28, #0.92, 0.3,
        'OCCURRENCE', 
        fontsize = fontsize, 
        rotation = 'vertical',
        color = 'b'
        )
    
    for i in range(len(axes) -1):
        adjust_axes_position(axes[i], axes[i + 1], 
            offset = 0.02 * (i + 1))


    if save:
        save_image(fig, target, dn)
    
    return fig

def test_single(
        dn, 
        start = None, 
        vmax = 60, 
        offset = 8, 
        remove_noise = True,
        root = 'E:\\'
        ):
    
    # start = im.round_date(dn)
    
    df =  pb.concat_files(
          dn, 
          root = root, 
          remove_noise =  remove_noise
          )

    ds = b.sel_times(df, dn, hours = 12)
    
    delta = dt.timedelta(hours = offset)
    file = im.get_closest(dn + delta, file_like = True)

    plot_time_evolution(
        file, 
        dn, 
        ds, 
        vmax = vmax
        )
    
    plt.show()
    
    return None 
    

# dn =  dt.datetime(2014, 2, 9, 20)
# dn = dt.datetime(2013, 12, 24, 20)

# test_single(
#     dn, 
#     start = None, 
#     vmax = 60, 
#     offset = 7, 
#     remove_noise = True
#     )


