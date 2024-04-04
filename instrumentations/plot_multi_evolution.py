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
    
    fig.savefig(f'{folder}/{name}')



def plot_time_evolution(
        file, 
        dn, 
        df, 
        target = None,
        vmax = 10, 
        site = 'SAA0K',
        save = False
        ):

    fig, ax_img, ax_ion, ax_tec, axes = b.layout4(
        figsize = (12, 15), 
        hspace = 0.1, 
        wspace = 0.3
        )
    
      
    path_of_image = os.path.join(
        im.path_all_sky(dn), file
        )
    
    if target is None:
        target = im.plot_images(
            path_of_image, ax_img,
            flip = False)
    else:
        im.plot_images(
            path_of_image, ax_img,
            flip = False)
    
    
    fig.suptitle(
        target.strftime('%Y/%m/%d %Hh%M (UT)'), 
                 y = 1.0)
    
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
        right_ticks = False
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



def run(df, dn, save = True, vmax = 10):

    files = os.listdir(im.path_all_sky(dn)) 
    
    for file in tqdm(files, dn.strftime('%Y%m%d')):
    
        plt.ioff()
        plot_time_evolution(
            file, dn, df, vmax = vmax, save = save)
        
       
        plt.clf()   
        plt.close()   
 






def test_single(dn):
    
    
    # # main()
    # folder = 'CA_2019_0502'
    
    # dn = get_datetime(folder)
    # dn = round_date(target)
    df =  pb.concat_files(
          dn, 
          root = 'D:\\'
          )
    # file = im.get_closest(target)
    # target1 = im.get_closest(target, file_like = False)
    
    file = 'O6_CA_20161004_014908.tif'
    ds = b.sel_times(df, dn, hours = 11)
    
    plot_time_evolution(file, dn, ds, vmax = 20)
    




def main(folder, vmax = 40):
    
    dn = im.get_datetime(folder)
    
    df =  pb.concat_files(
          dn, 
          root = 'D:\\'
          )
    
    
    folder_in = dn.strftime('%Y%m%d')
    b.make_dir(folder_in)
    
    
    run(df, dn, vmax = vmax)
    
    b.images_to_movie(
            path_in = folder_in, 
            path_out = '',
            movie_name = folder_in,
            fps = 12
            )


dn = dt.datetime(2016, 2, 11, 21)

folder = f'CA_{dn.year}_{dn.month}{dn.day}'
main(folder, vmax = 60)


# b.images_to_movie(
#           path_in = folder_in, 
#           path_out = '',
#           movie_name = folder_in,
#           fps = 12
#           )

# folder = '20170917'
folder = dn.strftime('%Y%m%d')
b.images_to_gif(name =  folder, path_in = f'{folder}/')