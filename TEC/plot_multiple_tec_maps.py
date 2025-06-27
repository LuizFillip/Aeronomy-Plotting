import base as b
import cartopy.crs as ccrs
import datetime as dt
import plotting as pl
import matplotlib.pyplot as plt

b.sci_format(fontsize = 25)


def plot_multiple_tec_maps(
        start, 
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
                boxes = False,
                colorbar = False
                )
            
            x, y = pl.valleys_and_peaks(dn, desired_dx = 5 )
            
            # if row != 2:
            #     if hour
            #     for lon in x:
            #         delta = 3
            #         if lon > -70:
            #             pl.arrow(
            #                 ax, 
            #                 (lon + delta, -10), 
            #                 (lon + delta, 10), 
            #                  text = '')
            
            
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
    # start =  dt.datetime(2014, 2, 2, 22)
    fig = plot_multiple_tec_maps(start, vmax = 60, step = 10)
    
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    FigureName = 'TECmaps_on_sunset'
    
    # fig.savefig(
    #       path_to_save + FigureName,
    #       dpi = 400
    #       )
    
# main()
