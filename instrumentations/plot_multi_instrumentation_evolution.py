import base as b
import matplotlib.pyplot as plt
import plotting as pl 
import datetime as dt
import imager as im 
import os 
import digisonde as dg



files = [ 
    'O6_CA_20220725_000007.tif',
    'O6_CA_20220725_021618.tif',
    'O6_CA_20220725_034219.tif', 
    'O6_CA_20220725_041809.tif'
    ]

dn = dt.datetime(2022, 7, 24, 20)



file = files[1]

def plot_time_evolution(file, dn):
    
    fig, ax_tec, ax_img, ax_ion, ax_ts = b.layout_2(
        nrows = 4, 
        ncols = 3, 
        wspace = 0.1, 
        hspace = 1, 
        figsize = (12, 8)
        )
    
    path_of_image = os.path.join(im.path_all_sky(dn), file)
    
    target = im.plot_images(path_of_image, ax_img)
    
    pl.plot_tec_map(target, ax_tec, vmax = 15, colorbar = False)
    
    path_of_ionogram = dg.path_ionogram(dn, target, site = 'SAA0K')
    
    pl.plot_single_ionogram(path_of_ionogram, ax = ax_ion, label = False)
    
    title = target.strftime('%Y/%m/%d %Hh%M (UT)')
    
    fig.suptitle(title)
    
    return fig

fig = plot_time_evolution(file, dn)