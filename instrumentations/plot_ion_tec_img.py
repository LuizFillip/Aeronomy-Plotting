import base as b
import PlasmaBubbles as pb
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg
import GEO as gg 
import matplotlib.pyplot as plt 

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
    path_to_save = f'movies/{folder}'
    b.make_dir(path_to_save)
    name = target.strftime('%Y%m%d%H%M%S')
    
    fig.savefig(f'{path_to_save}/{name}', dpi = 100)


def title(dn):
    return dn.strftime('%Y/%m/%d %Hh%M (UT)')


def plot_ion_tec_img(
        file, 
        dn, 
        kind = 'With EPB', 
        title_dn = None):
        
    fig, ax_img, ax_ion, ax_tec   = b.layout3(
        figsize = (19, 8), 
        wspace = 0.5, 
        hspace = 0.2
        )
    
   
    
    path_of_image = os.path.join(
        im.path_all_sky(dn), file)
    
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
        root = root_tec
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
    
    if title_dn is not None:
        
        time_title = title(target)
        
    
    return fig 

root_tec = 'D:\\'

dn = dt.datetime(2014,1,2,21)

delta = dt.timedelta(hours = 8)
file = im.get_closest(
    dn + delta, 
    file_like = True
    )
figure_1 = plot_ion_tec_img(
        file, 
        dn, 
        kind = 'With EPB', 
        title_dn = None)

dn = dt.datetime(2013,6,10,21)

delta = dt.timedelta(hours = 8)
file = im.get_closest(
    dn + delta, 
    file_like = True
    )
figure_2 = plot_ion_tec_img(
        file, 
        dn, 
        kind = 'Without EPB', 
        title_dn = None)

fig = b.join_images(figure_1, figure_2)