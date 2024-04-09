import base as b
import PlasmaBubbles as pb
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg
import matplotlib.pyplot as plt
from tqdm import tqdm 
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
    
    fig.savefig(f'movies/{folder}/{name}')


def title(dn):
    return dn.strftime('%Y/%m/%d %Hh%M (UT)')


def plot_time_evolution(
        file, 
        dn, 
        df, 
        target = None,
        vmax = 10, 
        site = 'SAA0K',
        save = False,
        threshold = 0.2
        ):

    fig, ax_img, ax_ion, ax_tec, axes = b.layout4(
        figsize = (12, 20), 
        hspace = 0.3, 
        wspace = 0.3
        )
    
      
    path_of_image = os.path.join(im.path_all_sky(dn), file)
    
    if dn.year <= 2019:
        flip = False
    else:
        flip = True
        
    target = im.plot_images(path_of_image, ax_ion, flip = flip)
    
    fig.suptitle(title(target), y = 0.95)

        
    pl.plot_tec_map(
        target, 
        ax = ax_tec, 
        vmax = vmax, 
        colorbar = True, 
        boxes = True,
        site = site
        )
   
    
    plot_regions(ax_tec, site)
    
    site, path_of_ionogram = dg.path_ionogram(dn, target)
    
    pl.plot_single_ionogram(
        path_of_ionogram, 
        ax = ax_img, 
        aspect = 'auto',
        label = True
        )
        
    pl.plot_roti_timeseries(
        axes, 
        df, 
        target, 
        dn, 
        vmax = 3, 
        right_ticks = False,
        threshold = 0.25
        )
    
    fontsize = 30
    
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



def run(dn, save = True, vmax = 10):
        
    df =  pb.concat_files(
          dn, 
          root = 'D:\\', 
          remove_noise = False
          )
    
    date_name = dn.strftime('%Y%m%d')
    b.make_dir(f'movies/{date_name}')
    

    files = os.listdir(im.path_all_sky(dn)) 
    
    for file in tqdm(files, date_name):
    
        plt.ioff()
        plot_time_evolution(
            file, dn, df, vmax = vmax, save = save)
        
       
        plt.clf()   
        plt.close()   
 


def test_single(dn,  vmax = 25):
    
    start = im.round_date(dn)
    
    df =  pb.concat_files(
          start, 
          root = 'D:\\', 
          remove_noise = False
          )
    file = im.get_closest(dn, file_like = True)
    
    ds = b.sel_times(df, start, hours = 11)
    
    plot_time_evolution(file, start, ds, vmax = vmax)
    
    plt.show()

    


# dn = dt.datetime(2013, 12, 24, 21)
# dn = dt.datetime(2013, 1, 14, 21)
# dn = dt.datetime(2016, 2, 11, 21)
# dn = dt.datetime(2016, 5, 27, 21)
# dn = dt.datetime(2016, 10, 3, 21)
# dn = dt.datetime(2017, 9, 17, 21)
# dn = dt.datetime(2019, 2, 24, 21)
# dn = dt.datetime(2019, 5, 2, 21)
# dn = dt.datetime(2019, 9, 6, 21)
# dn = dt.datetime(2018, 3, 19, 21)

# dn = dt.datetime(2020, 3, 30, 21)
# dn = dt.datetime(2020, 8, 20, 21)


def main(dn, vmax = 40, site = 'CA'):
    
    run(dn, vmax = vmax)
    
    folder_in = dn.strftime('%Y%m%d')
    
    b.images_to_gif(
        name =  folder_in, 
        path_out = 'movies',
        path_in = f'movies/{folder_in}/', 
        fps = 20
        )

dates = [dt.datetime(2016, 2, 11, 21), 
         dt.datetime(2016, 5, 27, 21), 
         dt.datetime(2016, 10, 3, 21),
         dt.datetime(2017, 9, 17, 21), 
         dt.datetime(2019, 2, 24, 21), 
         dt.datetime(2019, 5, 2, 21), 
         dt.datetime(2019, 9, 6, 21), 
         dt.datetime(2018, 3, 19, 21),
         dt.datetime(2020, 3, 30, 21),
         dt.datetime(2020, 8, 20, 21)
]

for dn in dates:
    run(dn, vmax = 12)
