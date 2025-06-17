import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import plotting as pl
import os 
import imager as im
import datetime as dt 
import numpy as np
import cartopy.crs as ccrs





    
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
    
    return None 
  
def plot_imager(path_sky: str, ax, index) -> dt.datetime:
    """Plota imagem All-Sky processada em um eixo."""
    
    image = im.DisplayASI(path_sky)
    
    image.display_original(ax)

    dn = image.dn
    title = dn.strftime(f'({index}) %Hh%M')
    ax.set(title = title)
    return dn

def plot_tecmaps_rows(gs2, target, index, col, vmax = 30):
    
    ax_tec = plt.subplot(
        gs2[2, col], projection = ccrs.PlateCarree())
    
    
    if index == 4:
        colorbar = True
    else:
        colorbar = False
        
    pl.plot_tec_map(
        target, ax_tec, 
        vmax = vmax, 
        colorbar = colorbar, 
        root = 'E:\\'
        )
    
    if index == 2:
        ax_tec.text(
            0.6, -0.2, 'Longitude (°)',
            transform = ax_tec.transAxes
        )
    

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
    else:
        ax_tec.set(
            xticks = np.arange(-90, -20, 20), 
            yticks = np.arange(-40, 40, 20), 
            xlabel = '', 
            )


def TEC_6300_IONOGRAM_ROTI(
        files, dn, 
        site = 'FZA0M', 
        root = 'E:\\',
        letter = '(a)',
        tec_max = 40
        ):
    
    PATH_SKY = im.path_asi(dn, root = root)
    
    fig = plt.figure(
        dpi = 300,
        figsize = (12,  12),
        layout = 'constrained'
        )
    
    gs2 = GridSpec(3, len(files))
    
    gs2.update(hspace = 0.4, wspace = 0)
    
    ax_rot = plt.subplot(gs2[-1, :])
    
    vmax = pl.plot_roti_timeseries(
        ax_rot, dn, translate = False)
    vmax = 5
    for col, fn in enumerate(files):
        index = col + 1
        
        ax_img = plt.subplot(gs2[0, col])
        
        target = plot_imager(
            os.path.join(PATH_SKY, fn),  
            ax_img, 
            index
            )
        
        ax_iono = plt.subplot(gs2[1, col])
        
        time_image = im.fn2dn(fn)
        
        dn1, path_iono = dg.iono_path_from_target(
            time_image, site)
        
        pl.plot_single_ionogram(
            path_iono, 
            ax = ax_iono, 
            aspect = 'auto',
            label = True,
            ylabel_position = 'left',
            title = False
            )
        
        
        title = dn1.strftime(f'({index}) %Hh%M')
        ax_iono.set(title = title)
        
        
        
        if index == 2:
            
            ax_iono.text(
                0.6, -0.15, 'Frequência (MHz)',
                transform = ax_iono.transAxes
            )
            
        if index == 1:
            ax_iono.set(ylabel = 'Altura virtual (km)')
            
        if index != 1:
            
            ax_iono.set(
                xticklabels = [], 
                yticklabels = [], 
                xlabel = '', 
                ylabel = '', 
                )
        else:
             
            ax_iono.set(
                xlabel = '', 
                )
                
            
        plot_shades(ax_rot, target, index, y = vmax + 0.3)
    
    ax_img.text(
        -3.3, 1.1, letter, 
        fontsize = 35,
        transform = ax_img.transAxes
        )
    
    return fig 






def main():
    dn = dt.datetime(2016, 10, 3, 20)
    
    site = 'FZA0M'
    site = 'SAA0K'
    
    files = [
        'O6_CA_20161003_232538.tif', 
        'O6_CA_20161004_022602.tif',
        'O6_CA_20161004_031109.tif',
        'O6_CA_20161004_042903.tif'
        
        ]
    fig = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 30,
        letter = '')

# FigureName = dn.strftime('%Y%m%d_validation')

