import imager as im  
import base as b 
import os 
import pandas as pd
import datetime as dt 

b.config_labels()


path = 'database/images/BJL_2022_0724/'


def plot_images(axes, dn, path):

    times = pd.date_range(dn, freq  = '30min', periods = 8)
    
    for num, ax in enumerate(axes):
        
        file = im.get_closest(times[num], site = 'BJL')
        path_of_image = os.path.join(path, file)
    
        im.plot_images(
            path_of_image, 
            ax, 
            time_infos = True,
            fontsize = 10, 
            limits = [0.25, 0.90], 
            dt_ps = (340, 510)
            )
        
def plot_keogram_painels(
        fig,
        zon_painel, 
        mer_painel, 
        area_factor = 2,  
        cmap = 'Greys_r', 
        limits = [0.25, 0.90]
        ):
    
    keo = im.KeogramAnalysis(path, area_factor = area_factor)
    
    zonal, merid = keo.make_keo(limits = limits)
    
    zon_painel.imshow(
        zonal, 
        aspect = 'auto', 
        extent =  keo.extend_values(),
        cmap = cmap
        )
    
    mer_painel.imshow(
        merid, 
        aspect = 'auto', 
        extent =  keo.extend_values(),
        cmap = cmap
        )
        
    zon_painel.set(
        ylabel = 'Zonal (W-E)', 
        xticks = [],  
        yticks = keo.yticks()
        )
    mer_painel.set(
        xticks = keo.xticks(),
        yticks = keo.yticks(), 
        ylabel = 'Meridional (N-S)', 
        xlabel = 'Universal time'
        )
    
    for a in [zon_painel, mer_painel]:
        a.axhline(0, lw = 2, color = 'w', linestyle = '--')
        
    fig.suptitle(f'{keo.site} - {keo.date} - {keo.layer}', y = 0.95)



dn = dt.datetime(2022, 7, 25, 0, 10)

def plot_keogram_and_images(dn, path):
    
    fig, axes, zon_ax, mer_ax = b.layout_keo_and_images(
        figsize = (11, 12), 
        wspace = 0., 
        hspace = 0.)
    
    
    plot_images(axes, dn, path)
    plot_keogram_painels(
        fig, 
        zon_ax, 
        mer_ax, 
        area_factor = 2
        )
    
    return fig 





fig = plot_keogram_and_images(dn, path)

#%%%
FigureName = 'keogram_images_bjl_20220724'

    
fig.savefig(
    b.LATEX(FigureName, 'paper2'),
    dpi = 400)