import base as b
import PlasmaBubbles as pb
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg
import matplotlib.pyplot as plt
from tqdm import tqdm 

def save_image(fig, target, dn):
    folder = dn.strftime('%Y%m%d')

    name = target.strftime('%Y%m%d%H%M%S')
    
    fig.savefig(f'movies/{folder}/{name}')


def title(dn):
    return dn.strftime('%Y/%m/%d %Hh%M (UT)')

def update_vmax(dn):
    d = dn.hour

    if (d >= 0) and (d <= 3):
        vmax = 10
    
    elif (d > 3) and (d <= 8): 
        vmax = 5
        
    else:
        vmax = 30
        
    return vmax 

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
        figsize = (12, 15), 
        hspace = 0.1, 
        wspace = 0.3
        )
    
      
    path_of_image = os.path.join(
        im.path_all_sky(dn), file
        )
    
    target = im.plot_images(
        path_of_image, ax_img,
        flip = False)
    
    fig.suptitle(title(target), y = 1.0)
    
    if vmax is None:
        vmax = update_vmax(target)
        
        
    pl.plot_tec_map(
        target, 
        ax = ax_tec, 
        vmax = vmax, 
        colorbar = True, 
        boxes = True,
        site = site
        )
    
    site, path_of_ionogram = dg.path_ionogram(dn, target)
    
    pl.plot_single_ionogram(
        path_of_ionogram, 
        ax = ax_ion, 
        aspect = 'auto',
        label = False
        )
        
    pl.plot_roti_timeseries(
        axes, 
        df, 
        target, 
        dn, 
        vmax = 2, 
        right_ticks = False,
        threshold = 0.2
        )
    
        
    fig.text(
        0.03, 0.23, 'ROTI (TECU/min)', 
        fontsize = 25, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.95, 0.25, 'Occurrence', 
        fontsize = 25, 
        rotation = 'vertical'
        )
    
    if save:
        save_image(fig, target, dn)
    
    return fig



def run(folder, save = True, vmax = 10):
    
    dn = im.get_datetime(folder)
    
    df =  pb.concat_files(
          dn, 
          root = 'D:\\'
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
          root = 'D:\\'
          )
    file = im.get_closest(dn, file_like = True)
    
    ds = b.sel_times(df, start, hours = 11)
    
    plot_time_evolution(file, start, ds, vmax = vmax)
    


dn = dt.datetime(2013, 12, 24, 21)
# dn = dt.datetime(2016, 2, 11, 21)
# dn = dt.datetime(2016, 5, 27, 21)
# dn = dt.datetime(2016, 10, 3, 21)
# dn = dt.datetime(2017, 9, 17, 21)
# dn = dt.datetime(2019, 2, 24, 21)
# dn = dt.datetime(2019, 5, 2, 21)
# dn = dt.datetime(2019, 9, 6, 21)

def main(dn, vmax = 40):
    folder_img = f'CA_{dn.year}_{dn.month}{dn.day}'
    run(folder_img, vmax = vmax)
    folder_in = dn.strftime('%Y%m%d')
    b.images_to_gif(
        name =  folder_in, 
        path_out = 'movies',
        path_in = f'movies/{folder_in}/', 
        fps = 20
        )

main(dn, vmax = 60)
# 

# # test_single(dn)
# folder_in = dn.strftime('%Y%m%d')
# b.images_to_gif(
#       name =  folder_in, 
#       path_out = 'movies',
#       path_in = f'movies/{folder_in}/', 
#       fps = 20
#       )

# dn = dt.datetime(2019, 9, 7, 2, 40)
# test_single(dn, vmax = 30)

# plt.show()