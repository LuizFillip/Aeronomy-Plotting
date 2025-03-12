import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl  
import numpy as np 
from mpl_toolkits.axes_grid1 import make_axes_locatable


b.config_labels(fontsize = 30)

def plot_seasonal_hourly_all_sectors(
        ds, 
        fontsize = 35, 
        translate = False,
        cmap = 'jet', 
        line_color = 'w', 
        midnight = True
        ):
    
    sectors = list(range(-70, -40, 10))[::-1]
    
    fig, ax = plt.subplots(
           ncols = 1,
           nrows = len(sectors),
           dpi = 300, 
            sharex = True, 
            sharey = True,
           figsize = (16, 14)
           )

    plt.subplots_adjust(hspace = 0.1)
        
 
    bins = pb.range_time(ds, step = 0.5)
    
    vmax = 29 # sunset
    vmax = 9
    for i, sector in enumerate(sectors):
        
        in_sector = ds.loc[(ds['lon'] == sector)] 
        
        print(in_sector['shift'].min())
        
        df = pb.concated_years(
            in_sector, 
            bins, 
            normalize = False
            )

        xticks = df.columns
        yticks = df.index
        values = df.values 
        
        vls = in_sector['start'].values
        
            # print(values.max())
        # pl.plot_histogram(ax[i], vls, i, bins)
        
        # print(values.max())
        ax[i].imshow(
              (values[::-1] / vmax) * 100,
              aspect = 'auto', 
              extent = [
                  xticks[0], xticks[-1], 
                  yticks[0], yticks[-1]
                  ],
              cmap = cmap, 
              vmax = 100, 
              vmin = 0
              )
        
      
        pl.plot_terminator(
            ax[i], 
            sector, 
            float_index = True, 
            color = line_color,
            midnight = midnight
            )
        
        l = b.chars()[i]
        
        if midnight:
            y = 0.8
        else:
            if i == 3:
                y = 0.1
            else:
                y = 0.8
            
        ax[i].text(
            0.01, y, 
            f'({l}) Setor {i + 1}', 
            transform = ax[i].transAxes, 
            color = line_color, 
            fontsize = 40
            )
        
        yticks = np.arange(yticks[0], yticks[-1], 2) 
        ytlabels = np.where(yticks >= 24, yticks - 24, yticks)
        
        ax[i].set(
            ylim = [yticks[0], yticks[-1]],
            yticks = yticks,
            xlim = [xticks[0], xticks[-1]],
            xticks = np.arange(2013, 2024, 1), 
            yticklabels = ytlabels
            )
        

    if translate:
        ylabel = 'Universal time'
        xlabel = 'Years'
        zlabel = 'Occurrence rate (\%)'
    else:
        xlabel = 'Anos'
        ylabel = 'Hora universal'
        zlabel = 'Taxa de ocorrência (\%)'


    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = cmap,
            fontsize = fontsize,
            step = 10,
            label = zlabel, 
            # sets = [0.13, 0.98, 0.75, 0.02], 
            orientation = 'horizontal', 
            levels = 10
            )
        
    ax[-1].set_xlabel(xlabel, fontsize = fontsize + 5)

    fig.text(
        0.045, 0.41, 
        ylabel, 
        fontsize = fontsize  + 5, 
        rotation = 'vertical'
        )
    
    return fig
    

def main():
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.2)

    ds = p.sel_type('midnight')

    ds
    fig = plot_seasonal_hourly_all_sectors(
            ds, 
            fontsize = 35, 
            translate = False, 
            midnight = True
            )
    
    # FigureName = f'seasonal_hourly_{epb_type}'
    
    # fig.savefig(
    #       b.LATEX(FigureName, 'climatology'),
    #       dpi = 400)


main()

