import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 
import plotting as pl 
import numpy as np 


def plot_height_fixes_for_multi_sites(
        sites,
        translate = True,
        cols = list(range(4, 11, 1)),
        fontsize = 35

        ):
    
    fig, ax = plt.subplots(
        nrows = len(sites),
        dpi = 300,
        sharey = True, 
        sharex = True,
        figsize = (16, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    ref_day = dt.datetime(2015, 12, 19)
    
    if translate:
       ylabel = 'Height (km)'
       title = 'Fixed frequencies (MHz)'
    else:
        ylabel = 'Altura (km)'
        title = 'Frequência fixas (MHz)'
        
        
    
    for i, site in enumerate(sites):
        
        df = dg.join_iono_days(
                site, 
                ref_day,
                cols = cols,
                parameter = 'heights'
                )
        
        ax[i].plot(df) 
        
        ax[0].legend(
            cols, 
            ncol = len(cols), 
            title = title,
            bbox_to_anchor = (0.5, 1.9), 
            loc = 'upper center', 
            columnspacing = 0.7
            )
        
        pl.plot_terminators(ax[i], df, site)
        

        ax[i].set(
            ylim = [0, 600],
            yticks = np.arange(100, 800, 200),
            xlim = [df.index[0], df.index[-1]]
            )
        
        s = b.chars()[i]
        name = dg.code_name(site)
        ax[i].text(
            0.02, 0.75, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        start = dt.datetime(2015, 12, 20, 21, 0)
        
        ax[i].axvspan(
              start, 
              start + dt.timedelta(hours = 12), 
              ymin = 0, 
              ymax = 1,
              alpha = 0.2, 
              color = 'gray'
              )
        
    fig.text(
        0.03, 0.35, 
        ylabel, 
        fontsize = fontsize + 5, 
        rotation = 'vertical'
        )
  
    
    
    b.format_time_axes(
        ax[-1], 
        hour_locator = 12, 
        pad = 80, 
        translate = translate, 
        )
        
    return fig

def main():
    sites = [ 'SAA0K', 'BVJ03', 'FZA0M', 'CAJ2M', 'CGK21']

    fig = plot_height_fixes_for_multi_sites(
        sites,
        translate = True
        
        )
    
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    FigureName = 'fixed_heights_sites'
    
    # fig.savefig(
    #       path_to_save + FigureName,
    #       dpi = 400
    #       )

main()