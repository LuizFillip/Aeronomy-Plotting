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

b.config_labels(fontsize = 25)



def roti_limit(dn, sector = -50, root = 'E:\\'):
    
    df = pb.concat_files(dn, root = root)

    df = b.sel_times(df, dn, hours = 11)
    
    # return  df.loc[(df['lon']> -40) & (df['lon'] < -30)]
    return pb.filter_region(df, dn.year, sector)
   

def ionogram_path(target, dn, site = 'FZA0M'):
    
    PATH_IONO = dg.path_ionogram(dn, site = site)
    
    dn = dg.closest_iono(target, PATH_IONO)
    
    file = dn.strftime(f'{site}_%Y%m%d(%j)%H%M%S.PNG')
    
    return dn, os.path.join(PATH_IONO, file)
    
    
    
def plot_shades(ax1, n, index, y = 4):
    
    delta = dt.timedelta(minutes = 10)
    
    ax1.text(
        n, y - 1, 
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
             threshold = 0.21,
             label = True
             )
     
     vmax = np.ceil(df['roti'].max()) 
     vmax = 4
     ax_rot.set(
         ylim = [0, vmax + 1], 
         xlim = [df.index[0], df.index[-1]],
         yticks = np.arange(0, vmax + 2, 1)
         )
     
     pl.plot_references_lines(
             ax_rot,
             -50, 
             dn, 
             label_top = 5.2,
             translate = False
             )
     
     b.format_time_axes(ax_rot, translate = False)
     return vmax

def TEC_6300_IONOGRAM_ROTI(
        files, dn, 
        site = 'FZA0M', 
        root = 'E:\\',
        letter = '(a)',
        tec_max = 40
        ):
    
    PATH_SKY = im.path_all_sky(dn, root = root)


    fig = plt.figure(
        dpi = 300,
        figsize = (11,  16),
        layout = 'constrained'
        )
    
    gs2 = GridSpec(len(files), len(files))
    
    gs2.update(hspace = 0.4, wspace = 0)
    
    ax_rot = plt.subplot(gs2[-1, :])
    
    vmax = plot_roti_timeseries(ax_rot, dn)
    vmax = 5
    for col, file in enumerate(files):
        index = col + 1
        
        ax_img = plt.subplot(gs2[0, col])
        
        target = im.plot_images(
            os.path.join(PATH_SKY, file),  
            ax_img, 
            infos = False,
            time_infos = False, 
            fontsize = 20,
            limits = [0.22, 0.95]
            )
        
        title(ax_img, target, index)
        
        ax_ion = plt.subplot(gs2[1, col])
        
        dn1, path_ion = ionogram_path(
            target, dn, site = site)
        
        pl.plot_single_ionogram(
            path_ion, 
            ax = ax_ion, 
            aspect = 'auto',
            label = True,
            ylabel_position = 'left',
            title = False
            )
        
        title(ax_ion, dn1, index)
        # title(ax_ion, dn1, index)
        
        ax_tec = plt.subplot(
            gs2[2, col], projection = ccrs.PlateCarree())
        
        
        
        if index == 2:
            
            ax_ion.text(
                0.6, -0.15, 'Frequência (MHz)',
                transform = ax_ion.transAxes
            )
            ax_tec.text(
                0.6, -0.2, 'Longitude (°)',
                transform = ax_tec.transAxes
            )
        
        
        if index == 4:
            colorbar = True
        else:
            colorbar = False
            
        pl.plot_tec_map(
            target, ax_tec, 
            vmax = tec_max, 
            colorbar = colorbar, 
            root = root
            )
            
        if index == 1:
            ax_ion.set(ylabel = 'Altura virtual (km)')
            
        if index != 1:
            ax_tec.set(
                xticks = np.arange(-90, -20, 20), 
                yticks = np.arange(-40, 40, 20), 
                xticklabels = [], 
                yticklabels = [], 
                xlabel = '', 
                ylabel = '', 
                title = ''
                )
            
            ax_ion.set(
                xticklabels = [], 
                yticklabels = [], 
                xlabel = '', 
                ylabel = '', 
                )
            
        else:
            
            ax_ion.set(
                xlabel = '', 
                )
            
            ax_tec.set(
                xticks = np.arange(-90, -20, 20), 
                yticks = np.arange(-40, 40, 20), 
                xlabel = '', 
                )
            
        title(ax_tec, dn1, index)
        
        plot_shades(ax_rot, target, index, y = vmax + 0.3)
    
    ax_img.text(
        -3.3, 1.1, letter, 
        fontsize = 35,
        transform = ax_img.transAxes
        )
    
    return fig 


def solar_maximum(site =  'SAA0K'):
    dn = dt.datetime(2013, 12, 24, 20)
    
    files = [
        # 'O6_CA_20131224_222810.tif', 
        'O6_CA_20131224_231957.tif',
        'O6_CA_20131225_011602.tif',
        'O6_CA_20131225_021645.tif',
        'O6_CA_20131225_024146.tif'
        ]
    
    
    
    figure_2 = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 60)
    
    dn = dt.datetime(2013, 6, 10, 20)
    
    files = [ 
            
        'O6_CA_20130610_220827.tif',
        'O6_CA_20130610_225828.tif', 
        'O6_CA_20130611_001329.tif', 
        'O6_CA_20130611_023100.tif',
        ]
    
    figure_1 = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 60, letter = '(b)')
    
    fig = b.join_images(figure_2, figure_1)

    FigureName = dn.strftime('validation')
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'products'),
        dpi = 400
        )



def solar_minimum():
    
    site =  'SAA0K'
    
    dn = dt.datetime(2019, 12, 28, 21)
    
    files = [
        'O6_CA_20191228_230604.tif',
        'O6_CA_20191229_001044.tif',
        'O6_CA_20191229_013322.tif', 
        'O6_CA_20191229_023803.tif'
        ]
    
    
    figure_1 = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 10,
        letter = '(a)')
    
    dn = dt.datetime(2019, 6, 24, 21)
    
    files = [
        'O6_CA_20190624_220934.tif',
        'O6_CA_20190624_231934.tif', 
        'O6_CA_20190625_003457.tif', 
        'O6_CA_20190625_010152.tif'
        ]
    
    
    
    figure_2  = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 10,
        letter = '(b)')
    
    
    fig = b.join_images(figure_1, figure_2)
    
    FigureName = dn.strftime('validation_solar_min')
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'products'),
        dpi = 400
        )

# solar_maximum(site =  'SAA0K')


dn = dt.datetime(2019, 5, 2, 20)

files = [
    'O6_CA_20190502_222618.tif',
    'O6_CA_20190503_010603.tif',
    'O6_CA_20190503_014157.tif',
    'O6_CA_20190503_023548.tif'
    ]
site =  'FZA0M'
fig = TEC_6300_IONOGRAM_ROTI(
    files, dn, site, tec_max = 10,
    letter = '')

FigureName = dn.strftime('20190502_validation')
 
fig.savefig(
     b.LATEX(FigureName, folder = 'products'),
     dpi = 400
     )