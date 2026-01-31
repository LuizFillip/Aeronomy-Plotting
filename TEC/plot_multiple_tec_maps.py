import base as b
import cartopy.crs as ccrs
import datetime as dt
import plotting as pl
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator

b.sci_format(fontsize = 20)


def plot_multiple_tec_maps(
        start, 
        vmax = 50, 
        step = 10,
        root = 'E:\\', 
        translate = True
        ):

    if translate:
        hr = 'UT'
        cbar = r'TEC (TECU)' #($10^{16} / m^2$)
    else:
        hr = 'HU'
        cbar = r'CET ($10^{16} / m^2$)' 
        
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
        nxt = day.day + 1
        day_label = day.strftime(f'%d-{nxt} %B %Y')
        
        if not translate:
            day_label = GoogleTranslator(
                source = 'en', 
                target = 'pt'
                ).translate(day_label)
            
        l = b.chars()[row]
        
        axs[row, 0].text(
            -0.4, 1.17,
            f'({l}) {day_label}', 
            fontsize = 25,
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
            
            ax.set(title = dn.strftime(f' ({col + 1}) %H:%M {hr}'))
            
            if not ((row == 2) and (col == 0)):
                ax.set(
                    xticklabels = [], 
                    yticklabels = [], 
                    xlabel = '', 
                    ylabel = ''
                    )
                
    
    arrows = {
        (0, 1): [(-49, -6)],
        (0, 2): [(-52, -8), (-44, -8)], 
        (0, 3): [(-50, -5), (-40, -6), (-60, -4)],
        (2, 2): [(-60, -5), (-50, -5)],             
        (2, 3): [(-63, -5), (-55, -5), (-45, -5)]  
        
    }
    
    pl.add_red_arrows_on_panels(
        axs, 
        arrows, 
        crs = ccrs.PlateCarree(), dy=3, 
        color = "red"
        )
    

                
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = vmax, 
            step = step,
            orientation = 'horizontal',
            anchor = [0.3, 0.97, 0.4, 0.02], 
            label = cbar
            )
    
    return fig 

def main():
    
    translate = True
    
    start = dt.datetime(2015, 12, 19, 22)
    
    fig = plot_multiple_tec_maps(
        start, 
        vmax = 60, 
        step = 10, 
        translate = translate
        )
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    if translate:
        lr = 'en'
    else:
        lr = 'pt'
        
    FigureName = f'TECmaps_on_sunset_{lr}'
    
    fig.savefig(
          path_to_save + FigureName,
          dpi = 400
          )
    
# main()

