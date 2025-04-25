import base as b
import cartopy.crs as ccrs
import datetime as dt
import plotting as pl
import matplotlib.pyplot as plt
import numpy as np 



b.config_labels(fontsize = 25)




def plot_multiple_tec_maps(
        start, 
        times,
        vmax = 50, 
        step = 10,
        root = 'E:\\'
        ):

    fig, axs = plt.subplots(
         figsize = (16, 14), 
         dpi = 300, 
         ncols = 4, 
         nrows = 3,
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(
        wspace = 0.1, 
        hspace = 0.3
        )
    
    for row in range(3):
        
        delta_day =  dt.timedelta(days = row)
        day = start + delta_day
        
        day_label = day.strftime('%d/%m/%y')
        
        l = b.chars()[row]
        
        axs[row, 0].text(
            -0.4, 1.17,
            f'({l}) {day_label}', 
            fontsize = 30,
            transform = axs[row, 0].transAxes
            )
        
        for col in range(4):
        
            delta = dt.timedelta(hours = col)
            
            dn = day + delta
            
            ax = axs[row, col]
        
            pl.plot_tec_map(
                dn, 
                ax = ax, 
                vmax = vmax, 
                root = root,
                boxes = True,
                colorbar = False
                )
            
            ax.set(title = dn.strftime(f' ({col + 1}) %Hh%M UT'))
            
            if not ((row == 2) and (col == 0)):
                ax.set(
                    xticklabels = [], 
                    yticklabels = [], 
                    xlabel = '', 
                    ylabel = ''
                    )
  
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = vmax, 
            step = step,
            orientation = 'horizontal',
            anchor = [0.3, 0.97, 0.4, 0.02] 
            )
    
    # fig.suptitle(start.strftime('%B %d, %Y'), y = 1.02)
    return fig 

def main():
    
    start =  dt.datetime(2015, 12, 19, 22)
    # start =  dt.datetime(2014, 2, 9, 23)
    # start = dt.datetime(2022, 7, 25, 1)
    hours = np.arange(0, 6, 1)
    fig = plot_multiple_tec_maps(start, hours, vmax = 50)
    
    FigureName = start.strftime('%Y%m%d')
    
    # fig.savefig(
    #     b.LATEX(FigureName, 
    #             folder = 'maps'),
    #     dpi = 400
    #     )
    
main()

# plt.show()
