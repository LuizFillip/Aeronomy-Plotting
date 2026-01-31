import matplotlib.pyplot as plt
import plotting as pl
import datetime as dt 
import digisonde as dg 
import base as b
import pandas as pd 




def plot_site_ionogram_sequence(ax, dn, site = 'FZA0M'):

    fname = dg.IonoDir(site, dn).path_from_dn
        
    pl.plot_single_ionogram(
        fname, 
        ax, 
        label = True, 
        ylim = [100, 1200]
        )
    
    title = dn.strftime('%Hh%M')
    
    ax.text(
        0.3, 0.85, 
        title, 
        color = 'w',
        transform = ax.transAxes
        )
    
    return dg.code_name(site)
    

def suptitle(fig, times):
    
    s = times[0]
    e = times[-1].day
    
    name = s.strftime(f'%d - {e} %B, %Y')
    return fig.suptitle(name)

def plot_ionograms_on_multisites(times, sites):
    
    ncols = len(times)
    nrows = len(sites)
    
    fig, ax = plt.subplots(
        figsize = (20, 12), 
        ncols = ncols, 
        nrows = nrows,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.2, wspace=0)
    
    end = nrows - 1
    
    for j, site in enumerate(sites):
        
        for i, dn in enumerate(times):
        
            site_name = plot_site_ionogram_sequence(
                ax[j, i], dn, site
                )
            s = b.chars()[j]
            
            y = 1.03
            x = 0.01
            
            ax[j, 0].text(
                x, y, 
                f'({s}) {site_name}', 
                fontsize = 35,
                transform = ax[j, 0].transAxes
                )
          
            if (i != 0) or (j != end):
              
                ax[j, i].set(
                    yticklabels = [], 
                    xticklabels = [], 
                    xlabel = '', 
                    ylabel = ''
                    )

    suptitle(fig, times)
    
    return fig 

def main():
    sites = [ 'SAA0K', 'BVJ03', 'FZA0M'] #'CAJ2M', 'CGK21'
    
    start = dt.datetime(2015, 12, 20, 21)
    
    times = pd.date_range(start, freq = '1H', periods = 8)
    
    fig = plot_ionograms_on_multisites(times, sites)
    
    
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    FigureName = 'multionogram_sequence'
    
    # fig.savefig(
    #       path_to_save + FigureName,
    #       dpi = 400
    #       )
    
main()