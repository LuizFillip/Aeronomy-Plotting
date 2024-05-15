import cv2
import os
import matplotlib.pyplot as plt
import digisonde as dg
import plotting as pl 
import pandas as pd 

def plot_ionogram(
        ax, 
        infile, 
        crop = True, 
        format_ = '%H:%M'
        ):

    img = cv2.imread(infile)

    if crop:
        img = dg.crop_image(img) 

    ax.imshow(img)
    
    filename = os.path.split(infile)[-1]
    dn = dg.ionosonde_fname(filename)
    
    ax.set(title = dn.strftime(format_))
    
    ax.axis("off")
    
    return dn
        
def fig_labels(
        fig, 
        fontsize = 30, 
        title = ''
        ):


    fig.text(
        .03, 0.4, 
        "Altitude (km)", 
        rotation = "vertical", 
        fontsize = fontsize
        )
    
    fig.text(
        .45, 0.03, 
        "Frequency (MHz)",
        fontsize = fontsize
        )
    
    fig.suptitle(
        title, 
        y = 0.95, 
        fontsize = fontsize
        )
    


def plot_sequence_of_ionogram(times):
    
    fig, ax = plt.subplots(
         figsize = (16, 10), 
         dpi = 300, 
          sharex = True,
        
         ncols = 4, 
         nrows = 2
         )
    
    plt.subplots_adjust(wspace = 0.1, hspace = 0.3)
    
    site = 'SAA0K'
    for i, ax in enumerate(ax.flat):
        
        dn = times[i]
        filename = dn.strftime(
            f'{site}_%Y%m%d(%j)%H%M%S.PNG')
        path_of_ionogram = os.path.join(
            PATH_IONOGRAM, 
            filename
            )
        pl.plot_single_ionogram(
            path_of_ionogram, 
            ax = ax, 
            aspect = 'auto',
            label = True,
            ylabel_position = 'left',
            title = False
            )
        time = dn.strftime('%Hh%M')
        ax.set(ylabel = '', xlabel = '', 
               title = time)
        
        if ((i == 0) or (i == 4)):
            pass
        else:
            ax.set(yticks = [])
        
      
    # date = dn.strftime('%d/%m/%Y')
    # title = f'{site} - {date}'
    
    fig_labels(
        fig, 
        fontsize = 30, 
        title = 'São Luís'
        )
    
    return


def main():
    PATH_IONOGRAM = 'database/ionogram/20220724S'
    
    files = os.listdir(PATH_IONOGRAM)
      
    files = sorted([f for f in files if 'PNG' in f])
    
    files = files[20:][::3]
    
    times = pd.date_range('2022-07-24 23:30:00', freq = '30min', periods = 8)
    
    plot_sequence_of_ionogram(times)