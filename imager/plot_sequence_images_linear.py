import matplotlib.pyplot as plt 
import datetime as dt
import pandas as pd 
import imager as im  
import base as b 


b.sci_format(fontsize = 25)

def text_BJL(ax, i, dn):
    fontsize = 25
    if dn.hour == 4:
        ax.text(
            0.5, 0.5, 'M', 
            color = 'white', 
            fontsize = fontsize + 5, 
            transform = ax.transAxes
            )
    elif dn.hour == 5:
        ax.text(
            0.5, 0.5, '', 
            color = 'white', 
            fontsize = fontsize + 5, 
            transform = ax.transAxes
            )
    else:
        ax.text(
            0.7 - i/20, 0.5, 'M', 
            color = 'white', 
            fontsize = fontsize + 5, 
            transform = ax.transAxes
            )
        
    
    
    if i >= 3:
        if dn.hour == 4:
            ax.text(
                0.7, 0.8, 'B', 
                color = 'white', 
                fontsize = fontsize + 5, 
                transform = ax.transAxes
                )
            
        elif dn.hour == 5:
            ax.text(
                0.5, 0.5, '', 
                color = 'white', 
                fontsize = fontsize + 5, 
                transform = ax.transAxes
                )
        else:
            ax.text(
                0.72, 0.7, 'B', 
                color = 'white', 
                fontsize = fontsize + 5, 
                transform = ax.transAxes
                )
    
    return None 

def plot_linear_images_sequence(
        times, 
        site, 
        area = 3, 
        fontsize = 25,
        ext = 'I'
        ):
    
    areap = 512 * area
    
    fig, ax = plt.subplots(
        figsize = (13, 14), 
        nrows = 3, 
        ncols = 3,
        )
        
    plt.subplots_adjust(hspace = 0.1, wspace = 0)
    
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
        
        asi.display_original(ax)
        
        dn = im.fn2dn(path_of_image)
        title = dn.strftime('%H:%M UT')
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
            if dn.hour >= 4:
                ax.text(
                    0.1, 0.7, 'B', 
                    color = 'white', 
                    fontsize = fontsize + 5, 
                    transform = ax.transAxes
                    )
            else:
                ax.text(
                    0.1, 0.5, 'B', 
                    color = 'white', 
                    fontsize = fontsize + 5, 
                    transform = ax.transAxes
                    )
        else:
            text_BJL(ax, i, dn)
               
    
    infos = im.sites_infos(site)
    
    fig.suptitle(f'({ext}) {infos.name}', y = 0.95)
    return fig

def main():
    start = dt.datetime(2022, 7, 25, 1, 20)
    
    times = pd.date_range(
        start, freq  = '30min', periods = 12)
    
    fig_1 = plot_linear_images_sequence(
        times, site = 'CA', ext = 'a')
    fig_2 = plot_linear_images_sequence(
        times, site = 'BJL', ext = 'b')
    
    fig = b.join_images(fig_1, fig_2)
    path_to_save = 'G:\\Meu Drive\\Papers\\MSTID_EPBs_Interaction\\Eps\\img\\'
    fig.savefig(
        path_to_save + 'images_sequence',
        dpi = 400
        )
    
main()