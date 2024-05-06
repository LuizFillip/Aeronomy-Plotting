from plotting import plot_time_evolution
import matplotlib.pyplot as plt 
import os 
import PlasmaBubbles as pb 
import base as b 
import imager as im 
from tqdm import tqdm 
import datetime as dt 

# im.save_fool_images(
#         folder = 'CA_2014_0209', 
#         last = False, 
#         freq = '2min'
#         )

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
 

def main(dn, vmax = 40, site = 'CA'):
    
    run(dn, vmax = vmax)
    
    folder_in = dn.strftime('%Y%m%d')
    
    b.images_to_gif(
        name =  folder_in, 
        path_out = 'movies',
        path_in = f'movies/{folder_in}/', 
        fps = 7
        )
   
dates = {
    dt.datetime(2013, 12, 24, 21): 60,
    dt.datetime(2015, 1, 19, 21): 60,
    dt.datetime(2015, 1, 22, 21): 60,
    dt.datetime(2016, 2, 11, 21): 60,
    dt.datetime(2016, 10, 3, 21): 20, #mid in 1
    
    
    dt.datetime(2017, 8, 20, 21): 6, 
    dt.datetime(2017, 8, 21, 21): 6, 
    dt.datetime(2017, 8, 30, 21): 6, 
    dt.datetime(2017, 9, 16, 21): 6, 
    dt.datetime(2017, 9, 17, 21): 30, 
    # dt.datetime(2017, 9, 21, 21): 6, 
    
    # dt.datetime(2017, 10, 17, 21): 20, 
    dt.datetime(2017, 10, 20, 21): 20, 
    dt.datetime(2017, 10, 22, 21): 50,
    dt.datetime(2018, 3, 19, 21): 6, 
    dt.datetime(2019, 2, 24, 21): 6, 
    dt.datetime(2019, 5, 2, 21): 6, 
    dt.datetime(2019, 9, 6, 21): 6, 
    dt.datetime(2019, 6, 1, 21): 6,
    dt.datetime(2019, 8, 29, 21): 6,
    dt.datetime(2019, 8, 30, 21): 6,
    dt.datetime(2020, 3, 30, 21): 6,
    dt.datetime(2018, 3, 19, 21): 6,
    dt.datetime(2020, 3, 30, 21): 6,
    dt.datetime(2020, 8, 20, 21): 6,
    dt.datetime(2022, 7, 24, 21): 6
    }


def run_all_dates(dates):


    for dn, vmax in dates.items():
        folder_in = dn.strftime('%Y%m%d')
        
        run(
            dn, 
            vmax = vmax, 
            remove_noise = True,
            root_tec = 'F:\\'
            )
        
        try:
            run(
                dn, 
                vmax = vmax, 
                remove_noise = True,
                root_tec = 'F:\\'
                )
            
            b.images_to_gif(
                    name =  folder_in, 
                    path_out = 'movies',
                    path_in = f'movies/{folder_in}/', 
                    fps = 5
                    )
            
            b.images_to_movie(
                    path_in = f'movies/{folder_in}/', 
                    path_out = 'movies/',
                    movie_name = folder_in,
                    fps = 5
                    )
        except:
            print('doest work', dn)
            continue

# dn = dt.datetime(2016, 10, 3, 21)
# folder_in = dn.strftime('%Y%m%d')
# vmax = 25
dn = dt.datetime(2014, 1, 2, 21)
# dn =  dt.datetime(2017, 9, 17, 21)

folder_in = dn.strftime('%Y%m%d')
# run(
#     dn, 
#     vmax = 6, 
#     remove_noise = True,
#     root_tec = 'D:\\'
#     )

# b.images_to_gif(
#         name =  folder_in, 
#         path_out = 'movies',
#         path_in = f'movies/{folder_in}/', 
#         fps = 5
#         )

b.images_to_movie(
        path_in = f'movies/{folder_in}/', 
        path_out = 'movies/',
        movie_name = folder_in,
        fps = 5
        )


