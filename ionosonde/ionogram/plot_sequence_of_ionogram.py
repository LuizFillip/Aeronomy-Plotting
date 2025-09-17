import matplotlib.pyplot as plt
import digisonde as dg
import plotting as pl 
import pandas as pd 
import datetime as dt
import base as b 
import numpy as np 

b.sci_format(fontsize = 20)

        
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
         ncols = 4, 
         nrows = 5
         )
    
    plt.subplots_adjust(wspace = 0, hspace = 0.3)
    
    
    for i, ax in enumerate(ax.flat):
        
        dn = times[i]
     
        
        path_of_ionogram = dg.ionogram_path(
            dn, site, root = 'E:\\')
        
        # pl.plot_single_ionogram(
        #     path_of_ionogram, 
        #     ax = ax, 
        #     aspect = 'auto',
        #     label = True,
        #     ylabel_position = 'left',
        #     title = False
        #     )
        
        pl.plot_single_ionogram(
            path_of_ionogram, 
            ax, 
            label = True, 
            ylim = [100, 1200]
            )
        
        time = dn.strftime('%H:%M UT')
        
        ax.set(title = time)
        
        
        if (i != 16):
          
            ax.set(
                yticklabels = [], 
                xticklabels = [], 
                xlabel = '', 
                ylabel = ''
                )
        else:
            ax.set(
                xticks = np.arange(0, 16, 4),
                ylabel = 'Altitude (km)',
                xlabel = 'Frequency (MHz)'
                )
            
    
    
    s = times[0]
    site_name = dg.code_name(site)
    name = s.strftime(f'%d %B, %Y - {site_name}')
    fig.suptitle(name)
    
    return fig 



def main():
    site = 'SAA0K'
    # site = 'BVJ03'
    # site = 'FZA0M'
    # site = 'CAJ2M'
    
    # for site in 
    sites = ['SAA0K', 'FZA0M', 'BVJ03', 'CAJ2M', 'CGK21']
    
    for site in sites:
        dn = dt.datetime(2015, 12, 21, 3)
    
        times = pd.date_range(
            dn, 
            freq = '20min', 
            periods = 20
            )
        
        fig = plot_sequence_of_ionogram(times, site)
        
        FigureName = dn.strftime(f'{site}_%Y%m%d')
        
        folder = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\ionograms\\'
        fig.savefig(
              folder + FigureName,
              dpi = 300
              )

    # 
main()