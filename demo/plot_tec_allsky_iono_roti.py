import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import plotting as pl
import os 
import imager as im
import base as b 
import datetime as dt 
import numpy as np
import PlasmaBubbles as pb 
import cartopy.crs as ccrs
from skimage import io
import GEO as gg

b.config_labels(fontsize = 25)



def roti_limit(dn, sector = -50):
    
    df = pb.concat_files(dn, root = 'D:\\')

    df = b.sel_times(df, dn, hours = 11)
    
    coords = gg.set_coords(dn.year, radius = 10)

    return pb.filter_coords(df, sector, coords)
   





def plot_ionogram(target, ax, site = 'FZA0M'):
            
    dn = closest_iono(target)
    file = dn.strftime(f'{site}_%Y%m%d(%j)%H%M%S.PNG')
    
    infile = os.path.join(PATH_IONO, file)
    
    img = io.imread(infile)
    y, h = 300, 560
    x, w = 188, 559
    
    img = img[y: y + h, x: x + w]
   
    ax.imshow(img)
    
    ax.set(
        xticks = [], 
        yticks = []
        )
    
    return dn
    
    
    
def plot_shades(ax1, n, index, y = 4):
    
    delta = dt.timedelta(minutes = 10)
    
    ax1.text(
        n, y, 
        index, 
        transform = ax1.transData
        )
    
    ax1.axvspan(
        n, n + delta,
        alpha = 0.7, 
        color = 'gray',
        edgecolor = 'k', 
        lw = 2
    )
  
def title(ax, dn, index):
    title = dn.strftime(f'({index}) %Hh%M')
    ax.set(title = title)
 
def plot_roti_timeseries(ax_rot, dn, ref_long = -50):
     
     df = roti_limit(dn)
     
     pl.plot_roti_points(
             ax_rot, df , 
             threshold = 0.25,
             label = True
             )
     vmax = np.ceil(df['roti'].max()) 
     
     ax_rot.set(
         ylim = [0, vmax + 1], 
         xlim = [df.index[0], df.index[-1]],
         yticks = np.arange(0, vmax + 1, 1)
         )
     

     b.format_time_axes(ax_rot, translate = True)
     return vmax

def TEC_6300_IONOGRAM_ROTI(files, dn, site = 'FZA0M', tec_max = 40):
    
    fig = plt.figure(
        dpi = 300,
        figsize = (11,  16),
        layout = 'constrained'
        )
    
    gs2 = GridSpec(len(files), len(files))
    
    gs2.update(hspace = 0.45, wspace = 0)
    
    ax_rot = plt.subplot(gs2[-1, :])
    
    vmax = plot_roti_timeseries(ax_rot, dn)
    
    for col, file in enumerate(files):
        index = col + 1
        
        ax_img = plt.subplot(gs2[0, col])
        
        target = im.plot_images(file, ax_img)
        
        title(ax_img, target, index)
        
        ax_ion = plt.subplot(gs2[1, col])
        
        dn = plot_ionogram(target, ax_ion, site = site)
        
        title(ax_ion, dn, index)
        
        ax_tec = plt.subplot(gs2[2, col], projection = ccrs.PlateCarree())
        
        
        
        if index == 2:
            
            ax_ion.text(
                0.6, -0.1, 'Frequência (MHz)',
                transform = ax_ion.transAxes
            )
            ax_tec.text(
                0.6, -0.1, 'Longitude (°)',
                transform = ax_tec.transAxes
            )
        
        
        if index == 4:
            pl.plot_tec_map(
                target, ax_tec, 
                vmax = tec_max, 
                colorbar = True
                )
        else:
            pl.plot_tec_map(
                target, ax_tec, 
                vmax = tec_max, 
                colorbar = False
                )
            
        if index == 1:
            ax_ion.set(ylabel = 'Altura virtual (km)')
            
        if index != 1:
            ax_tec.set(
                xticks = [], 
                yticks = [], 
                xlabel = '', 
                ylabel = '', 
                title = ''
                )
    
        else:
            
            ax_tec.set(
                xticks = np.arange(-90, -20, 20), 
                yticks = np.arange(-40, 40, 20), 
                xlabel = '', 
                title = ''
                )
            
        
        title(ax_tec, dn, index)
        
        plot_shades(ax_rot, target, index, y = vmax + 0.5)
    
    ax_img.text(
        -3.3, 1.1, '(a)', 
        fontsize = 35,
        transform = ax_img.transAxes
        )
    
    return fig 

dn = dt.datetime(2013, 12, 24, 20)

files = [
    # 'O6_CA_20131224_222810.tif', 
    'O6_CA_20131224_231957.tif',
    'O6_CA_20131225_011602.tif',
    'O6_CA_20131225_021645.tif',
    'O6_CA_20131225_024146.tif'
    ]

# dn = dt.datetime(2013, 6, 10, 20)

# files = [ 
        
#     'O6_CA_20130610_220827.tif',
#     'O6_CA_20130610_225828.tif', 
#     'O6_CA_20130611_001329.tif', 
#     'O6_CA_20130611_010516.tif'
#     ]

# dn = dt.datetime(2022, 7, 24, 20)

# files = [ 
#     'O6_CA_20220725_000007.tif',
#     'O6_CA_20220725_021618.tif',
#     'O6_CA_20220725_034219.tif', 
#     'O6_CA_20220725_041809.tif'
#     ]

site =  'FZA0M'
# site =  'SAA0K'




PATH_SKY = im.path_all_sky(dn)
PATH_IONO = dg.path_ionogram(dn, site = 'SAA0K')





fig  = TEC_6300_IONOGRAM_ROTI(files, dn, site, tec_max = 80)

# FigureName = 'Midnight_validation'
# fig.savefig(
#     b.LATEX(folder_ion, folder = 'products'),
#     dpi = 400
#     )
