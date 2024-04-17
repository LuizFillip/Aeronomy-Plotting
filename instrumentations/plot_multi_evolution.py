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
 
    target = im.plot_images(path_of_image, ax_ion)
    
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
        label = True
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



def run(
        dn, 
        save = True,
        vmax = 10, 
        remove_noise = True,
        root_tec = 'D:\\'
        ):
        
    df =  pb.concat_files(
          dn, 
          root = 'D:\\', 
          remove_noise = remove_noise
          )
    
    date_name = dn.strftime('%Y%m%d')
    b.make_dir(f'movies/{date_name}')
    
    files = os.listdir(im.path_all_sky(dn)) 
    
    for file in tqdm(files, date_name):
    
        plt.ioff()
        plot_time_evolution(
            file, dn, df, 
            vmax = vmax, 
            save = save, 
            root_tec = root_tec
            )
        
        plt.clf()   
        plt.close()   
 


def test_single(dn,  vmax = 25, remove_noise = True):
    
    start = im.round_date(dn)
    
    df =  pb.concat_files(
          start, 
          root = 'D:\\', 
          remove_noise = remove_noise
          )
    
    
    ds = b.sel_times(df, start, hours = 12)
    
    try:
        file = im.get_closest(
            dn, 
            file_like = True, 
            ext = '.png'
            )
    
        plot_time_evolution(file, start, ds, vmax = vmax)
    except:
        file = im.get_closest(
            dn, 
            file_like = True, 
            ext = '.tif'
            )
    
        plot_time_evolution(file, start, ds, vmax = vmax)
    
    plt.show()

    


# 
# dn = 
def main(dn, vmax = 40, site = 'CA'):
    
    run(dn, vmax = vmax)
    
    folder_in = dn.strftime('%Y%m%d')
    
    b.images_to_gif(
        name =  folder_in, 
        path_out = 'movies',
        path_in = f'movies/{folder_in}/', 
        fps = 20
        )
    
# im.save_fool_images('CA_2017_0830', last = False)


dates = {
    dt.datetime(2013, 12, 24, 21): 60,
    dt.datetime(2013, 1, 14, 21): 60,
    dt.datetime(2016, 2, 11, 21): 60,
    dt.datetime(2016, 10, 3, 21): 30,
    dt.datetime(2016, 5, 27, 21): 12, 
    dt.datetime(2017, 9, 17, 21): 12, 
    dt.datetime(2017, 3, 2, 21): 40, 
    dt.datetime(2017, 8, 30, 21): 10, 
    dt.datetime(2018, 3, 19, 21): 12, 
    dt.datetime(2019, 2, 24, 21): 10, 
    dt.datetime(2019, 5, 2, 21): 10, 
    dt.datetime(2019, 9, 6, 21): 8, 
    dt.datetime(2020, 3, 30, 21): 8,
    dt.datetime(2018, 3, 19, 21): 8,
    dt.datetime(2020, 3, 30, 21): 10,
    dt.datetime(2020, 8, 20, 21): 6,
    dt.datetime(2022, 7, 24, 21): 10
    }

# vmaxs = list(dates.keys())

# vmax = vmaxs[0]
# dn = dates[vmax]
dn = dt.datetime(2022, 7, 24, 21)
vmax = 60

dates = [
    '2015-01-19',
    '2015-01-22',
    '2017-08-20', 
    '2017-08-21', 
    '2017-08-22', 
    '2017-09-16',
    '2017-09-21',
    '2017-10-17', 
    '2017-10-20', 
    '2017-10-22', 
    '2019-06-01', 
    '2019-08-29',
    '2019-08-30'
    ]

delta = dt.timedelta(hours = 21)

# for dn in pd.to_datetime(dates):
    
#         folder_in = dn.strftime('%Y%m%d')
        
#         b.images_to_gif(
#             name =  folder_in, 
#             path_out = 'movies',
#             path_in = f'movies/{folder_in}/', 
#             fps = 20
#             )

            
    # run(dn + delta, 
    #     vmax = vmax, 
    #     remove_noise = False,
    #     root_tec = 'F:\\')


dn= dt.datetime(2016, 10, 3)
    
folder_in = dn.strftime('%Y%m%d')


# b.images_to_gif(
#      name =  folder_in, 
#      path_out = 'movies',
#      path_in = f'movies/{folder_in}/', 
#      fps = 20
#      )

b.images_to_movie(
        path_in = f'movies/{folder_in}/', 
        path_out =  'movies/',
        movie_name = folder_in,
        fps = 5
        )