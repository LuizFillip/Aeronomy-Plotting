import base as b
from tqdm import tqdm 
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
     
     
def save_image(fig, target, dn):
    folder = dn.strftime('%Y%m%d')
    path_to_save = f'movies/{folder}'
    b.make_dir(path_to_save)
    name = target.strftime('%Y%m%d%H%M%S')
    
    fig.savefig(f'{path_to_save}/{name}', dpi = 100)


def title(dn):
    delta = dt.timedelta(hours = 3)
    dn -= delta
    return dn.strftime('%Y/%m/%d %Hh%M (LT)')


def plot_ion_tec_img(
        file, 
        dn, 
        kind = 'With EPB', 
        title_dn = None, 
        root = 'E:\\'
        ):
        
    fig, ax_img, ax_ion, ax_tec   = b.layout3(
        figsize = (19, 8), 
        wspace = 0.5, 
        hspace = 0.2
        )
    
   
    
    path_of_image = os.path.join(
        im.path_all_sky(dn, root = root), file)
    
    target = im.plot_images(
        path_of_image, 
        ax_ion, 
        time_infos = False,
        fontsize = 15
        )
    

    fig.suptitle(kind, y = 0.89)
    
    pl.plot_tec_map(
        target, 
        ax = ax_tec, 
        vmax = 60, 
        colorbar = True, 
        boxes = True,
        root = root
        )
    
    site, path_of_ionogram = dg.path_ionogram(
        dn, target, root = root)
    
    plot_regions(ax_tec, site)
    
    pl.plot_single_ionogram(
        path_of_ionogram, 
        ax = ax_img, 
        aspect = 'auto',
        label = True,
        ylabel_position = 'right',
        title = False
        )
    
    if title_dn is not None:
        
        time_title = title(target)
        
        fig.suptitle(time_title, y = 0.92)
    
    return fig 


with_epb = dt.datetime(2014, 1, 2, 21)
without_epb = dt.datetime(2014, 6, 21, 21)



def plot_with_and_without_epb(
        with_epb, 
        without_epb, 
        delta
        ):
    
    file = im.get_closest(
        with_epb + delta, 
        file_like = True
        )
    figure_1 = plot_ion_tec_img(
            file, 
            with_epb, 
            kind = 'With EPB', 
            title_dn = True)
    
    
    file = im.get_closest(
        without_epb + delta, 
        file_like = True
        )
    figure_2 = plot_ion_tec_img(
            file, 
            without_epb, 
            kind = 'Without EPB', 
            title_dn = True)
    
    fig = b.join_images(figure_1, figure_2)
    
    dn = with_epb + delta
    
    fn = dn.strftime('%Y%m%d%H%M%S')
    fig.savefig('temp/' + fn)
    return fig

def run():
    for minute in tqdm(range(0, 12 * 60, 2)):
        
        delta = dt.timedelta(minutes = minute)
        
        plt.ioff()
    
        fig = plot_with_and_without_epb(
                with_epb, 
                without_epb, 
                delta
                )
        
        plt.clf()   
        plt.close()   
