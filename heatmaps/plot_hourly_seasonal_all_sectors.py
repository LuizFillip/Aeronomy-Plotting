import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl  
import numpy as np 
import pandas as pd 


b.config_labels()









def plot_seasonal_hourly_all_sectors(
        ds, 
        fontsize = 35, 
        translate = False,
        sector = 1
        ):
    
    fig, ax = plt.subplots(
           ncols = 1,
           nrows = 4,
           dpi = 300, 
           sharex = True, 
           sharey = True,
           figsize = (16, 14)
           )

    plt.subplots_adjust(wspace = 0.05)
     
    values = pb.annual_hourly_all_sectors(
            ds, 
            normalize = True,
            step = 1, 
            percent = True
        )

    z, x, y = values.shape
    step = 1
    yticks = np.arange(20, 32 + step, step)
    cmap = 'jet'


    start = ds.index[0].strftime('%Y-01-01')
    end = ds.index[-1].strftime('%Y-12-31')


    xticks = pd.date_range(start, end, periods = y)

    sectors = list(range(-80, -40, 10))[::-1]
    for i, sector in enumerate(sectors):
        
        pl.plot_terminator(ax[i], sector)
        
        ax[i].set(title = f'Setor: {i + 1}')
        
        ax[i].imshow(
              values[i],
              aspect = 'auto', 
              extent = [xticks[0], xticks[-1], 
                        yticks[0], yticks[-1]],
              cmap = cmap, 
              vmax = 100, 
              vmin = 0
              )
        
        

    if translate:
        ylabel = 'Universal time'
        xlabel = 'Years'
        zlabel = 'Occurrence (\%)'
    else:
        xlabel = 'Anos'
        ylabel = 'Hora universal'
        zlabel = 'Ocorrência (\%)'


    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = cmap,
            fontsize = 25,
            step = 10,
            label = zlabel, 
            sets = [0.32, 0.98, 0.4, 0.02], 
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
    
    b.plot_letters(
        ax, 
        y = 1.04, 
        x = 0, 
        num2white = None
        )
     
    return fig
    

def main():

    ds = b.load('events_class2')
    
    
    ds = ds.loc[(ds['type'] == 'midnight') & 
                (ds['drift'] == 'fresh')]
    
    fig = plot_seasonal_hourly_all_sectors(
            ds, 
            fontsize = 35, 
            translate = False,
            sector = 1
            )
    
    FigureName = 'seasonal_hourly_all_sectors'
    
    fig.savefig(
          b.LATEX(FigureName, 'climatology'),
          dpi = 400)


# main()