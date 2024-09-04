import base as b
import cartopy.crs as ccrs
import datetime as dt
import plotting as pl
import matplotlib.pyplot as plt
import numpy as np 

def run_in_days(infile):
    for day in range(0, 5, 1):
        delta = dt.timedelta(days = day)
        
        start =  dt.datetime(2016, 1, 11, 21, 0) + delta 
        
        fig = plot_multiple_tec_maps(start, vmax = 50)
        
        FigureName = start.strftime('%Y%m%d')
        fig.savefig(
            b.LATEX(infile + FigureName, 
                    folder = 'maps'),
            dpi = 400
            )

b.config_labels(fontsize = 25)


def plot_multiple_tec_maps(
        start, 
        hours,
        vmax = 50, 
        root = 'E:\\'
        ):

    fig, ax = plt.subplots(
         figsize = (18, 14), 
         dpi = 300, 
         ncols = 3, 
         nrows = 2,
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(
        wspace = 0.1, 
        hspace = 0.1
        )
    
    # minutes = np.arange(0, 400, 30)
    
    for i, ax in enumerate(ax.flat):
                
        dn = start + dt.timedelta(hours = int(hours[i]))
        
        pl.plot_tec_map(
            dn, ax = ax, 
            vmax = vmax, 
            root = root,
            boxes = True,
            colorbar = False
            )
        
        ax.set(title = dn.strftime('%Hh%M UT'))
        
        if i != 0:
            ax.set(xticklabels = [], 
                   yticklabels = [], 
                   xlabel = '', 
                   ylabel = '')
    
        l = b.chars()[i]
        ax.text(0.02, 1.05, f'({l})', 
                fontsize = 30,
                transform = ax.transAxes)
        
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = vmax, 
            orientation = 'horizontal',
            sets = [0.3, 0.97, 0.4, 0.02] 
            )
    
    # fig.suptitle(start.strftime('%B %d, %Y'), y = 1.02)
    return fig 

def main():
    
    start =  dt.datetime(2015, 12, 20, 20)
    start =  dt.datetime(2014, 2, 9, 23)
    hours = np.arange(0, 7, 1)
    fig = plot_multiple_tec_maps(start, hours, vmax = 80)
    
    FigureName = start.strftime('%Y%m%d')
    fig.savefig(
        b.LATEX(FigureName, 
                folder = 'maps'),
        dpi = 400
        )
    
main()

plt.show()
