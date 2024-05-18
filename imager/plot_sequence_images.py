import imager as im  
import matplotlib.pyplot as plt 
import base as b 
import os 



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

b.config_labels()

def plot_sequence_of_images(files):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (18, 9), 
        nrows = 2, 
        ncols = 4
        )
    
    plt.subplots_adjust(hspace = 0.02, wspace = 0.01)
    
    infile = 'database/images/CA_2022_0724/'
    
    for num, ax in enumerate(ax.flat):
        path_of_image = os.path.join(infile, files[num])
    
        im.plot_images(
            path_of_image, 
            ax, 
            time_infos = True,
            fontsize = 18
            )
        
    return fig

fig = plot_sequence_of_images(files)

FigureName = 'Sequence_images_20220724'

fig.savefig(
      b.LATEX(FigureName, folder = 'paper2'),
      dpi = 400
      )