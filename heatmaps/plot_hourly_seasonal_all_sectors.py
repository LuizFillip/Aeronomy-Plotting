import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl  
import numpy as np 


b.config_labels(fontsize = 30)

def plot_seasonal_hourly_all_sectors(
        ds, 
        fontsize = 35, 
        translate = False,
        cmap = 'jet', 
        line_color = 'w'
        ):
    
    fig, ax = plt.subplots(
           ncols = 1,
           nrows = 4,
           dpi = 300, 
           sharex = True, 
           sharey = True,
           figsize = (16, 14)
           )

    plt.subplots_adjust(hspace = 0.05)
        
    sectors = list(range(-80, -40, 10))[::-1]
    
    bins = pb.range_time(ds, step = 0.5)
   
    for i, sector in enumerate(sectors):
        
        in_sector = ds.loc[(ds['lon'] == sector)] 
        
        df = pb.concated_years(in_sector, bins, normalize = False)

        xticks = df.columns
        yticks = df.index
        values = (df.values / 9) * 100
        
        ax[i].imshow(
              values[::-1] ,
              aspect = 'auto', 
              extent = [xticks[0], xticks[-1], 
                        yticks[0], yticks[-1]],
              cmap = cmap, 
              vmax = 100, 
              vmin = 0
              )
        
        pl.plot_terminator(
            ax[i], 
            sector, 
            float_index = True, 
            color = line_color
            )
        
        l = b.chars()[i]
        ax[i].text(
            0.01, 0.8, 
            f'({l}) Setor {i + 1}', 
            transform = ax[i].transAxes, 
            color = line_color
            )
        
        yticks = np.arange(yticks[0], yticks[-1], 2) 
        ytlabels = np.where(yticks >= 24, yticks - 24, yticks)
        
        ax[i].set(
            ylim = [yticks[0] - 0.5, yticks[-1] + 1],
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
            sets = [0.13, 0.98, 0.75, 0.02], 
            orientation = 'horizontal', 
            levels = 10
            )
        
    fig.text(
        0.5, 0.05,
        xlabel, 
        fontsize = fontsize
        )

    fig.text(
        0.045, 0.41, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    return fig
    

def main():
    epb_type = 'midnight'
    ds = b.load('events_class2')
    
    
    ds = ds.loc[(ds['type'] == epb_type) & 
                (ds['drift'] == 'fresh')]
    
    ds = ds.loc[ds.index.year < 2023]
    fig = plot_seasonal_hourly_all_sectors(
            ds, 
            fontsize = 35, 
            translate = False
            )
    
    FigureName = 'seasonal_hourly_all_sectors'
    
    # fig.savefig(
    #       b.LATEX(FigureName, 'climatology'),
    #       dpi = 400)


main()

