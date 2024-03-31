import base as b
import PlasmaBubbles as pb
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg
import matplotlib.pyplot as plt
from tqdm import tqdm 
import numpy as np 


def plot_roti(ax, df, target, sector = -50):
    
    ds = pb.filter_region(df, target, sector = sector)
    
    pl.plot_roti_points(ax, ds, label = True)
    
    ax.set(
        ylim = [0, 2], 
        yticks = np.arange(0, 2.5, 0.5),
        xlim = [df.index[0], df.index[-1]]
        )
    
    terminator = pb.terminator(sector, dn, float_fmt = False)
    
    ax.axvline(terminator, color = 'k', lw = 2)
    
    b.format_time_axes(ax)

def plot_time_evolution(file, dn, df):
    
    fig, ax_tec, ax_img, ax_ion, ax_ts = b.layout_2(
        nrows = 4, 
        ncols = 3, 
        wspace = 0.2, 
        hspace = 1, 
        figsize = (14, 10)
        )
    
    path_of_image = os.path.join(
        im.path_all_sky(dn), file
        )
    
    target = im.plot_images(path_of_image, ax_img)
    
    pl.plot_tec_map(
        target, 
        ax_tec, 
        vmax = 15, 
        colorbar = False
        )
    
    path_of_ionogram = dg.path_ionogram(
        dn, 
        target, 
        site = 'SAA0K'
        )
    
    pl.plot_single_ionogram(
        path_of_ionogram, 
        ax = ax_ion, 
        label = True
        )
    
    
    plot_roti(ax_ts, df, target)
    
    title = target.strftime('%Y/%m/%d %Hh%M (UT)')
    
    fig.suptitle(title)
    
    folder = dn.strftime('%Y%m%d')
    name = target.strftime('%Y%m%d%H%M%S')
    
    fig.savefig(f'{folder}/{name}')
         
    return fig



def run(df, dn):

    files = os.listdir(im.path_all_sky(dn)) 
    
    for file in tqdm(files):
    
        plt.ioff()
        fig = plot_time_evolution(file, dn, df)
        
        plt.clf()   
        plt.close()   


files = [ 
    'O6_CA_20220725_000007.tif',
    'O6_CA_20220725_021618.tif',
    'O6_CA_20220725_034219.tif', 
    'O6_CA_20220725_041809.tif'
    ]

dn = dt.datetime(2022, 7, 24, 20)


def main():
    df =  pb.concat_files(
         dn, 
         root = 'D:\\'
         )
     
    df = b.sel_times(df, dn, hours = 11)
    
    
    folder = dn.strftime('%Y%m%d')
    b.make_dir(folder)
    
    run(df, dn)
    # file = files[0]
    # fig = plot_time_evolution(file, dn, df)
    b.images_to_movie(
            path_in = folder, 
            path_out = '',
            movie_name = folder,
            fps = 12
            )