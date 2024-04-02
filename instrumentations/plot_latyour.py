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




fig, ax_img, ax_ion, ax_tec, axes = b.layout3(
    figsize = (16, 14), 
    hspace = 0.1, 
    wspace = 2
    )

dn = dt.datetime(2013, 12, 24, 21)

df =  pb.concat_files(
     dn, 
     root = 'D:\\'
     )
 
df = b.sel_times(df, dn, hours = 11)
  
  
  # folder = dn.strftime('%Y%m%d')
  # b.make_dir(folder)
  
file = 'O6_CA_20131224_214144.tif'
  
path_of_image = os.path.join(
    im.path_all_sky(dn), file
    )

target = im.plot_images(
    path_of_image, ax_img)

pl.plot_tec_map(
    target, 
    ax_tec, 
    vmax = 80, 
    colorbar = True, 
    boxes= True
    )

path_of_ionogram = dg.path_ionogram(
    dn, 
    target, 
    site = 'FZA0M'# 'SAA0K'
    )

pl.plot_single_ionogram(
    path_of_ionogram, 
    ax = ax_ion, 
    aspect = 'auto',
    label = False 
    )

def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)

fig.suptitle(dn.strftime('%Y/%m/%d %Hh%M (UT)'))

pl.plot_roti_timeseries(
    axes, df, range_time(dn, 200), dn, right_ticks = True)


