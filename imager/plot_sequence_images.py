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

def plot_sequence_of_images(dn, path):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (18, 9), 
        nrows = 2, 
        ncols = 4
        )
    
    plt.subplots_adjust(hspace = 0.02, wspace = 0.01)
    times = pd.date_range(dn, freq  = '30min', periods = 8)
    
    for num, ax in enumerate(ax.flat):
        
        file = im.get_closest(times[num], site = 'BJL')
        path_of_image = os.path.join(path, file)
    
        im.plot_images(
            path_of_image, 
            ax, 
            time_infos = True,
            fontsize = 18
            )
        
    return fig

infile = 'database/images/BJL_2022_0724/'
dn= dt.datetime(2022, 7, 25, 0)

fig = plot_sequence_of_images(dn, infile)



FigureName = 'Sequence_images_CP_20220724'

# fig.savefig(
#       b.LATEX(FigureName, folder = 'paper2'),
#       dpi = 400
#       )





