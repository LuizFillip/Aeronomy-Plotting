import imager as im  
import matplotlib.pyplot as plt 
import base as b 
import os 
import pandas as pd
import datetime as dt 

# 


files = [
    
    'O6_CA_20220724_223406.tif',
    'O6_CA_20220724_234922.tif',
    'O6_CA_20220725_010437.tif',
    'O6_CA_20220725_020908.tif',
    'O6_CA_20220725_025918.tif',
    'O6_CA_20220725_031003.tif',
    'O6_CA_20220725_034554.tif',
    'O6_CA_20220725_042144.tif',
    
    
    ]


files = [
    'O6_CP_20220724_230910.tif',
    'O6_CP_20220724_235544.tif',
    'O6_CP_20220725_004219.tif',
    'O6_CP_20220725_012025.tif',
    'O6_CP_20220725_020700.tif',
    'O6_CP_20220725_030203.tif',
    'O6_CP_20220725_034837.tif',
    'O6_CP_20220725_040533.tif',
    'O6_CP_20220725_044754.tif',
    'O6_CP_20220725_052147.tif'
    
    ]



b.config_labels()

def site_names(site):
    
    imager_codes = {
       "CA": "São João do Cariri", 
       "BJL": "Bom Jesus da Lapa", 
       "CP": "Cachoeira Paulista", 
       "CF": "Comandante Ferraz", 
       "SMS": "São Martinho da Serra"
           }
    
    return imager_codes[site]


def make_path(dn, site, root = 'E:\\images\\'):
    folder = dn.strftime(f'{site}_%Y_%m%d')
    return f'{root}{folder}\\'

def plot_sequence_of_images(
        dn, 
        site, 
        times, 
        shape = (3, 4),
        title = ''
        ):
    
    folder = dn.strftime(f'{site}_%Y_%m%d')
    path = f'E:\\images\\{folder}\\'

    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (18, 14), 
        nrows = shape[0], 
        ncols = shape[1]
        )
    
    plt.subplots_adjust(hspace = 0.01, wspace = 0.01)
    
    for num, ax in enumerate(ax.flat):
        
        file = im.get_closest(times[num], site = site)
        path_of_image = os.path.join(path, file)
    
        im.plot_images(
            path_of_image, 
            ax, 
            time_infos = True,
            fontsize = 15, 
            dt_ps = (353, 510)
            )
        
    fig.suptitle(site_names(site), y = 0.95)
    return fig


def main():
    dn = dt.datetime(2024, 9, 24, 23)
    dn = dt.datetime(2020, 9, 16, 23)
    dn = dt.datetime(2022, 7, 24, 23)
    
    site = 'BJL'
    
    times = pd.date_range(dn, freq  = '30min', periods = 12)
    
    
    fig = plot_sequence_of_images(dn, site, times)
    
    FigureName = f'sequence_{site}_20220724'

# fig.savefig(
#       b.LATEX(FigureName, folder = 'paper2'),
#       dpi = 400
#       )





main()