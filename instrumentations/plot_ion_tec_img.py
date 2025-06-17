import base as b
from tqdm import tqdm 
import plotting as pl 
import datetime as dt
import imager as im 
import digisonde as dg
import GEO as gg 

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


def title(dn, kind):
    delta = dt.timedelta(hours = 3)
    dn -= delta
    return dn.strftime(f'{kind} - %Y/%m/%d %Hh%M (LT)')

def plot_imager(path_sky: str, ax) -> dt.datetime:
    """Plota imagem All-Sky processada em um eixo."""
    
    image = im.DisplayASI(path_sky)
    
    image.display_original(ax)

    return  image.dn

def plot_ion_tec_img(
        dn, 
        site,
        vtec = 30,
        kind = 'With EPB', 
        title_dn = None, 
        root = 'E:\\'
        ):
        
    fig, ax_img, ax_ion, ax_tec  = b.layout3(
        figsize = (19, 8), 
        wspace = 0.5, 
        hspace = 0.2
        )
  
    path_of_image = im.path_from_closest_dn(
            dn, 
            site = 'CA', 
            layer = 'O6', 
            file_like = True
            )
    
    target = plot_imager(
        path_of_image, 
        ax_ion
        )
    

    fig.suptitle(kind, y = 0.89)
    
    pl.plot_tec_map(
        target, 
        ax = ax_tec, 
        vmax = vtec, 
        colorbar = True, 
        boxes = False,
        root = root,
        vertical_cbar = False
        )
    
    dn1, path_of_ionogram = dg.iono_path_from_target(
        target, site)
    
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
        
        time_title = title(target, kind)
        
        fig.suptitle(
            time_title, 
            y = 0.90, 
            fontsize = 40)
    
    return fig 


import matplotlib.pyplot as plt 

start = dt.datetime(2017, 9, 17, 21)

site = 'FZA0M'
site = 'SAA0K'
# fig = plot_ion_tec_img(
#         dn, 
#         site,
#         kind = '', 
#         title_dn = dn, 
#         root = 'E:\\'
#         )

for minute in tqdm(range(2 * 60, 12 * 60, 2)):
    
    delta = dt.timedelta(minutes = minute)
    
    dn = start + delta
    
    plt.ioff()

    fig = plot_ion_tec_img(
            dn, 
            site,
            kind = '', 
            title_dn = dn, 
            root = 'E:\\'
            )
    
    fn = dn.strftime('%Y%m%d%H%M%S')
    fig.savefig('temp/' + fn)
    
    
    plt.clf()   
    plt.close()   
