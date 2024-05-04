import base as b
import PlasmaBubbles as pb
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg
import GEO as gg 
 
def plot_regions(ax_tec, site):
     
     lat, lon = gg.sites['car']['coords']
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
def save_image(fig, target, dn):
    folder = dn.strftime('%Y%m%d')

    name = target.strftime('%Y%m%d%H%M%S')
    
    fig.savefig(f'movies/{folder}/{name}', dpi = 100)


def title(dn):
    return dn.strftime('%Y/%m/%d %Hh%M (UT)')


def plot_time_evolution(
        file, 
        dn, 
        df, 
        target = None,
        vmax = 10, 
        site = 'SAA0K',
        save = True,
        threshold = 0.20, 
        fontsize = 30, 
        root_tec = 'D:\\'
        ):

    fig, ax_img, ax_ion, ax_tec, axes = b.layout4(
        figsize = (12, 20), 
        hspace = 0.3, 
        wspace = 0.3
        )
    
      
    path_of_image = os.path.join(im.path_all_sky(dn), file)
 
    target = im.plot_images(
        path_of_image, 
        ax_ion, 
        time_infos = False,
        fontsize = 15
        )
    
    fig.suptitle(title(target), y = 0.95)

    pl.plot_tec_map(
        target, 
        ax = ax_tec, 
        vmax = vmax, 
        colorbar = True, 
        boxes = True,
        site = site, 
        root = root_tec
        )
   
    plot_regions(ax_tec, site)
    
    site, path_of_ionogram = dg.path_ionogram(dn, target)
    
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
        vmax = 3, 
        right_ticks = False,
        threshold = threshold
        )
    

    fig.text(
        0.03, 0.23, 'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.95, 0.26, 'Occurrence', 
        fontsize = fontsize, 
        rotation = 'vertical',
        color = 'b'
        )

    
    if save:
        save_image(fig, target, dn)
    
    return fig

def test_single(
        dn, 
        start = None, 
        vmax = 60, 
        offset = 8, 
        remove_noise = True
        ):
    
    start = im.round_date(dn)
    
    df =  pb.concat_files(
          start, 
          root = 'D:\\', 
          remove_noise =  remove_noise
          )
    
    
    ds = b.sel_times(df, start, hours = 12)
    
    de = dt.timedelta(hours = 8)
    file = im.get_closest(
        dn + de, 
        file_like = True, 
        ext = '.tif'
        )

    plot_time_evolution(file, start, ds, vmax = vmax)
        
    
dn = dt.datetime(2017, 8, 30, 21)

test_single(dn, start = None, vmax = 6, remove_noise = True)