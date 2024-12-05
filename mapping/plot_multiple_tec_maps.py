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


def arrow(ax, xy, xytext, text = '$B_1$', color = 'red'):

    ax.annotate(
        text, xy = xy, 
        xytext=xytext,
        arrowprops=dict(
            color = color,
            lw = 4,
            arrowstyle='->'), 
        transform = ax.transData, 
        fontsize = 40, 
        color = color
        )
    return None 

def plot_arrows_bubbles(axs):
    arrow(axs[0, 1], (-60, -10), (-60, 10), text = '$B_1$')
    arrow(axs[0, 2], (-55, -10), (-55, 10), text = '$B_1$')
    arrow(axs[0, 2], (-65, -10), (-65, 10), text = '$B_2$', 
          color = 'black')
    
    arrow(axs[1, 0], (-50, -10), (-50, 10), text = '$B_1$')
    arrow(axs[1, 0], (-65, -10), (-65, 10), text = '$B_2$', 
          color = 'black')
    
    arrow(axs[1, 1], (-47, -8), (-47, 11), text = '$B_1$')
    arrow(axs[1, 1], (-60, -10), (-60, 10), text = '$B_2$', 
          color = 'black')
    
    arrow(axs[1, 2], (-45, -8), (-45, 11), text = '$B_1$')
    arrow(axs[1, 2], (-58, -10), (-58, 10), text = '$B_2$', 
          color = 'black')
    
    return None 
      

def plot_multiple_tec_maps(
        start, 
        times,
        vmax = 50, 
        step = 1,
        root = 'E:\\'
        ):

    fig, axs = plt.subplots(
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
    
    # plot_arrows_bubbles(axs)
    
    
    for i, ax in enumerate(axs.flat):
        
        delta = dt.timedelta(hours = int(times[i]))
        
        dn = start + delta
        print(dn)
        
        pl.plot_tec_map(
            dn, 
            ax = ax, 
            vmax = vmax, 
            root = root,
            boxes = True,
            colorbar = False
            )
        
        ax.set(title = dn.strftime('%Hh%M UT'))
        
        if i != 0:
            ax.set(
                xticklabels = [], 
                yticklabels = [], 
                xlabel = '', 
                ylabel = ''
                )
    
        l = b.chars()[i]
        ax.text(
            0.02, 1.05,
            f'({l})', 
            fontsize = 30,
            transform = ax.transAxes
            )
    
    
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = vmax, 
            step = step,
            orientation = 'horizontal',
            sets = [0.3, 0.97, 0.4, 0.02] 
            )
    
    # fig.suptitle(start.strftime('%B %d, %Y'), y = 1.02)
    return fig 

def main():
    
    start =  dt.datetime(2015, 12, 20, 20)
    start =  dt.datetime(2014, 2, 9, 23)
    start = dt.datetime(2022, 7, 25, 1)
    hours = np.arange(0, 6, 1)
    fig = plot_multiple_tec_maps(start, hours, vmax = 8)
    
    FigureName = start.strftime('%Y%m%d')
    
    # fig.savefig(
    #     b.LATEX(FigureName, 
    #             folder = 'maps'),
    #     dpi = 400
    #     )
    
main()

plt.show()
