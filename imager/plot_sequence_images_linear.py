import matplotlib.pyplot as plt 
import datetime as dt
import pandas as pd 
import imager as im  
import base as b 


b.config_labels(fontsize = 25)

def plot_linear_images_sequence(
        times, 
        site, 
        areap, 
        fontsize = 25
        ):

    fig, ax = plt.subplots(
        figsize = (14, 15), 
        nrows = 3, 
        ncols = 3,
        )
        
    plt.subplots_adjust(hspace = 0.15, wspace = 0)
    
    for i, ax in enumerate(ax.flat):
        
        l = b.chars()[i]
        dn = times[i]
        
        path_of_image = im.path_from_closest_dn(
                dn, 
                site = site, 
                )
        
        asi = im.DisplayASI(
            path_of_image, 
            site, 
            areap, 
            limits = [0.25, 0.99]
            )
        
        asi.display(ax)
        
        file_time = im.fn2datetime(path_of_image)
        title = file_time.strftime(f'({l}) %Hh%M UT')
        ax.set_title(title, fontsize = fontsize)
        
        if i != 6:
            
            ax.set(
                xlabel = '', 
                ylabel = '', 
                xticklabels = [], 
                yticklabels = []
                )
        else:
            ax.set_xlabel(
                'Longitude (°)', 
                fontsize = fontsize
                )
            ax.set_ylabel(
                'Latitude (°)', 
                fontsize = fontsize
                )
    
    infos = im.sites_infos(site)
    
    fig.suptitle(infos.name, y = 0.95)
    return fig

alt_ag, areap, site =  250, 1536, 'BJL'

start = dt.datetime(2022, 7, 25, 1, 20)

times = pd.date_range(start, freq  = '30min', periods = 12)

fig = plot_linear_images_sequence(times, site, areap)