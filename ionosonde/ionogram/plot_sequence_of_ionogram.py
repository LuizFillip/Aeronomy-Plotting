import matplotlib.pyplot as plt
import digisonde as dg
import plotting as pl 
import pandas as pd 
import datetime as dt


        
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
     
        
        path_of_ionogram = dg.ionogram_path(dn, site, root = 'E:\\')
        
        pl.plot_single_ionogram(
            path_of_ionogram, 
            ax = ax, 
            aspect = 'auto',
            label = True,
            ylabel_position = 'left',
            title = False
            )
        time = dn.strftime('%Hh%M')
        
        ax.set(
            ylabel = '',
               xlabel = '', 
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
    # site = 'BVJ03'
    # site = 'FZA0M'
    # site = 'CAJ2M'
    
    dn = dt.datetime(2015, 12, 20, 21)

    
    # delta= dt.timedelta(hours = 1)
    times = pd.date_range(
        dn, 
        freq = '30min', 
        periods = 12
        )
    
    fig = plot_sequence_of_ionogram(times, site)
    
    FigureName = dn.strftime(f'{site}_%Y%m%d')
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'paper2'),
    #       dpi = 300
    #       )

    # 
main()