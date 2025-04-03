import cv2
import os
import matplotlib.pyplot as plt
import digisonde as dg
import plotting as pl 
import pandas as pd 
import datetime as dt
import base as b 

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
    
    return None 


def plot_sequence_of_ionogram(times, site):
    
    fig, ax = plt.subplots(
         figsize = (16, 10), 
         dpi = 300, 
         sharex = True,
         ncols = 4, 
         nrows = 3
         )
    
    plt.subplots_adjust(wspace = 0.1, hspace = 0.2)
    
    
    for i, ax in enumerate(ax.flat):
        
        dn = times[i]
     
        
        path_of_ionogram = dg.path_from_site_dn(
            dn, site, root = 'E:\\')
        
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
        
        if ((i == 0) or (i == 4) or (i == 8)):
            pass
        else:
            ax.set(yticklabels = [])
    
    
    date = dn.strftime(' - %Y-%m-%d')
    fig_labels(
        fig, 
        fontsize = 30, 
        title = dg.code_name(site) + date
        )
    
    return fig 



def main():
    site = 'SAA0K'
    site = 'BVJ03'
    # site = 'FZA0M'
    # site = 'CAJ2M'
    
    dn = dt.datetime(2015, 12, 20, 21)

    
    # delta= dt.timedelta(hours = 1)
    times = pd.date_range(
        dn, 
        freq = '1H', 
        periods = 12
        )
    
    fig = plot_sequence_of_ionogram(times, site)
    
    FigureName = dn.strftime(f'{site}_%Y%m%d')
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'paper2'),
    #       dpi = 300
    #       )

    # 
# main()