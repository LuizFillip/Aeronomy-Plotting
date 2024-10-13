import matplotlib.pyplot as plt 
import datetime as dt
import pandas as pd 
import imager as im  
import base as b 


b.config_labels(fontsize = 25)

def text_BJL(ax, i, fontsize):
    ax.text(
        -41 - i/2, -14, 'M', 
        color = 'white', 
        fontsize = fontsize + 5
        )
    
    
    if i >= 4:
        
        ax.text(
            -41, -10, 'B', 
            color = 'white', 
            fontsize = fontsize + 5
            )
    
    return None 

def plot_linear_images_sequence(
        times, 
        site, 
        areap = 1536, 
        fontsize = 25,
        ext = 'I'
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
        
        if site == 'CA':
            ax.text(
                -40, -8, 'B', 
                color = 'white', 
                fontsize = fontsize + 5
                )
        else:
            text_BJL(ax, i, fontsize)
               
    
    infos = im.sites_infos(site)
    
    fig.suptitle(f'({ext}) {infos.name}', y = 0.95)
    return fig

def main():
    start = dt.datetime(2022, 7, 25, 1, 20)
    
    times = pd.date_range(start, freq  = '30min', periods = 12)
    
    fig_1 = plot_linear_images_sequence(times, site = 'CA', ext = 'I')
    fig_2 = plot_linear_images_sequence(times, site = 'BJL', ext = 'II')
    
    fig = b.join_images(fig_1, fig_2)
    
    # fig.savefig(
    #     b.LATEX(FigureName, folder = 'products'),
    #     dpi = 400
    #     )